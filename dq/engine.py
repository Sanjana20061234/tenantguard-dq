from dq.schema import TableChecks
from dq.models import CheckResult, RunReport, Status
from dq.adapters.base import DatabaseAdapter
from dq.checks import get_check

def run_checks(checks: list[TableChecks], adapter: DatabaseAdapter) -> RunReport:
    results = []
    for table_checks in checks:
        for decl in table_checks.checks:
            check_cls = get_check(decl.type)
            check_instance = check_cls(table_checks.table, decl)
            result = check_instance.execute(adapter)
            results.append(result)

    passed = sum(1 for r in results if r.status == Status.PASS)
    failed = sum(1 for r in results if r.status == Status.FAIL)
    errors = sum(1 for r in results if r.status == Status.EXEC_ERROR)
    warnings = sum(1 for r in results if r.status == Status.FAIL and r.severity == "warning")
    # For reporting, failure count usually means error failures that halt
    errors += sum(1 for r in results if r.status == Status.FAIL and r.severity == "error")

    report = RunReport(
        backend=adapter.dialect,
        total_checks=len(results),
        passed=passed,
        failed=failed,
        errors=errors,
        warnings=warnings,
        results=results
    )
    return report
