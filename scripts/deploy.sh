# deploy.sh
#!/bin/bash
# Set automatic exit options, script will immediately stop executing when a command fails or encounters undefined variables | 设置自动退出选项，当命令失败或遇到未定义变量时脚本会立即停止执行
set -euo pipefail

# Deployment directory configuration | 部署目录配置
# Note: Please modify the following variables according to your actual project and server configuration | 注意: 请根据您的实际项目和服务器配置修改以下变量
DEPLOY_DIR=/home/ubuntu/lightning-fastapi
# Archive name | 存档名称
ARCHIVE_NAME="lightning-fastapi.tar.gz"
# Deployment file list | 部署文件列表
DEPLOY_FILES=(
  "app"
  "scripts"
  "docker"
  "config"
  "pyproject.toml"
  "poetry.lock"
)

# Color definitions | 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print colored messages | 打印带颜色的消息
echo_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

echo_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

echo_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

echo_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Display deployment information | 显示部署信息
echo_info "🚀 Starting deployment of Lightning FastAPI project | 开始部署 Lightning FastAPI 项目"
echo_info "📂 Deployment directory: $DEPLOY_DIR | 部署目录: $DEPLOY_DIR"

# Check if target directory exists, create if it doesn't | 检查目标目录是否存在，不存在则创建
if [ ! -d "$DEPLOY_DIR" ]; then
  echo_warning "📁 Deployment directory does not exist, will create directory: $DEPLOY_DIR | 部署目录不存在，将创建目录: $DEPLOY_DIR"
  mkdir -p "$DEPLOY_DIR"
fi

# Create temporary directory for packaging | 创建临时目录用于打包
TEMP_DIR=$(mktemp -d)
echo_info "📁 Creating temporary directory: $TEMP_DIR | 创建临时目录: $TEMP_DIR"

# Copy files needed for deployment to temporary directory | 复制需要部署的文件到临时目录
for file in "${DEPLOY_FILES[@]}"; do
  echo_info "📋 Copying $file to temporary directory | 复制 $file 到临时目录"
  cp -r "$file" "$TEMP_DIR/"
done

# Create compressed package | 创建压缩包
echo_info "🗜️ Creating deployment archive: $ARCHIVE_NAME | 创建部署压缩包: $ARCHIVE_NAME"
tar -czf "$ARCHIVE_NAME" -C "$TEMP_DIR" .

# Transfer archive to server | 将压缩包传输到服务器
echo_info "📤 Transferring archive to server: $ARCHIVE_NAME | 传输压缩包到服务器: $ARCHIVE_NAME"
scp "$ARCHIVE_NAME" ubuntu@api.yourdomain.com:~

# Extract and restart service on server | 在服务器上解压缩并重启服务
echo_info "🔄 Deploying and restarting service on server | 在服务器上部署和重启服务"
ssh ubuntu@api.yourdomain.com << EOF
  set -e
  cd ~
  echo "📂 Extracting deployment package to $DEPLOY_DIR | 解压缩部署包到 $DEPLOY_DIR"
  mkdir -p $DEPLOY_DIR
  tar -xzf $ARCHIVE_NAME -C $DEPLOY_DIR
  
  # Enter deployment directory | 进入部署目录
  cd $DEPLOY_DIR
  
  # Configure environment variables | 配置环境变量
  if [ ! -f ".env.staging" ]; then
    echo "📝 Creating .env.staging file | 创建 .env.staging 文件"
    cp config/.env.staging .env.staging
  fi
  
  # Choose appropriate Docker Compose file based on environment | 根据环境选择合适的Docker Compose文件
  COMPOSE_FILE="docker/docker-compose.yml"
  
  # Restart service | 重启服务
  echo "🔄 Restarting service - using \$COMPOSE_FILE | 重启服务 - 使用 \$COMPOSE_FILE"
  docker compose -f \$COMPOSE_FILE down || true
  docker compose -f \$COMPOSE_FILE build --no-cache
  docker compose -f \$COMPOSE_FILE up -d
  
  # Clean up temporary files | 清理临时文件
  rm -f ~/\$ARCHIVE_NAME
  
  echo "✅ Deployment completed | 部署完成"
EOF

# Clean up local temporary files | 清理本地临时文件
echo_info "🧹 Cleaning up local temporary files | 清理本地临时文件"
rm -rf "$TEMP_DIR"
rm -f "$ARCHIVE_NAME"

echo_success "✅ Deployment process completed | 部署流程完成"
echo_info "🔍 You can login to the server via 'ssh ubuntu@api.yourdomain.com' to check deployment results | 可以通过 'ssh ubuntu@api.yourdomain.com' 登录服务器查看部署结果"