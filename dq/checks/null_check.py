from dq.checks import BaseCheck, register_check
from dq.safesql import verify_and_create
from dq.schema import NullCheck

@register_check("null_check")
class NullCheckImpl(BaseCheck):
    def build_sql(self, dialect: str):
        decl: NullCheck = self.declaration
        # COUNT(*) where any listed column IS NULL
        conditions = " OR ".join([f"{col} IS NULL" for col in decl.columns])
        sql = f"SELECT COUNT(*) FROM {self.table} WHERE {conditions}"
        return verify_and_create(sql, dialect)
