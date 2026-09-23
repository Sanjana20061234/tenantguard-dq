# Architecture

The system is designed to parse declarative YAML files, convert them into `SafeQuery` objects, and execute them on multiple backends. The `SafeQuery` rule engine strictly ensures that no raw data leaks by enforcing count-only aggregation on the queries before execution.

Database interaction is abstracted via a Base `DatabaseAdapter` which can execute on `stub`, `DuckDB`, or `ClickHouse`.
