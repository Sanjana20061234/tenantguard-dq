from typing import Type, Callable
from dq.schema import CheckDeclaration
from dq.adapters.base import DatabaseAdapter
from dq.safesql import SafeQuery
from dq.models import CheckResult, Status
import time

class BaseCheck:
    def __init__(self, table: str, declaration: CheckDeclaration):
        self.table = table
        self.declaration = declaration

    def build_sql(self, dialect: str) -> SafeQuery:
        raise NotImplementedError

    def execute(self, adapter: DatabaseAdapter) -> CheckResult:
        start_time = time.time()
        result = CheckResult(
            check_id=self.declaration.id,
            table=self.table,
            type=self.declaration.type,
            severity=self.declaration.severity,
            status=Status.PASS
        )
        try:
            query = self.build_sql(adapter.dialect)
            violations = adapter.fetch_scalar_int(query)
            result.violations = violations
            if violations > 0:
                result.status = Status.FAIL
                result.message = f"Found {violations} violations."
        except Exception as e:
            result.status = Status.EXEC_ERROR
            # Note: Mask error details to avoid leaking data
            result.message = f"Execution error: {e.__class__.__name__}"
            
        result.duration_ms = int((time.time() - start_time) * 1000)
        return result

_CHECK_REGISTRY = {}

def register_check(check_type: str):
    def decorator(cls: Type[BaseCheck]):
        _CHECK_REGISTRY[check_type] = cls
        return cls
    return decorator

def get_check(check_type: str) -> Type[BaseCheck]:
    if check_type not in _CHECK_REGISTRY:
        raise ValueError(f"Unknown check type: {check_type}")
    return _CHECK_REGISTRY[check_type]

# Import checks to register them
from . import null_check
from . import unique_key
from . import range_check
from . import cross_tenant
from . import row_count_reconciliation
