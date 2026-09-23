from dq.adapters.base import DatabaseAdapter
from dq.safesql import SafeQuery

class StubAdapter(DatabaseAdapter):
    """
    Adapter for unit tests that returns scripted counts without a database.
    """
    def __init__(self, script: dict[str, int] = None):
        self._script = script or {}
        self._tables = {"organisations": ["organisation_id", "name"]}

    @property
    def dialect(self) -> str:
        return "duckdb"

    def fetch_scalar_int(self, query: SafeQuery) -> int:
        # For tests, we match based on the raw SQL string or inject results via some mechanism.
        # Here we just use the script mapping exact SQL to int, or return 0.
        return self._script.get(query.sql, 0)

    def list_tables(self) -> list[str]:
        return list(self._tables.keys())

    def get_columns(self, table: str) -> list[str]:
        return self._tables.get(table, [])

    def close(self) -> None:
        pass
