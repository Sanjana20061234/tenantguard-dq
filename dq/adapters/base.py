from abc import ABC, abstractmethod
from typing import Any
from dq.safesql import SafeQuery

class DatabaseAdapter(ABC):
    @property
    @abstractmethod
    def dialect(self) -> str:
        """SQL dialect name (e.g., 'duckdb', 'clickhouse')."""
        pass

    @abstractmethod
    def fetch_scalar_int(self, query: SafeQuery) -> int:
        """Executes a SafeQuery and returns the scalar integer result."""
        pass

    @abstractmethod
    def list_tables(self) -> list[str]:
        """Lists available tables."""
        pass

    @abstractmethod
    def get_columns(self, table: str) -> list[str]:
        """Gets columns for a specific table."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Closes the connection."""
        pass
