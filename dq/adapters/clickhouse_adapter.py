import clickhouse_connect
from dq.adapters.base import DatabaseAdapter
from dq.safesql import SafeQuery
import os

class ClickHouseAdapter(DatabaseAdapter):
    def __init__(self, host="localhost", port=8123, username="default", password=""):
        self.client = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)
        
    @property
    def dialect(self) -> str:
        return "clickhouse"

    def fetch_scalar_int(self, query: SafeQuery) -> int:
        try:
            result = self.client.query(query.sql)
            if result.result_rows and len(result.result_rows) > 0:
                row = result.result_rows[0]
                if row and len(row) > 0:
                    return int(row[0])
            return 0
        except Exception as e:
            raise RuntimeError(e.__class__.__name__)

    def list_tables(self) -> list[str]:
        res = self.client.query("SHOW TABLES")
        return [r[0] for r in res.result_rows]

    def get_columns(self, table: str) -> list[str]:
        res = self.client.query(f"DESCRIBE TABLE {table}")
        return [r[0] for r in res.result_rows]

    def close(self) -> None:
        self.client.close()
