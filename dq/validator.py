from dq.discovery import discover_checks
import sys

def validate_checks(checks_dir: str):
    """
    Validates check declarations. 
    Fails (exit 2) on schema violations, unknown check type, duplicate check ids, etc.
    """
    try:
        checks = discover_checks(checks_dir)
        # Check for duplicates
        seen = set()
        for t in checks:
            for c in t.checks:
                if c.id in seen:
                    raise ValueError(f"Duplicate check id found: {c.id}")
                seen.add(c.id)
        # Assuming further detailed validation logic would be here
    except Exception as e:
        print(f"Validation Error: {e}")
        sys.exit(2)
