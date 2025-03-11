#!/bin/bash
set -e

# Color definitions | 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Print colored messages | 打印带颜色的消息
echo_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

echo_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Print welcome message | 打印欢迎信息
echo -e "${GREEN}⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️${NC}"
echo -e "${GREEN}  ______         _              _____  _____${NC}"
echo -e "${GREEN} |  ____|       | |       /\\   |  __ \\|_   _|${NC}"
echo -e "${GREEN} | |__ __ _  ___| |_     /  \\  | |__) | | |  ${NC}"
echo -e "${GREEN} |  __/ _\` |/ __| __|   / /\\ \\ |  ___/  | |  ${NC}"
echo -e "${GREEN} | | | (_| |\\__ \\ |_   / ____ \\| |     _| |_ ${NC}"
echo -e "${GREEN} |_|  \\__,_||___/\\__| /_/    \\_\\_|    |_____|${NC}"
echo -e "${GREEN}                                       By JY ${NC}"
echo -e "${GREEN}                           One-click migration fix | 一键修复迁移脚本                                   ${NC}"
echo -e "${GREEN}⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️${NC}"
echo ""

echo_info "🔧 This script is used to fix database migration issues. | 这个脚本用于修复数据库迁移问题。"
echo_warn "⚠️ Make sure all containers are stopped before running this script. | 确保在运行此脚本之前已经停止了所有容器。"
echo ""

read -p "Do you want to continue fixing the database? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo_info "❌ Operation cancelled | 操作已取消"
    exit 0
fi

# Check if Docker is installed | 检查Docker是否已安装
echo_info "🔍 Checking if Docker is installed... | 检查Docker是否已安装..."
if ! command -v docker &> /dev/null; then
    echo_error "❌ Docker is not installed. Please install Docker first: https://docs.docker.com/get-docker/ | Docker未安装，请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Stop all containers | 停止所有容器
echo_info "🛑 Stopping all existing containers... | 停止所有现有容器..."
docker compose -f docker/docker-compose-quickstart.yml down -v || true

# Ensure migration directory exists | 确保迁移目录存在
if [ ! -d "app/alembic/versions" ]; then
    echo_info "📁 Creating migration version directory... | 创建迁移版本目录..."
    mkdir -p app/alembic/versions
fi

# Delete existing migration files (if any) | 删除现有迁移文件（如果有）
echo_info "🗑️ Deleting existing migration files... | 删除现有迁移文件..."
rm -f app/alembic/versions/*.py

# Start temporary database container | 启动临时数据库容器
echo_info "🐳 Starting database container... | 启动数据库容器..."
docker compose -f docker/docker-compose-quickstart.yml up -d db

# Wait for database to start | 等待数据库启动
echo_info "⏳ Waiting for database to start... | 等待数据库启动..."
sleep 10

# Build application image | 构建应用镜像
echo_info "🏗️ Building application image... | 构建应用镜像..."
docker compose -f docker/docker-compose-quickstart.yml build app

# Generate migration files | 生成迁移文件
echo_info "📝 Generating migration files... | 正在生成迁移文件..."

# Get database name from environment variables, use default if not set | 获取环境变量中的数据库名称，如果未设置则使用默认值
if [ -f .env ] && grep -q "POSTGRES_DB=" .env; then
  DB_NAME=$(grep "POSTGRES_DB=" .env | cut -d= -f2)
else
  DB_NAME="fastapi_starter"
fi

echo_info "🗄️ Using database: ${DB_NAME} | 使用数据库: ${DB_NAME}"

docker run --rm --network=docker_default \
  -v $(pwd)/app:/WORKDIR/app \
  -e POSTGRES_SERVER=db \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=${DB_NAME} \
  -e ENVIRONMENT=dev \
  -e RUNINDOCKER=True \
  fastapi-starter-dev:latest \
  alembic -c /WORKDIR/alembic.ini revision --autogenerate -m "repair migration"

# Check if migration files were generated | 检查迁移文件是否生成
if [ -z "$(ls -A app/alembic/versions/*.py 2>/dev/null)" ]; then
    echo_error "❌ Failed to create migration files | 迁移文件创建失败"
    docker compose -f docker/docker-compose-quickstart.yml down -v
    exit 1
else
    echo_success "✅ Migration files successfully generated | 迁移文件已成功生成"
fi

# Apply migrations and initialize database | 应用迁移并初始化数据库
echo_info "🔄 Applying migrations and initializing database... | 应用迁移并初始化数据库..."
docker run --rm --network=docker_default \
  -v $(pwd)/app:/WORKDIR/app \
  -e POSTGRES_SERVER=db \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=${DB_NAME} \
  -e ENVIRONMENT=dev \
  -e RUNINDOCKER=True \
  fastapi-starter-dev:latest \
  alembic -c /WORKDIR/alembic.ini upgrade head

echo_success "✅ Database migration and repair completed | 数据库迁移和修复完成"

# Start full application | 启动完整应用
echo_info "🚀 Starting full application... | 启动完整应用..."
docker compose -f docker/docker-compose-quickstart.yml up -d

echo_success "✅ Application started, please use the following command to view logs: | 应用已启动，请使用以下命令查看日志："
echo_info "📊 docker compose -f docker/docker-compose-quickstart.yml logs -f" 