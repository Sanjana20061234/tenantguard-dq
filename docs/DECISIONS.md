# Decisions

- Opted for explicit python generation of data over Faker to avoid extra dependencies.
- Opted for PyYAML and Typer as minimal core dependencies.
- Fallback for ClickHouse adapter missing is DuckDB which is zero-setup.
- Python execution alias on windows can cause errors if Python is missing; documented that winget installation of Python 3.11 is required.
