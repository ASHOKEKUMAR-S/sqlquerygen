# Unit tests for SQLQueryGenerator
import pytest
from sqlquerygen.sql_query_generator import SQLQueryGenerator

# Sample schema for testing
sample_schema = {
    "hostname": "TEXT",
    "cvss_score": "REAL",
    "severity": "TEXT",
    "status": "TEXT",
    "detection_date": "DATE",
    "age": "INTEGER"
}

def test_basic_select_query():
    generator = SQLQueryGenerator(sample_schema, "scan_results")
    query = generator.generate_query()
    assert query.startswith("SELECT ")
    assert "FROM scan_results" in query
    assert ";" in query

def test_clause_toggles_off():
    generator = SQLQueryGenerator(
        schema=sample_schema,
        table_name="scan_results",
        enable_where=False,
        enable_order_by=False,
        enable_group_by=False,
        enable_having=False,
        enable_limit=False
    )
    query = generator.generate_query()
    assert "WHERE" not in query
    assert "ORDER BY" not in query
    assert "GROUP BY" not in query
    assert "HAVING" not in query
    assert "LIMIT" not in query

def test_query_randomness():
    gen1 = SQLQueryGenerator(sample_schema, "scan_results")
    gen2 = SQLQueryGenerator(sample_schema, "scan_results")
    q1 = gen1.generate_query()
    q2 = gen2.generate_query()
    assert q1 != q2  # Not guaranteed, but highly likely
