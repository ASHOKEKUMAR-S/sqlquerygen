import os
import pytest
from sqlquerygen.schema_introspector import SchemaIntrospector
from dotenv import load_dotenv

load_dotenv()

# This assumes you have an existing DB at the given path
@pytest.fixture(scope="module")
def sqlite_test_db_path():
    db_path = os.getenv("TEST_SQLITE_DB_PATH")
    if not db_path or not os.path.exists(db_path):
        pytest.skip("TEST_SQLITE_DB_PATH not set or file not found.")
    return db_path


def test_get_tables(sqlite_test_db_path):
    introspector = SchemaIntrospector(sqlite_test_db_path)
    tables = introspector.get_tables()
    assert isinstance(tables, list)
    assert all(isinstance(t, str) for t in tables)
    assert len(tables) > 0  # DB should not be empty
    introspector.close()


def test_get_columns(sqlite_test_db_path):
    introspector = SchemaIntrospector(sqlite_test_db_path)
    tables = introspector.get_tables()
    for table in tables:
        columns = introspector.get_columns(table)
        assert isinstance(columns, dict)
        assert all(isinstance(col, str) for col in columns)
        assert all(isinstance(col_type, str) for col_type in columns.values())
    introspector.close()


def test_get_schema(sqlite_test_db_path):
    introspector = SchemaIntrospector(sqlite_test_db_path)
    schema = introspector.get_schema()
    assert isinstance(schema, dict)
    assert len(schema) > 0
    for table, columns in schema.items():
        assert isinstance(columns, dict)
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in columns.items())
    introspector.close()
