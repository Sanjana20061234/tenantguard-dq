# Runbook

## Reading the Report
Look at the Status and Message columns. Any ERROR severity check failure will halt the pipeline.

## Triage
- **Null Org ID (BUG-1)**: Indicates corrupted loading. Remediation: Filter out or backfill the org ID.
- **Duplicate Key (BUG-2)**: Upsert failure or bad source data. Remediation: Deduplicate upstream.
- **Cross-Tenant Leak (BUG-3)**: Critical data breach risk! Remediation: Delete violating rows immediately.
- **Range Violation (BUG-4)**: Business logic failure (negative fee). Remediation: Correct the reference data.
- **Row-count Mismatch**: Indicates dropped records during ETL. Remediation: Re-run ETL.

All diagnostic investigations should rely on count queries. A warehouse admin must trace row data separately.
