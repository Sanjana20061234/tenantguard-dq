import sqlglot
from sqlglot import exp

class SafeQuery:
    """
    A verified count-only SQL query.
    Can only be created via verify_and_create().
    """
    def __init__(self, sql: str):
        self._sql = sql

    @property
    def sql(self) -> str:
        return self._sql

def verify_and_create(sql: str, dialect: str = "duckdb") -> SafeQuery:
    """
    Parses the SQL and enforces the security rule:
    - Must be a single SELECT statement.
    - No SELECT *
    - No bare columns in the outermost projection (only aggregates like COUNT are allowed).
    """
    try:
        statements = sqlglot.parse(sql, read=dialect)
    except Exception as e:
        raise ValueError(f"SQL parsing error: {e}")

    if not statements or len(statements) != 1:
        raise ValueError("Query must contain exactly one statement.")

    stmt = statements[0]
    if not isinstance(stmt, exp.Select):
        raise ValueError("Query must be a SELECT statement.")

    # Check for SELECT *
    for projection in stmt.expressions:
        if isinstance(projection, exp.Star):
            raise ValueError("SELECT * is not allowed.")
        # Check if the projection is just a column without an aggregate
        if isinstance(projection, exp.Column):
            raise ValueError("Bare columns in the outermost projection are not allowed. Use COUNT().")

    return SafeQuery(sql)
