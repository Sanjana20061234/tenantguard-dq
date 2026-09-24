from dq.adapters.stub_adapter import StubAdapter
from dq.discovery import discover_checks
from dq.engine import run_checks
from dq.schema import TableChecks


def test_discovery_empty(tmp_path):
    checks = discover_checks(tmp_path)
    assert len(checks) == 0

def test_discovery_valid(tmp_path):
    f = tmp_path / "valid.yml"
    f.write_text('''
version: 1
table: test_table
checks:
  - id: t1
    type: null_check
    columns: [id]
    severity: error
''')
    checks = discover_checks(tmp_path)
    assert len(checks) == 1
    assert checks[0].table == "test_table"
    assert checks[0].checks[0].id == "t1"

def test_engine_run():
    f = TableChecks.model_validate({
        "version": 1,
        "table": "test_table",
        "checks": [
            {
                "id": "t1",
                "type": "null_check",
                "columns": ["id"],
                "severity": "error"
            }
        ]
    })
    
    # Stub will return 0 for everything by default -> PASS
    adapter = StubAdapter()
    report = run_checks([f], adapter)
    assert report.passed == 1
    assert report.failed == 0
    
    # Mocking a failure
    adapter = StubAdapter(script={"SELECT COUNT(*) FROM test_table WHERE id IS NULL": 5})
    report = run_checks([f], adapter)
    assert report.passed == 0
    assert report.failed == 1
    assert report.results[0].violations == 5
    assert report.results[0].status == "FAIL"
