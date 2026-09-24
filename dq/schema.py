from typing import Literal

from pydantic import BaseModel

from dq.models import Severity


class CheckDeclaration(BaseModel, extra="forbid"):
    id: str
    type: str
    severity: Severity

class NullCheck(CheckDeclaration):
    type: Literal["null_check"]
    columns: list[str]

class UniqueKeyCheck(CheckDeclaration):
    type: Literal["unique_key"]
    columns: list[str]

class RangeCheck(CheckDeclaration):
    type: Literal["range_check"]
    column: str
    min: float
    max: float

class Reference(BaseModel):
    table: str
    column: str

class CrossTenantCheck(CheckDeclaration):
    type: Literal["cross_tenant_check"]
    column: str
    references: Reference

class RowCountReconciliationCheck(CheckDeclaration):
    type: Literal["row_count_reconciliation"]
    expected_from: str | None = None
    compare_to: Reference | None = None
    tolerance_pct: float = 0.0

CheckType = NullCheck | UniqueKeyCheck | RangeCheck | CrossTenantCheck | RowCountReconciliationCheck

class TableChecks(BaseModel, extra="forbid"):
    version: int
    table: str
    checks: list[CheckType]
