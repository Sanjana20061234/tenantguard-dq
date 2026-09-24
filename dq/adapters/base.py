from abc import ABC, abstractmethod

from dq.safesql import SafeQuery


class DatabaseAdapter(ABC):
    @property
    @abstractmethod
    def dialect(self) -> str:
        """SQL dialect name (e.g., 'duckdb', 'clickhouse')."""

    @abstractmethod
    def fetch_scalar_int(self, query: SafeQuery) -> int:
        """Executes a SafeQuery and returns the scalar integer result."""

    @abstractmethod
    def list_tables(self) -> list[str]:
        """Lists available tables."""

    @abstractmethod
    def get_columns(self, table: str) -> list[str]:
        """Gets columns for a specific table."""

    @abstractmethod
    def close(self) -> None:
        """Closes the connection."""
