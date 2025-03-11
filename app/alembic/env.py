import os
import logging
from app.models.table import SQLModel
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool, text
from sqlalchemy.schema import CreateTable
from alembic import op

# 导入自定义的RLS命令
try:
    from app.alembic.rls_commands import EnableRLSCommand
except ImportError:
    # 如果导入失败，记录警告但不中断执行
    logging.warning("无法导入RLS命令，可能需要手动启用行级安全性")

# 导入必要的模块

# 从配置中获取 Alembic 配置对象
config = context.config

# 解释用于 Python 日志记录的配置文件。
# 这行设置了日志记录器。
fileConfig(config.config_file_name)

# 获取logger实例
logger = logging.getLogger("alembic")

target_metadata = SQLModel.metadata

# 自定义表创建监听器，用于自动添加行级安全性
from sqlalchemy import event
from sqlalchemy.schema import DDLElement
from sqlalchemy.ext.compiler import compiles


class EnableRLS(DDLElement):
    def __init__(self, table_name):
        self.table_name = table_name


@compiles(EnableRLS)
def compile_enable_rls(element, compiler, **kw):
    return f"ALTER TABLE {element.table_name} ENABLE ROW LEVEL SECURITY;"


@compiles(CreateTable)
def compile_create_table(create, compiler, **kw):
    table = create.element
    # 获取标准的CREATE TABLE语句
    create_table_sql = compiler.visit_create_table(create)
    # 添加启用RLS的语句
    enable_rls_sql = f"ALTER TABLE {table.name} ENABLE ROW LEVEL SECURITY;"
    # 记录日志
    logger.info(f"自动为表 {table.name} 启用行级安全性")
    # 返回组合的SQL语句 - 注意这里不直接返回组合语句，因为alembic会单独执行它们
    return create_table_sql


# 修改run_migrations_online函数，添加后处理钩子
def process_revision_directives(context, revision, directives):
    if directives and directives[0].upgrade_ops:
        # 遍历所有创建表操作
        for op in directives[0].upgrade_ops.ops:
            if hasattr(op, "table_name") and op.table_name:
                # 为每个新创建的表添加启用RLS的操作
                logger.info(f"将为表 {op.table_name} 添加RLS启用指令")
                # 这里不需要显式添加，因为我们已经修改了CreateTable的编译方法


# 从配置中获取其他需要的值，根据 env.py 的需要定义
# my_important_option = config.get_main_option("my_important_option")
# ... 等等。


# docker中运行，应当连接的是host.docker.internal
# IDE中，执行迁移，应当使用localhost
# 根据运行环境选择不同的服务器地址
def is_running_in_docker() -> bool:
    return os.getenv("RUNINDOCKER", "False").lower() == "true"


def get_url():
    # 获取数据库连接 URL
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "")  # 直接使用环境变量中的服务器地址
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def run_migrations_offline():
    logger.info("数据库迁移: 以'离线'模式运行迁移。")
    logger.info(f"数据库迁移: RUNINDOCKER环境变量值为: {os.getenv('RUNINDOCKER', '')}")
    logger.info(f"数据库迁移: 是否在Docker中运行: {is_running_in_docker()}")
    logger.info(f"数据库迁移: 数据库连接URL为: {get_url()}")
    """以'离线'模式运行迁移。

    这将配置上下文仅包含 URL
    而不是 Engine，尽管在这里也可以接受 Engine。
    通过跳过 Engine 创建，我们甚至不需要 DBAPI 可用。

    在这里对 context.execute() 的调用会将给定的字符串发送到脚本输出。

    """
    # 获取数据库连接 URL
    url = get_url()
    # 配置上下文
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        # 执行迁移
        context.run_migrations()


def run_migrations_online():
    logger.info("数据库迁移: 以'在线'模式运行迁移。")
    logger.info(f"数据库迁移: RUNINDOCKER环境变量值为: {os.getenv('RUNINDOCKER', '')}")
    logger.info(f"数据库迁移: 是否在Docker中运行: {is_running_in_docker()}")
    logger.info(f"数据库迁移: 数据库连接URL为: {get_url()}")
    """以'在线'模式运行迁移。

    在这种情况下，我们需要创建一个 Engine
    并将一个连接与上下文关联起来。

    """
    # 从配置中获取配置项
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    # 创建可连接的 Engine
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # 配置上下文
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            process_revision_directives=process_revision_directives,
        )
        with context.begin_transaction():
            # 执行迁移
            context.run_migrations()


# 检查是否处于离线模式
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
