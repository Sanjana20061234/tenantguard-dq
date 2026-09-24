# TenantGuard DQ

An extensible, config-driven data quality engine for a multi-tenant wealth-management platform. It evaluates data against YAML-declared checks and automatically guards against duplicate keys, cross-tenant data leaks, and invalid constraints.

## Architecture

```mermaid
graph TD
    A[Checks YAML] --> B[Discovery]
    B --> C[Engine]
    C --> D[SafeQuery Generator]
    D --> E[Database Adapters]
    E --> F[DuckDB / ClickHouse]
    F --> C
    C --> G[RunReport]
    G --> H[CLI / Policy Enforcer]
```

## Quickstart

```bash
pip install -e .
python fixtures\generate_data.py --mode clean`npython fixtures\generate_data.py --mode corrupt
dq demo --backend duckdb
```

## Project Tree
- `dq/`: The core engine
- `fixtures/`: Test data generators
- `checks/`: Declarations
- `docs/`: Documentation
