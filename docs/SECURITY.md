# Security

TenantGuard DQ strictly enforces a count-only execution model. 
Raw data cannot leak into logs or reports because:
1. `SafeQuery` uses `sqlglot` to verify that `SELECT *` and raw column projections are rejected. Only count aggregations are allowed.
2. The `DatabaseAdapter` interface only accepts `SafeQuery` objects and only returns scalars (ints).
3. `redaction.py` applies a logging filter to scrub unexpected row formats or potential PII strings.
