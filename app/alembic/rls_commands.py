"""
自定义 Alembic 命令，用于自动为表启用行级安全性
"""

from alembic.operations import Operations, MigrateOperation
from sqlalchemy import text


class EnableRLSCommand(MigrateOperation):
    """启用行级安全性的命令"""

    def __init__(self, table_name):
        self.table_name = table_name

    @classmethod
    def enable_rls(cls, operations, table_name):
        """为指定表启用行级安全性"""
        op = EnableRLSCommand(table_name)
        return operations.invoke(op)


@Operations.implementation_for(EnableRLSCommand)
def enable_rls(operations, operation):
    """实现启用行级安全性的操作"""
    conn = operations.get_bind()
    table_name = operation.table_name

    # 检查表是否存在
    result = conn.execute(
        text(
            f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"
        )
    ).fetchone()

    if result and result[0]:
        # 启用行级安全性
        conn.execute(text(f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY"))

        # 创建默认策略
        try:
            conn.execute(
                text(f"""
            CREATE POLICY allow_all ON {table_name}
                FOR ALL
                USING (true)
            """)
            )
        except Exception as policy_error:
            # 如果策略已存在，会抛出错误，但我们可以忽略它
            if "already exists" in str(policy_error):
                return f"已为表 {table_name} 启用行级安全性，策略已存在"
            else:
                return f"已为表 {table_name} 启用行级安全性，但创建策略时出错: {str(policy_error)}"

        return f"已为表 {table_name} 启用行级安全性"
    else:
        return f"表 {table_name} 不存在，无法启用行级安全性"


# 扩展 Operations 类，添加 enable_rls 方法
Operations.enable_rls = EnableRLSCommand.enable_rls
