from enum import Enum

from pydantic import BaseModel


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"

class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    EXEC_ERROR = "EXEC_ERROR"

class CheckResult(BaseModel):
    check_id: str
    table: str
    type: str
    severity: Severity
    status: Status
    violations: int | None = None
    rows_scanned: int | None = None
    duration_ms: int = 0
    message: str | None = None

class RunReport(BaseModel):
    backend: str
    total_checks: int
    passed: int
    failed: int
    errors: int
    warnings: int
    results: list[CheckResult]
