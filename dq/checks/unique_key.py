from dq.checks import BaseCheck, register_check
from dq.safesql import verify_and_create
from dq.schema import UniqueKeyCheck


@register_check("unique_key")
class UniqueKeyCheckImpl(BaseCheck):
    def build_sql(self, dialect: str):
        decl: UniqueKeyCheck = self.declaration
        cols = ", ".join(decl.columns)
        # SELECT COUNT(*) FROM (SELECT k1,k2 FROM t GROUP BY k1,k2 HAVING COUNT(*) > 1)
        sql = f"SELECT COUNT(*) FROM (SELECT {cols} FROM {self.table} GROUP BY {cols} HAVING COUNT(*) > 1) AS subq"
        return verify_and_create(sql, dialect)
