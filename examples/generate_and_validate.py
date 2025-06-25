import sqlite3
import json
import os
from dotenv import load_dotenv
from sqlquerygen.schema_introspector import SchemaIntrospector
from sqlquerygen.sql_query_generator import SQLQueryGenerator
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
DB_FILE = os.getenv("TEST_SQLITE_DB_PATH")
NUM_QUERIES_PER_TABLE = 5000
OUTPUT_FILE = "outputs/validated_queries.jsonl"
MAX_COMPLEXITY = 6  # Maximum allowed complexity score (SELECT=1, WHERE=1, GROUP BY=1, HAVING=1, ORDER BY=1, LIMIT=0.5)

def query_complexity_score(query: str) -> float:
    score = 1.0  # base score for SELECT
    if "WHERE" in query: score += 1
    if "GROUP BY" in query: score += 1
    if "HAVING" in query: score += 1
    if "ORDER BY" in query: score += 1
    if "LIMIT" in query: score += 0.5
    return score

def validate_query(query: str, conn) -> bool:
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        return True
    except sqlite3.Error:
        return False

def generate_and_validate_for_table(table: str, table_schema: dict, db_path: str) -> list:
    conn = sqlite3.connect(db_path)
    generator = SQLQueryGenerator(
        schema=table_schema,
        table_name=table,
        enable_where=True,
        enable_group_by=True,
        enable_having=True,
        enable_order_by=True,
        enable_limit=True
    )

    validated = []
    for _ in range(NUM_QUERIES_PER_TABLE):
        query = generator.generate_query()
        if query_complexity_score(query) <= MAX_COMPLEXITY and validate_query(query, conn):
            validated.append({ "table": table, "query": query })
    conn.close()
    return validated

def main():
    if not DB_FILE or not os.path.exists(DB_FILE):
        print(f"❌ Database not found at {DB_FILE}")
        return

    os.makedirs("outputs", exist_ok=True)
    introspector = SchemaIntrospector(DB_FILE)
    schema = introspector.get_schema()
    introspector.close()

    all_validated_queries = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(generate_and_validate_for_table, table, schema[table], DB_FILE): table
            for table in schema
        }
        for future in as_completed(futures):
            all_validated_queries.extend(future.result())

    with open(OUTPUT_FILE, "w") as f:
        for item in all_validated_queries:
            f.write(json.dumps(item) + "\n")

    print(f"✅ {len(all_validated_queries)} valid queries written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
