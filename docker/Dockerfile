# Use Python 3.10 slim version as base image | 使用Python 3.10精简版作为基础镜像
FROM python:3.10

# Set working directory to /WORKDIR/ | 设置工作目录为 /WORKDIR/
WORKDIR /WORKDIR/

# Install Poetry package manager | 安装 Poetry 包管理工具
RUN pip install poetry==1.7.1

# Copy project dependency files to container | 复制项目依赖文件到容器中
COPY pyproject.toml /WORKDIR/

# Configure Poetry to not create virtual environments and install dependencies | 配置 Poetry 不创建虚拟环境并安装依赖
RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-interaction --no-ansi

# Copy application code to container | 复制应用程序代码到容器
COPY ./app /WORKDIR/app
# Copy database migration configuration file | 复制数据库迁移配置文件
COPY config/alembic.ini /WORKDIR/
# Copy scripts directory | 复制脚本目录
COPY scripts/ /WORKDIR/scripts/

# Set PYTHONPATH environment variable | 设置 PYTHONPATH 环境变量
ENV PYTHONPATH=/WORKDIR

# Grant execution permissions to startup script | 赋予启动脚本执行权限
RUN chmod +x /WORKDIR/scripts/start.sh
