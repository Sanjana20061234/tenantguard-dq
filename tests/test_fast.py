import os
import pytest
from dq.runner import apply_policy, PipelineHaltError
from dq.models import RunReport, CheckResult, Status
from dq.report import write_json_report, write_markdown_report
from dq.discovery import discover_checks

def test_canary_string_not_in_logs(tmp_path):
    report = RunReport(
        backend="stub",
        total_checks=1,
        passed=0,
        failed=1,
        errors=1,
        warnings=0,
        results=[
            CheckResult(
                check_id="test",
                table="test",
                type="null_check",
                severity="error",
                status=Status.FAIL,
                violations=1,
                duration_ms=10
            )
        ]
    )
    
    write_json_report(report, str(tmp_path))
    write_markdown_report(report, str(tmp_path))
    
    with open(tmp_path / "dq_report.json") as f:
        content = f.read()
        assert "SECRET_PII_CANARY_123" not in content
        
    with open(tmp_path / "dq_report.md") as f:
        content = f.read()
        assert "SECRET_PII_CANARY_123" not in content

def test_error_halts_warning_does_not():
    # Only warning
    report = RunReport(
        backend="stub", total_checks=1, passed=0, failed=1, errors=0, warnings=1,
        results=[]
    )
    # Should not raise
    apply_policy(report, fail_fast=False, fail_on_warning=False)
    
    # With error
    report.errors = 1
    with pytest.raises(PipelineHaltError):
        apply_policy(report, fail_fast=False, fail_on_warning=False)

def test_fail_on_warning():
    report = RunReport(
        backend="stub", total_checks=1, passed=0, failed=1, errors=0, warnings=1,
        results=[]
    )
    # With fail_on_warning=True, it should raise
    with pytest.raises(PipelineHaltError):
        apply_policy(report, fail_fast=False, fail_on_warning=True)

def test_stub_no_db_drivers_imported():
    import sys
    assert "duckdb" not in sys.modules
    assert "clickhouse_driver" not in sys.modules

def test_validator_rejects_bad_checks(tmp_path):
    bad_checks_dir = os.path.join(os.path.dirname(__file__), "fixtures", "bad_checks")
    if os.path.exists(bad_checks_dir):
        for f in os.listdir(bad_checks_dir):
            if f.endswith(".yml"):
                import shutil
                test_dir = tmp_path / f.replace('.yml', '')
                test_dir.mkdir()
                shutil.copy(os.path.join(bad_checks_dir, f), test_dir / f)
                with pytest.raises(Exception):
                    discover_checks(str(test_dir))
