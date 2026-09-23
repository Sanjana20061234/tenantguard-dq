# Check Reference

- **null_check**: `COUNT(*)` where any listed column `IS NULL`.
- **unique_key**: `SELECT COUNT(*) FROM (SELECT k1,k2 FROM t GROUP BY k1,k2 HAVING COUNT(*) > 1)`.
- **range_check**: `COUNT(*)` where column < min or > max (NULLs are not range violations).
- **cross_tenant_check**: `COUNT(*)` of child rows joined to parent on the FK where `child.organisation_id <> parent.organisation_id`.
- **row_count_reconciliation**: actual `COUNT(*)` vs expected manifest.
