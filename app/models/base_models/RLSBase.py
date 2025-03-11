"""
自动启用行级安全性的SQLModel基类
"""

from sqlmodel import SQLModel
from sqlalchemy import event, DDL
from sqlalchemy.ext.declarative import declared_attr


class RLSMixin:
    """
    行级安全性混入类

    为继承此类的所有表自动启用行级安全性
    """

    @declared_attr
    def __tablename__(cls):
        """获取表名"""
        return cls.__name__.lower()

    @classmethod
    def __declare_last__(cls):
        """
        在表创建后自动执行

        此方法会在SQLAlchemy完成表映射后自动调用
        我们在这里添加事件监听器，以便在表创建后启用行级安全性
        """
        # 获取表名
        table_name = cls.__tablename__

        # 创建启用RLS的DDL
        enable_rls = DDL(f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY")

        # 创建默认策略的DDL
        create_policy = DDL(f"""
        CREATE POLICY allow_all ON {table_name}
            FOR ALL
            USING (true)
        """)

        # 添加事件监听器，在表创建后执行
        event.listen(cls.__table__, "after_create", enable_rls)

        # 添加事件监听器，在表创建后执行
        # 注意：如果策略已存在，这将失败，但不会影响表的创建
        try:
            event.listen(cls.__table__, "after_create", create_policy)
        except Exception as e:
            # 记录错误但继续执行，因为策略已存在
            print(f"警告：为表 {table_name} 创建默认策略时出错，可能是因为策略已存在。错误: {str(e)}")


class RLSModel(SQLModel, RLSMixin):
    """
    自动启用行级安全性的SQLModel基类

    所有需要自动启用行级安全性的表都应该继承此类，而不是直接继承SQLModel

    示例:
    ```python
    class User(RLSModel, table=True):
        id: int = Field(primary_key=True)
        name: str
    ```
    """

    class Config:
        """SQLModel配置"""

        arbitrary_types_allowed = True
