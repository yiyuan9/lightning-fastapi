# ⚡️ Lightning-FastAPI 后端 Starter

[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![中文](https://img.shields.io/badge/语言-中文-red)](README.zh-CN.md)

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│▗    ▝      ▐    ▗       ▝              ▗▄▄▖         ▗   ▗▖ ▗▄▄ ▗▄▄ │
│▐   ▗▄   ▄▄ ▐▗▖ ▗▟▄ ▗▗▖ ▗▄  ▗▗▖  ▄▄     ▐    ▄▖  ▄▖ ▗▟▄  ▐▌ ▐ ▝▌ ▐  │
│▐    ▐  ▐▘▜ ▐▘▐  ▐  ▐▘▐  ▐  ▐▘▐ ▐▘▜     ▐▄▄▖▝ ▐ ▐ ▝  ▐   ▌▐ ▐▄▟▘ ▐  │
│▐    ▐  ▐ ▐ ▐ ▐  ▐  ▐ ▐  ▐  ▐ ▐ ▐ ▐     ▐   ▗▀▜  ▀▚  ▐   ▙▟ ▐    ▐  │
│▐▄▄▖▗▟▄ ▝▙▜ ▐ ▐  ▝▄ ▐ ▐ ▗▟▄ ▐ ▐ ▝▙▜     ▐   ▝▄▜ ▝▄▞  ▝▄ ▐  ▌▐   ▗▟▄ │
│         ▖▐                      ▖▐                                 │
│         ▝▘                      ▝▘                                 │
└────────────────────────────────────────────────────────────────────┘
                                                               ⚡️ By JY
```

## 目录

- [FastAPI 后端 Starter](#fastapi-后端-starter)
  - [项目简介](#项目简介)
  - [致谢](#致谢)
  - [特性](#特性)
  - [快速开始](#快速开始-)
  - [技术栈](#技术栈)
  - [项目结构](#项目结构)
  - [目录](#目录)
  - [完整设置指南](#完整设置指南)
    - [1. 获取代码](#1-获取代码)
    - [2. 配置环境变量](#2-配置环境变量)
    - [3. 使用Docker启动项目](#3-使用docker启动项目)
    - [4. 验证项目运行状态](#4-验证项目运行状态)
    - [5. 数据库迁移（如需修改模型）](#5-数据库迁移如需修改模型)
    - [6. 初始化新的Git仓库（可选）](#6-初始化新的git仓库可选)
  - [常见问题排查](#常见问题排查)
  - [开发指南](#开发指南)
    - [项目结构](#项目结构-1)
    - [API 文档](#api-文档)
    - [依赖管理](#依赖管理)
    - [自定义开发](#自定义开发)
  - [部署与定制](#部署与定制)
    - [部署配置](#部署配置)
    - [项目定制](#项目定制)
  - [故障排除](#故障排除)
    - [数据库迁移问题](#数据库迁移问题)
  - [许可](#许可)

## 项目简介

这是一个基于 FastAPI 的后端 Starter 项目，提供了完整的用户认证、数据库集成和 Docker 部署支持，帮助你快速启动新的后端项目开发。

## 致谢

特别感谢 [@liseami](https://github.com/liseami)

## 特性

- ✅ 完整的用户认证系统（注册、登录、JWT令牌）
- ✅ 行级安全 (RLS) 支持
- ✅ 短信验证码功能
- ✅ 待办事项示例API
- ✅ Docker 容器化部署
- ✅ 自动化数据库迁移
- ✅ 开发和生产环境配置
- ✅ 优化的项目结构
- ✅ Cursor智能规则（Python FastAPI规则）
- ✅ SQLModel与FastAPI集成
- ✅ 多环境支持（开发、测试、生产）
- ✅ 完整的CI/CD工作流配置
- ✅ 全球化错误处理机制
- ✅ 异步数据库操作支持
- ✅ API性能优化建议
- ✅ 生命周期管理（lifespan）
- ✅ 自动化部署脚本
- ✅ 快速创建项目CLI工具

## 快速开始 ⚡

### 方法1: 使用Python包创建项目（最简单）

最简单的方式是通过pip安装和使用我们的Python命令行工具：

```bash
# 安装工具
pip3 install lightning-fastapi

# 创建一个名为"my-backend"的新项目
lightning-fastapi my-backend

# 或者不指定名称，交互式创建
lightning-fastapi
```

这个命令会：
1. 自动创建一个新的项目目录
2. 克隆并配置好所有必要的文件
3. 创建一个新的Git仓库
4. 自动使用Docker启动项目

> **注意**：`lightning-fastapi` 命令是用来创建新项目的工具，它会自动启动Docker容器。创建后的项目本身仍然使用Poetry进行依赖管理。

### 方法2: 一键启动

如果你已经安装了Docker和Docker Compose，你可以使用我们的一键启动脚本：

```bash
# 克隆仓库
git clone [仓库URL] lighting-fastapi
cd lighting-fastapi

# 运行一键启动脚本
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

这个脚本会自动：
1. 检查Docker和Docker Compose是否已安装
2. 创建默认环境配置
3. 启动包含PostgreSQL数据库的Docker容器
4. 设置和初始化应用

启动成功后，你可以在浏览器中访问 http://localhost:8000/docs 查看API文档。

## 技术栈

- **数据库映射**: [SQLModel](https://sqlmodel.tiangolo.com/)
- **依赖管理**: [Poetry](https://python-poetry.org/)
- **API 框架**: [FastAPI](https://fastapi.tiangolo.com/)
- **数据库迁移**: [Alembic](https://alembic.sqlalchemy.org/)
- **认证**: JWT Token
- **容器化**: Docker & Docker Compose

## 项目结构

项目采用模块化的目录结构，便于扩展和维护：

```
.
├── app/                    # 主应用代码
│   ├── alembic/            # 数据库迁移配置
│   ├── api/                # API路由和依赖
│   ├── core/               # 核心配置
│   ├── crud/               # 数据库操作
│   ├── models/             # 数据模型
│   ├── tool/               # 工具函数
│   ├── backend_pre_start.py # 启动前检查
│   ├── initial_data.py     # 初始数据
│   ├── log_info.py         # 日志工具
│   └── main.py             # 应用入口
├── config/                 # 配置文件目录
│   ├── .env                # 环境变量配置
│   ├── .env.staging        # 测试环境配置
│   └── alembic.ini         # Alembic迁移配置
├── docker/                 # Docker相关文件
│   ├── Dockerfile          # 应用容器配置
│   └── docker-compose.yml  # 容器编排配置
├── docs/                   # 文档目录
│   └── PUBLISH.md          # NPM包发布指南
├── scripts/                # 脚本目录
│   ├── quickstart.sh       # 快速启动脚本
│   └── start.sh            # 应用启动脚本
├── tools/                  # 开发工具
│   ├── create-lighting-fastapi.js # NPX创建项目脚本
│   └── package.json        # NPM包配置
├── .github/                # GitHub工作流配置
├── .gitignore              # Git忽略文件
├── LICENSE                 # 项目许可证
├── poetry.lock             # Poetry锁定依赖
├── pyproject.toml          # Python项目配置
└── README.md               # 项目说明文档
```

### 目录说明

- **app/** - 核心应用代码，包含所有业务逻辑、API路由和数据模型
- **config/** - 存放项目配置文件，如环境变量和数据库迁移配置
- **docker/** - Docker相关文件，用于容器化部署应用
- **docs/** - 项目文档目录
- **scripts/** - 自动化脚本，用于部署、启动和配置项目
- **tools/** - 开发工具，如NPX脚本用于快速创建项目

## 完整设置指南

以下是从零开始设置FastAPI后端Starter项目的完整步骤。按照顺序执行每一步，即可快速搭建起一个功能完整的后端服务。

### 1. 获取代码

```bash
# 克隆仓库
git clone [仓库URL] lighting-fastapi
cd lighting-fastapi

# 移除现有Git版本控制（如果要创建自己的项目）
rm -rf .git
```

### 2. 配置环境变量

修改项目根目录中的`.env`文件，根据您的PostgreSQL设置更新以下配置：

```
# 数据库配置 - 本地开发环境
POSTGRES_SERVER=host.docker.internal  # Docker中连接本地数据库的地址
# POSTGRES_SERVER=localhost  # 如果不使用Docker，可改为localhost
POSTGRES_PORT=5432  # PostgreSQL默认端口
POSTGRES_USER=postgres  # 更改为您的PostgreSQL用户名
POSTGRES_PASSWORD=postgres  # 更改为您的PostgreSQL密码
POSTGRES_DB=fastapi_starter  # 您创建的数据库名称

# 超级管理员配置 - 请修改为您自己的设置
FIRST_SUPERUSER=admin
FIRST_SUPERUSER_PHONE_NUMBER=13800138000
FIRST_SUPERUSER_PASSWORD=admin123

# 是否开放注册
USERS_OPEN_REGISTRATION=True
```

### 3. 使用Docker启动项目

确保您已经安装了Docker和Docker Compose，然后执行以下命令：

```bash
# 构建并启动容器
docker compose -f docker/docker-compose-local.yml up -d

# 查看运行状态
docker compose -f docker/docker-compose-local.yml ps
```

> **注意**：首次启动需要下载镜像和安装依赖，可能需要几分钟的时间。请耐心等待。

### 4. 验证项目运行状态

可以通过以下方式验证项目是否正常运行：

```bash
# 查看容器日志
docker compose -f docker/docker-compose-local.yml logs -f
```

成功启动后，您将看到类似以下的输出信息：

```
app-1  | 🚀 —————————————————— 程序启动
app-1  | 🌍 运行环境: development
app-1  | 📝 项目名称: lightning-fastapi
app-1  | 🔗 API路径: /api/v1
app-1  | ✅ —————————————————— 程序启动
```

同时，打开浏览器访问 http://localhost:8000/docs 应该能看到API文档界面。

### 5. 数据库迁移（如需修改模型）

如果您修改了数据模型并需要更新数据库结构，请执行以下步骤：

```bash
# 进入应用容器
docker compose -f docker/docker-compose-local.yml exec app bash

# 生成迁移脚本
alembic revision --autogenerate -m "描述您的变更"

# 应用迁移
alembic upgrade head

# 退出容器
exit
```

### 6. 初始化新的Git仓库（可选）

如果您打算将这个starter项目作为您自己项目的起点，可以初始化一个新的Git仓库：

```bash
# 初始化新的Git仓库
git init

# 添加所有文件
git add .

# 提交初始代码
git commit -m "初始化FastAPI后端Starter项目"

# 添加远程仓库（替换为您自己的GitHub仓库地址）
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

## 常见问题排查

如果项目未能正常启动，请检查以下几点：

1. **端口冲突**：
   - 确保端口8000没有被其他应用占用
   - 如需使用其他端口，修改`docker/docker-compose-local.yml`文件中的端口映射（例如 "8080:8000"）

2. **Docker相关问题**：
   - 确保Docker和Docker Compose已正确安装（运行`docker --version`和`docker compose version`检查）
   - 尝试重建容器：`docker compose -f docker/docker-compose-local.yml up -d --build --force-recreate`

3. **权限问题**：
   - 在Linux系统上，可能需要使用`sudo`来运行Docker命令

4. **清理Docker缓存**（如果遇到奇怪的问题）：
   ```bash
   docker compose -f docker/docker-compose-local.yml down
   docker system prune -a
   docker compose -f docker/docker-compose-local.yml up -d
   ```

## 开发指南

### 项目结构

```
app/
├── alembic/              # 数据库迁移配置
├── api/                  # API路由和依赖
│   ├── routes/           # API端点定义
│   └── depends.py        # 依赖注入
├── core/                 # 核心配置
│   ├── config.py         # 应用配置
│   ├── db.py             # 数据库连接
│   └── security.py       # 安全相关
├── crud/                 # 数据库操作
├── models/               # 数据模型
│   ├── base_models/      # 基础模型
│   ├── public_models/    # 公共模型
│   └── table.py          # 表定义
├── tool/                 # 工具函数
├── backend_pre_start.py  # 启动前检查
├── initial_data.py       # 初始数据
├── log_info.py           # 日志工具
└── main.py               # 应用入口
```

### API 文档

启动项目后，访问 API 文档：
```
http://localhost:8000/docs
```

### 依赖管理

项目使用Poetry进行依赖管理，这是独立于`lightning-fastapi`工具的：

- 安装项目依赖：
```bash
# 进入已创建的项目目录
cd your-project-name
poetry install
```

- 添加新依赖：
```bash
poetry add [包名]
```

- 删除依赖：
```bash
poetry remove [包名]
```

- 激活虚拟环境：
```bash
poetry shell
```

- 使用虚拟环境运行命令：
```bash
poetry run uvicorn app.main:app --reload
```

> **提示**：请勿混淆`lightning-fastapi`命令行工具与项目本身的依赖管理。前者是用于创建新项目的工具，后者是项目自身运行所需的依赖管理系统。

### 自定义开发

1. 添加新的模型：
   - 在 `app/models/base_models/` 创建新的基础模型
   - 在 `app/models/table.py` 添加表定义

2. 添加新的CRUD操作：
   - 在 `app/crud/` 创建新的CRUD文件

3. 添加新的API路由：
   - 在 `app/api/routes/` 创建新的路由文件
   - 在 `app/api/main.py` 注册新路由

## 部署与定制

### 部署配置

本项目包含完整的部署工作流和配置文件：

1. **本地开发环境**：
   - `docker/docker-compose-local.yml` - 用于本地开发环境的Docker Compose配置

2. **生产/测试环境**：
   - `docker/docker-compose.yml` - 用于生产环境的Docker Compose配置
   - `config/.env.staging` - 测试环境的配置文件
   - `scripts/deploy.sh` - 部署脚本，用于在服务器上部署和重启应用

3. **CI/CD 工作流**：
   - `.github/workflows/deploy-staging.yml` - GitHub Actions工作流文件，用于自动部署到测试环境

### 项目定制

将此Starter用于您自己的项目时，请记得修改以下内容：

1. **项目名称**：
   - 在`.env`和`.env.staging`文件中更新`PROJECT_NAME`
   - 在`docker/docker-compose.yml`和`docker/docker-compose-local.yml`中更新镜像名称和容器名称
   - 在`scripts/deploy.sh`中更新以下内容:
     ```bash
     # 将 DEPLOY_DIR=/home/ubuntu/lightning-fastapi 修改为
     DEPLOY_DIR=/home/ubuntu/your-project-name
     
     # 将 ARCHIVE_NAME="lightning-fastapi.tar.gz" 修改为
     ARCHIVE_NAME="your-project-name.tar.gz"
     ```

2. **部署路径**：
   - 在`scripts/deploy.sh`中更新`DEPLOY_DIR`变量
   - 在`.github/workflows/deploy-staging.yml`中更新部署路径

3. **数据库配置**：
   - 更新所有环境文件中的数据库连接信息

4. **密钥**：
   - 生成新的`SECRET_KEY`用于JWT令牌签名，可以使用以下命令：
     ```bash
     openssl rand -base64 32
     ```

5. **Logo和品牌**：
   - 在`app/main.py`中更新启动logo和项目信息

## 故障排除

### 数据库迁移问题

如果您在启动应用时遇到数据库表不存在的问题（例如 `relation "user" does not exist`），可以使用以下步骤解决：

1. 停止所有正在运行的容器：
```bash
docker compose -f docker/docker-compose-quickstart.yml down
```

2. 运行修复脚本：
```bash
chmod +x scripts/fix_migration.sh
./scripts/fix_migration.sh
```

## 致谢

特别感谢 [@liseami](https://github.com/liseami) 提供的灵感。

## 许可

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。
