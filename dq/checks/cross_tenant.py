from dq.checks import BaseCheck, register_check
from dq.safesql import verify_and_create
from dq.schema import CrossTenantCheck


@register_check("cross_tenant_check")
class CrossTenantCheckImpl(BaseCheck):
    def build_sql(self, dialect: str):
        decl: CrossTenantCheck = self.declaration
        # COUNT(*) of child rows joined to parent on the FK where child.organisation_id <> parent.organisation_id
        parent_table = decl.references.table
        parent_col = decl.references.column
        
        sql = f"""
            SELECT COUNT(*)
            FROM {self.table} child
            INNER JOIN {parent_table} parent ON child.{decl.column} = parent.{parent_col}
            WHERE child.organisation_id <> parent.organisation_id
        """
        return verify_and_create(sql, dialect)
