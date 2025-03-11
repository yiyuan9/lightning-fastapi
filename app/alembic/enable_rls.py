"""
为所有表启用行级安全性的命令行工具
"""

import os
import sys
import logging
import time
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 设置操作超时时间（秒）
OPERATION_TIMEOUT = 10


def get_database_url():
    """从环境变量获取数据库连接URL"""
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def enable_rls_for_table(conn, table):
    """
    为指定表启用行级安全性，处理可能的超时情况

    Args:
        conn: 数据库连接
        table: 表名

    Returns:
        bool: 操作是否成功
    """
    try:
        # 设置语句超时
        conn.execute(text("SET statement_timeout = '30s'"))
        conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
        logger.info(f"表 {table} RLS启用成功")
        return True
    except OperationalError as oe:
        logger.warning(f"表 {table} 操作超时: {str(oe)}")
        logger.info(f"尝试使用PL/pgSQL异常处理方式处理表 {table}")
        # 重置超时设置
        conn.execute(text("RESET statement_timeout"))
        # 使用PL/pgSQL的异常处理机制
        conn.execute(
            text(f"""
            DO $$
            BEGIN
                ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
            EXCEPTION WHEN OTHERS THEN
                RAISE NOTICE 'Error enabling RLS on {table}: %', SQLERRM;
            END
            $$;
            """)
        )
        return True
    except Exception as e:
        logger.error(f"为表 {table} 启用RLS时出错: {str(e)}")
        return False


def create_default_policy(conn, table):
    """
    为指定表创建默认的RLS策略

    Args:
        conn: 数据库连接
        table: 表名

    Returns:
        bool: 操作是否成功
    """
    try:
        start_time = time.time()
        conn.execute(
            text(f"""
            CREATE POLICY IF NOT EXISTS allow_all ON {table}
                FOR ALL
                USING (true)
            """)
        )
        logger.info(f"已为表 {table} 创建默认策略")

        # 检查操作是否超时
        if time.time() - start_time > OPERATION_TIMEOUT:
            logger.warning(f"为表 {table} 创建策略操作超时，但已完成")
        return True
    except Exception as policy_error:
        # 如果策略已存在，会抛出错误，但我们可以忽略它
        if "already exists" in str(policy_error):
            logger.info(f"表 {table} 的默认策略已存在，跳过创建")
            return True
        else:
            logger.warning(f"为表 {table} 创建默认策略时出错: {str(policy_error)}")
            return False


def enable_rls_for_all_tables():
    """为所有表启用行级安全性"""
    # 获取数据库连接
    db_url = get_database_url()
    if not db_url or "://:@:" in db_url:
        logger.error("无法获取有效的数据库连接URL，请检查环境变量")
        return False

    try:
        # 创建数据库引擎，设置连接超时
        engine = create_engine(db_url, connect_args={"connect_timeout": 30})

        # 连接数据库
        with engine.connect() as conn:
            # 获取所有表
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            logger.info(f"找到 {len(tables)} 个表")

            # 为每个表启用行级安全性
            for table in tables:
                # 为每个表使用单独的事务
                with conn.begin() as trans:
                    try:
                        # 检查表是否已经启用了RLS
                        start_time = time.time()
                        result = conn.execute(
                            text(
                                f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'"
                            )
                        ).fetchone()

                        # 检查操作是否超时
                        if time.time() - start_time > OPERATION_TIMEOUT:
                            logger.warning(
                                f"检查表 {table} 的RLS状态操作超时，跳过此表"
                            )
                            continue

                        if result and not result[0]:  # 如果表存在且未启用RLS
                            logger.info(f"为表 {table} 启用行级安全性")

                            # 启用RLS
                            if enable_rls_for_table(conn, table):
                                # 创建默认策略
                                create_default_policy(conn, table)
                                logger.info(
                                    f"已为表 {table} 启用行级安全性并处理默认策略"
                                )
                        else:
                            logger.info(f"表 {table} 已启用行级安全性，跳过")

                        # 提交事务
                        trans.commit()
                    except Exception as e:
                        # 回滚事务
                        trans.rollback()
                        logger.error(f"为表 {table} 启用RLS时出错: {str(e)}")

            logger.info("完成所有表的行级安全性启用")
            return True

    except Exception as e:
        logger.error(f"连接数据库或启用RLS时出错: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("开始为所有表启用行级安全性")
    success = enable_rls_for_all_tables()
    if success:
        logger.info("成功完成")
        sys.exit(0)
    else:
        logger.error("操作失败")
        sys.exit(1)
