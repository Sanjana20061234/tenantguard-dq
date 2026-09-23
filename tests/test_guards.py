import pytest
from dq.guards import generate_guards
import yaml

def test_generate_guards(tmp_path):
    catalog = tmp_path / "catalog.yml"
    out_dir = tmp_path / "_generated"
    
    catalog.write_text('''
tables:
  users:
    business_keys: [org_id, user_id]
    parents:
      organisations: org_id
''')

    generate_guards(catalog, out_dir)
    
    out_file = out_dir / "users_guards.yml"
    assert out_file.exists()
    
    with open(out_file, "r") as f:
        data = yaml.safe_load(f)
        
    assert data["table"] == "users"
    checks = {c["id"]: c for c in data["checks"]}
    
    assert "users_org_not_null" in checks
    assert "users_unique_key" in checks
    assert "users_organisations_same_tenant" in checks
    assert "users_rowcount" in checks
