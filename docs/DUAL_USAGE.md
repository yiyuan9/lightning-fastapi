# FastAPI Starter Dual Usage Methods | FastAPI Starter 双重使用方式

This project supports two different but complementary usage methods. Understanding the difference between these two is important for correct usage. | 本项目支持两种不同但互补的使用方式，理解这两者的区别对于正确使用非常重要。

## 1. fastapi-starter Command Line Tool | 1. fastapi-starter 命令行工具

**Purpose**: Quickly create new FastAPI projects | **目的**：快速创建新的FastAPI项目

**Usage**: | **使用方式**：
```bash
# Install globally via pip | 通过pip全局安装
pip install fastapi-starter

# Create new project | 创建新项目
fastapi-starter my-new-project
```

**How it works**: | **工作原理**：
- This tool is a Python package, using the code in the `src/fastapi_starter/` directory | 这个工具是一个Python包，使用`src/fastapi_starter/`目录中的代码
- It clones the project repository to the specified directory | 它会克隆项目仓库到指定目录
- Sets up a new Git repository | 设置新的Git仓库
- Provides interactive startup options | 提供交互式启动选项

**Suitable scenarios**: | **适用场景**：
- When you need to quickly start a new project from scratch | 当你需要快速从头开始一个新项目时
- Similar to other frameworks' "scaffolding" tools | 类似于其他框架的"脚手架"工具

## 2. Poetry Dependency Management of the Project Itself | 2. 项目本身的Poetry依赖管理

**Purpose**: Manage dependencies and development environment for already created projects | **目的**：管理已创建项目的依赖和开发环境

**Usage**: | **使用方式**：
```bash
# In the project directory | 在项目目录中
poetry install
poetry shell
poetry run uvicorn app.main:app --reload
```

**How it works**: | **工作原理**：
- Uses the [tool.poetry] section in pyproject.toml | 使用pyproject.toml中的[tool.poetry]部分
- Manages dependencies for the FastAPI application in the app directory | 管理app目录中FastAPI应用的依赖
- Handles dependency relationships for development, testing, and production environments | 处理开发、测试和生产环境的依赖关系

**Suitable scenarios**: | **适用场景**：
- Daily development after you have already created the project | 当你已经创建了项目后的日常开发
- Running projects in different environments (development, testing, production) | 在不同环境（开发、测试、生产）中运行项目
- When you need to add new dependencies or update existing ones | 当需要添加新依赖或更新现有依赖时

## How They Work Together | 如何协同工作

These two methods complement each other perfectly: | 这两种方式完美互补：

1. **Create a new project**: Use the `fastapi-starter` command line tool | **创建新项目**：使用`fastapi-starter`命令行工具
2. **Develop the project**: Use Poetry configuration within the project | **开发项目**：使用项目内的Poetry配置

The pyproject.toml file contains two parts of configuration: | pyproject.toml文件包含了两部分配置：
- `[project]` section: For packaging and distribution of the command line tool | `[project]`部分：用于命令行工具的打包和分发
- `[tool.poetry]` section: For dependency management of the created project | `[tool.poetry]`部分：用于创建后项目的依赖管理

## Notes | 注意事项

- Don't confuse the `fastapi-starter` command with Poetry dependencies of the project | 不要混淆`fastapi-starter`命令与项目的Poetry依赖
- `fastapi-starter` requires fewer dependencies (such as inquirer) | `fastapi-starter`仅需要较少的依赖（如inquirer）
- The project itself needs more dependencies (FastAPI, SQLModel, etc.) | 项目本身需要较多的依赖（FastAPI, SQLModel等）
- After modifying the project template, please commit changes using Git, so `fastapi-starter` will clone the latest template | 修改项目模板后，请使用Git提交变更，这样`fastapi-starter`会克隆最新的模板 