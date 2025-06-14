# Reads schema and data from SQLite DB
import sqlite3
from typing import Dict, List


class SchemaIntrospector:
    def __init__(self, sqlite_path: str):
        self.sqlite_path = sqlite_path
        self.conn = sqlite3.connect(sqlite_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_tables(self) -> List[str]:
        """Returns list of all non-system tables in the SQLite DB."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        return [row["name"] for row in self.cursor.fetchall()]

    def get_columns(self, table_name: str) -> Dict[str, str]:
        """Returns a dictionary of column names and types for a given table."""
        self.cursor.execute(f"PRAGMA table_info('{table_name}');")
        return {row["name"]: row["type"] for row in self.cursor.fetchall()}

    def get_schema(self) -> Dict[str, Dict[str, str]]:
        """Returns the full schema as a dictionary: {table: {column: type}}"""
        schema = {}
        for table in self.get_tables():
            schema[table] = self.get_columns(table)
        return schema

    def sample_column_values(self, table_name: str, column_name: str, limit: int = 5) -> List[str]:
        """Returns sample values from a given column."""
        query = f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL LIMIT {limit};"
        try:
            self.cursor.execute(query)
            return [row[column_name] for row in self.cursor.fetchall()]
        except Exception:
            return []

    def close(self):
        """Closes the SQLite connection."""
        self.conn.close()
