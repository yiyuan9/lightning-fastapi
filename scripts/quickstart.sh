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

cleanup_on_error() {
    echo_error "❌ Error occurred during startup, cleaning up... | 启动过程中出现错误，正在清理..."
    docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml down
    exit 1
}

# Catch errors | 捕获错误
trap 'cleanup_on_error' ERR

# Check if Docker is installed | 检查Docker是否已安装
echo_info "🔍 Checking if Docker is installed... | 检查Docker是否已安装..."
if ! command -v docker &> /dev/null; then
    echo_error "❌ Docker is not installed. Please install Docker first: https://docs.docker.com/get-docker/ | Docker未安装，请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed | 检查Docker Compose是否已安装
echo_info "🔍 Checking if Docker Compose is installed... | 检查Docker Compose是否已安装..."
if ! command -v docker compose &> /dev/null; then
    echo_error "❌ Docker Compose is not installed. Please install Docker Compose first: https://docs.docker.com/compose/install/ | Docker Compose未安装，请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check .env file | 检查.env文件
echo_info "📄 Checking environment configuration... | 检查环境配置..."
if [ ! -f .env ]; then
    echo_info "📝 No .env file found, creating default configuration... | 未找到.env文件，创建默认配置..."
    cp config/.env.staging .env
    echo_info "✅ Default environment configuration created | 已创建默认环境配置"
fi

# Clean up previously existing containers | 清理之前可能存在的容器
echo_info "🧹 Cleaning up previously running containers... | 清理之前运行的容器..."
docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml down -v > /dev/null 2>&1 || true

# Ensure migration directory exists | 确保迁移目录存在
if [ ! -d "app/alembic/versions" ]; then
    echo_info "📁 Creating migration version directory... | 创建迁移版本目录..."
    mkdir -p app/alembic/versions
fi

# Start application | 启动应用
echo_info "🚀 Starting FastAPI Starter application (including PostgreSQL database)... | 正在启动FastAPI Starter应用（包含PostgreSQL数据库）..."
docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml up -d --build

# Wait for application to start | 等待应用启动
MAX_RETRIES=10
RETRY_COUNT=0
APP_READY=false

echo_info "⏳ Waiting for application to start... | 等待应用启动..."
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml logs app | grep -q "Application startup complete"; then
        APP_READY=true
        break
    fi
    
    # Check if container exited abnormally | 检查容器是否异常退出
    if ! docker ps | grep -q lightning-fastapi-dev; then
        echo_error "⚠️ Application container has exited, please check logs: | 应用容器已退出，请检查日志:"
        docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml logs app
        cleanup_on_error
    fi
    
    echo_info "⌛ Application is starting, please wait... (${RETRY_COUNT}/${MAX_RETRIES}) | 应用正在启动，请等待... (${RETRY_COUNT}/${MAX_RETRIES})"
    RETRY_COUNT=$((RETRY_COUNT+1))
    sleep 5
done

# Check if application started successfully | 检查应用是否成功启动
if [ "$APP_READY" = true ]; then
    echo_success "✅ Lightning FastAPI application has started successfully! | Lightning FastAPI应用已成功启动!"
    echo ""
    echo -e "${GREEN}=================================${NC}"
    echo -e "🌐 API documentation: ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "👤 Default admin username: ${BLUE}$(grep FIRST_SUPERUSER .env | cut -d= -f2)${NC}"
    echo -e "🔑 Default admin password: ${BLUE}$(grep FIRST_SUPERUSER_PASSWORD .env | cut -d= -f2)${NC}"
    echo -e "${GREEN}=================================${NC}"
    echo ""
    echo_info "📊 Use the following command to view application logs: | 使用以下命令查看应用日志:"
    echo -e "  ${BLUE}docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml logs -f${NC}"
    echo ""
    echo_info "🛑 Use the following command to stop the application: | 使用以下命令停止应用:"
    echo -e "  ${BLUE}docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml down${NC}"
else
    echo_error "❌ Application did not start successfully within the specified time, please check logs: | 应用在规定时间内未成功启动，请检查日志:"
    docker compose -p lightning-fastapi -f docker/docker-compose-quickstart.yml logs app
    cleanup_on_error
fi 