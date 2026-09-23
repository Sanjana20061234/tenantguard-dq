import yaml
from pathlib import Path
from typing import Any
from dq.schema import TableChecks

def load_yaml(path: Path) -> Any:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def discover_checks(checks_dir: str | Path) -> list[TableChecks]:
    checks_dir = Path(checks_dir)
    discovered = []
    
    if not checks_dir.exists():
        return discovered
        
    for yaml_file in checks_dir.rglob("*.yml"):
        data = load_yaml(yaml_file)
        if not data:
            continue
        try:
            # Validate via Pydantic
            table_checks = TableChecks.model_validate(data)
            discovered.append(table_checks)
        except Exception as e:
            raise ValueError(f"Failed to parse {yaml_file}: {e}")
            
    return discovered
