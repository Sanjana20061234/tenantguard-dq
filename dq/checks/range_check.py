from dq.checks import BaseCheck, register_check
from dq.safesql import verify_and_create
from dq.schema import RangeCheck

@register_check("range_check")
class RangeCheckImpl(BaseCheck):
    def build_sql(self, dialect: str):
        decl: RangeCheck = self.declaration
        # COUNT(*) where column < min or column > max. NULLs are not violations.
        sql = f"SELECT COUNT(*) FROM {self.table} WHERE CAST({decl.column} AS FLOAT) < {decl.min} OR CAST({decl.column} AS FLOAT) > {decl.max}"
        return verify_and_create(sql, dialect)
