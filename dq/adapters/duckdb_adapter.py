from pathlib import Path

import duckdb

from dq.adapters.base import DatabaseAdapter
from dq.safesql import SafeQuery


class DuckDBAdapter(DatabaseAdapter):
    """
    In-memory DuckDB adapter that loads CSVs.
    """
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.conn = duckdb.connect(database=':memory:')
        self._load_data()

    def _load_data(self):
        if not self.data_dir.exists():
            return
        
        for csv_file in self.data_dir.glob("*.csv"):
            table_name = csv_file.stem
            # Load CSV into DuckDB
            # We enforce all columns are read as VARCHAR to avoid type inference issues during tests
            query = f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file}', all_varchar=true)"
            self.conn.execute(query)

    @property
    def dialect(self) -> str:
        return "duckdb"

    def fetch_scalar_int(self, query: SafeQuery) -> int:
        try:
            result = self.conn.execute(query.sql).fetchone()
            if result and result[0] is not None:
                return int(result[0])
            return 0
        except Exception as e:  # noqa: BLE001
            # Mask driver specific errors to prevent data leakage
            raise RuntimeError(e.__class__.__name__)

    def list_tables(self) -> list[str]:
        res = self.conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
        return [r[0] for r in res]

    def get_columns(self, table: str) -> list[str]:
        res = self.conn.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}'").fetchall()
        return [r[0] for r in res]

    def close(self) -> None:
        self.conn.close()
