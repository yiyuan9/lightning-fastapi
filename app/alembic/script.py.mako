"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}
    
    # 检查是否有新创建的表，如果有，为它们启用行级安全性
    # 这是一个备用方案，以防编译器钩子未能正确工作
    from sqlalchemy import inspect, text
    from sqlalchemy.engine import reflection
    
    # 获取连接
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # 获取所有表
    tables = inspector.get_table_names()
    
    # 为每个表启用行级安全性
    for table in tables:
        try:
            # 检查表是否已经启用了RLS
            result = conn.execute(text(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'")).fetchone()
            if result and not result[0]:  # 如果表存在且未启用RLS
                print(f"为表 {table} 启用行级安全性")
                op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
                
                # 创建默认策略
                try:
                    op.execute(f"""
                    CREATE POLICY allow_all ON {table}
                        FOR ALL
                        USING (true)
                    """)
                    print(f"为表 {table} 创建了默认策略")
                except Exception as policy_error:
                    # 如果策略已存在，会抛出错误，但我们可以忽略它
                    if "already exists" in str(policy_error):
                        print(f"表 {table} 的默认策略已存在，跳过创建")
                    else:
                        print(f"为表 {table} 创建默认策略时出错: {str(policy_error)}")
        except Exception as e:
            print(f"为表 {table} 启用RLS时出错: {str(e)}")


def downgrade():
    ${downgrades if downgrades else "pass"}
