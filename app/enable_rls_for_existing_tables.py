"""
为现有表启用行级安全性的脚本
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text, inspect

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_database_url():
    """从环境变量获取数据库连接URL"""
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def enable_rls_for_all_tables():
    """为所有表启用行级安全性"""
    # 获取数据库连接
    db_url = get_database_url()
    if not db_url or "://:@:" in db_url:
        logger.error("无法获取有效的数据库连接URL，请检查环境变量")
        return False

    try:
        # 创建数据库引擎
        engine = create_engine(db_url)

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
                        result = conn.execute(
                            text(
                                f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'"
                            )
                        ).fetchone()

                        if result and not result[0]:  # 如果表存在且未启用RLS
                            logger.info(f"为表 {table} 启用行级安全性")
                            conn.execute(
                                text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
                            )

                            # 创建默认策略
                            try:
                                conn.execute(
                                    text(f"""
                            CREATE POLICY allow_all ON {table}
                                FOR ALL
                                USING (true)
                            """)
                                )
                                logger.info(f"已为表 {table} 创建默认策略")
                            except Exception as policy_error:
                                # 如果策略已存在，会抛出错误，但我们可以忽略它
                                if "already exists" in str(policy_error):
                                    logger.info(
                                        f"表 {table} 的默认策略已存在，跳过创建"
                                    )
                                else:
                                    logger.warning(
                                        f"为表 {table} 创建默认策略时出错: {str(policy_error)}"
                                    )

                            logger.info(f"已为表 {table} 启用行级安全性并处理默认策略")
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
