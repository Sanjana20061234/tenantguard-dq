import yaml
from pathlib import Path
from dq.schema import TableChecks

def generate_guards(catalog_path: str | Path, output_dir: str | Path):
    catalog_path = Path(catalog_path)
    output_dir = Path(output_dir)
    
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found at {catalog_path}")
        
    with open(catalog_path, "r") as f:
        catalog = yaml.safe_load(f)
        
    tables = catalog.get("tables", {})
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean previous generated
    for f in output_dir.glob("*.yml"):
        f.unlink()
        
    for table_name, table_info in tables.items():
        checks = []
        
        # 1. Null check on organisation_id
        if table_name != "organisations" or "organisation_id" in table_info.get("business_keys", []):
            checks.append({
                "id": f"{table_name}_org_not_null",
                "type": "null_check",
                "columns": ["organisation_id"],
                "severity": "error"
            })
            
        # 2. Business key unique check
        bkeys = table_info.get("business_keys", [])
        if bkeys:
            checks.append({
                "id": f"{table_name}_unique_key",
                "type": "unique_key",
                "columns": bkeys,
                "severity": "error"
            })
            
        # 3. Cross-tenant check for each parent
        parents = table_info.get("parents", [])
        for p in parents:
            parent_table = p['table']
            fk_col = p['column']
            checks.append({
                "id": f"{table_name}_{parent_table}_same_tenant",
                "type": "cross_tenant_check",
                "column": fk_col,
                "references": {
                    "table": parent_table,
                    "column": fk_col
                },
                "severity": "error"
            })
                
        # 4. Row count reconciliation
        checks.append({
            "id": f"{table_name}_rowcount",
            "type": "row_count_reconciliation",
            "expected_from": "manifest",
            "tolerance_pct": 0,
            "severity": "warning"
        })
        
        doc = {
            "version": 1,
            "table": table_name,
            "checks": checks
        }
        
        # Validate through schema to ensure correctness
        TableChecks.model_validate(doc)
        
        out_file = output_dir / f"{table_name}_guards.yml"
        header = "# AUTO-GENERATED, DO NOT EDIT\n"
        with open(out_file, "w") as f:
            f.write(header)
            yaml.dump(doc, f, sort_keys=False)
