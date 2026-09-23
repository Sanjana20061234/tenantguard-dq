import pytest
from dq.safesql import verify_and_create

def test_safequery_valid():
    sq = verify_and_create("SELECT COUNT(*) FROM table WHERE col IS NULL")
    assert sq.sql == "SELECT COUNT(*) FROM table WHERE col IS NULL"

def test_safequery_rejects_select_star():
    with pytest.raises(ValueError, match="SELECT \* is not allowed"):
        verify_and_create("SELECT * FROM table")

def test_safequery_rejects_bare_columns():
    with pytest.raises(ValueError, match="Bare columns in the outermost projection are not allowed"):
        verify_and_create("SELECT col FROM table")

def test_safequery_rejects_multiple_statements():
    with pytest.raises(ValueError, match="Query must contain exactly one statement"):
        verify_and_create("SELECT COUNT(*) FROM t; SELECT COUNT(*) FROM t;")
