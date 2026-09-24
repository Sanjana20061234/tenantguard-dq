import json
from pathlib import Path

from dq.checks import BaseCheck, register_check
from dq.safesql import verify_and_create
from dq.schema import RowCountReconciliationCheck


@register_check("row_count_reconciliation")
class RowCountReconciliationCheckImpl(BaseCheck):
    def build_sql(self, dialect: str):
        # This one is tricky because it compares COUNT(*) to expected value.
        # It's an engine check, but the security requirement says only count queries are permitted.
        # We can just run a query that returns how many rows are out of tolerance (0 or 1).
        
        decl: RowCountReconciliationCheck = self.declaration
        
        if decl.expected_from == "manifest":
            # Load manifest
            manifest_path = Path("fixtures/manifest.json")
            if not manifest_path.exists():
                expected = 0
            else:
                with open(manifest_path, "r") as f:
                    manifest = json.load(f)
                expected = manifest.get(self.table, 0)
                
            tol_min = expected * (1 - decl.tolerance_pct / 100)
            tol_max = expected * (1 + decl.tolerance_pct / 100)
            
            # Return 1 if out of bounds, else 0
            sql = f"""
                SELECT COUNT(*) FROM (
                    SELECT COUNT(*) as c FROM {self.table}
                    HAVING c < {tol_min} OR c > {tol_max}
                ) as subq
            """
        else:
            other_table = decl.compare_to.table
            sql = f"""
                SELECT COUNT(*) FROM (
                    SELECT 
                        (SELECT COUNT(*) FROM {self.table}) as c1,
                        (SELECT COUNT(*) FROM {other_table}) as c2
                    HAVING c1 <> c2
                ) as subq
            """
            
        return verify_and_create(sql, dialect)
