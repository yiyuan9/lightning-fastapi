#!/bin/bash
set -e

# Database initialization | 数据库初始化
python /WORKDIR/app/backend_pre_start.py

# Check if migration files exist | 检查是否存在迁移文件
if [ ! "$(ls -A /WORKDIR/app/alembic/versions/*.py 2>/dev/null)" ]; then
    echo "🔍 No migration files detected, generating... | 未检测到迁移文件，正在生成..."
    # Generate initial migration files | 生成初始迁移文件
    alembic revision --autogenerate -m "initial migration" 
fi

# Apply migrations | 应用迁移
alembic upgrade head

# Initialize data | 初始化数据
python /WORKDIR/app/initial_data.py

# Calculate total worker count | 计算总 worker 数
CORES=$(nproc)
WORKERS_PER_CORE=${WORKERS_PER_CORE:-1}  # If not set, default to 1 | 如果未设置，默认为1
WORKERS=$((CORES * WORKERS_PER_CORE))

# Use logger.info to print core calculation process | 使用 logger.info 打印核心计算过程
python /WORKDIR/app/log_info.py "💻 CPU cores: $CORES | CPU核心数: $CORES"
python /WORKDIR/app/log_info.py "👷 Workers per core: $WORKERS_PER_CORE | 每个核心的worker数: $WORKERS_PER_CORE"
python /WORKDIR/app/log_info.py "👥 Total workers: $WORKERS | 总worker数: $WORKERS"

# Start application | 启动应用
if [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "staging" ]; then
    python /WORKDIR/app/log_info.py "🚀 Starting application in production or staging environment with $WORKERS workers | 在生产或暂存环境中启动应用，使用 $WORKERS 个workers"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers $WORKERS
else
    # Local development mode | 本地开发模式
    python /WORKDIR/app/log_info.py "🛠️ Starting application in development environment with hot reload enabled | 在开发环境中启动应用，启用热重载模式"
    exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi