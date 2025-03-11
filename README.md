# ⚡️ Lightning-FastAPI Backend Starter

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

## Table of Contents

- [Lightning-FastAPI Backend Starter](#%EF%B8%8F-lightning-fastapi-backend-starter)
  - [Introduction](#introduction)
  - [Acknowledgements](#acknowledgements)
  - [Features](#features)
  - [Quick Start](#quick-start-)
  - [Technology Stack](#technology-stack)
  - [Project Structure](#project-structure)
  - [Complete Setup Guide](#complete-setup-guide)
    - [1. Get the Code](#1-get-the-code)
    - [2. Configure Environment Variables](#2-configure-environment-variables)
    - [3. Start the Project with Docker](#3-start-the-project-with-docker)
    - [4. Verify Project Status](#4-verify-project-status)
    - [5. Database Migration (If Needed)](#5-database-migration-if-needed)
    - [6. Initialize New Git Repository (Optional)](#6-initialize-new-git-repository-optional)
  - [Troubleshooting](#troubleshooting)
  - [Development Guide](#development-guide)
    - [Project Structure](#project-structure-1)
    - [API Documentation](#api-documentation)
    - [Dependency Management](#dependency-management)
    - [Custom Development](#custom-development)
  - [Deployment & Customization](#deployment--customization)
    - [Deployment Configuration](#deployment-configuration)
    - [Project Customization](#project-customization)
  - [Error Handling](#error-handling)
    - [Database Migration Issues](#database-migration-issues)
  - [License](#license)

## Introduction

This is a FastAPI-based backend starter project that provides complete user authentication, database integration, and Docker deployment support to help you quickly start new backend project development.

## Acknowledgements

Shoutout to [@liseami](https://github.com/liseami) for the inspiration.

## Features

- ✅ Complete user authentication system (registration, login, JWT tokens)
- ✅ Row-level security (RLS) support
- ✅ SMS verification code functionality
- ✅ Todo list example API
- ✅ Docker containerized deployment
- ✅ Automated database migration
- ✅ Development and production environment configuration
- ✅ Optimized project structure
- ✅ Cursor smart rules (Python FastAPI rule)
- ✅ SQLModel integration with FastAPI
- ✅ Multi-environment support (development, staging, production)
- ✅ Complete CI/CD workflow configuration
- ✅ Global error handling mechanisms
- ✅ Asynchronous database operations
- ✅ API performance optimization guidelines
- ✅ Lifecycle management (lifespan)
- ✅ Automated deployment scripts
- ✅ Fast project creation CLI tool

## Quick Start ⚡

### Method 1: Using Python Package (Simplest)

The easiest way is to install and use our Python command-line tool:

```bash
# Install the tool
pip3 install lightning-fastapi

# Create a new project named "my-backend"
lightning-fastapi my-backend

# Or create interactively without specifying a name
lightning-fastapi
```

This command will:
1. Automatically create a new project directory
2. Clone and configure all necessary files
3. Create a new Git repository
4. Automatically start the project using Docker

> **Note**: The `lightning-fastapi` command is a tool for creating new projects; it will automatically start Docker containers. The created project itself still uses Poetry for dependency management.

### Method 2: One-Click Startup

If you already have Docker and Docker Compose installed, you can use our one-click startup script:

```bash
# Clone the repository
git clone [repository URL] lighting-fastapi
cd lighting-fastapi

# Run the one-click startup script
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

This script will automatically:
1. Check if Docker and Docker Compose are installed
2. Create default environment configuration
3. Start Docker containers with PostgreSQL database
4. Setup and initialize the application

After successful startup, you can access the API documentation in your browser at http://localhost:8000/docs.

## Technology Stack

- **Database Mapping**: [SQLModel](https://sqlmodel.tiangolo.com/)
- **Dependency Management**: [Poetry](https://python-poetry.org/)
- **API Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database Migration**: [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication**: JWT Token
- **Containerization**: Docker & Docker Compose

## Project Structure

The project uses a modular directory structure for easy extension and maintenance:

```
.
├── app/                    # Main application code
│   ├── alembic/            # Database migration configuration
│   ├── api/                # API routes and dependencies
│   ├── core/               # Core configuration
│   ├── crud/               # Database operations
│   ├── models/             # Data models
│   ├── tool/               # Utility functions
│   ├── backend_pre_start.py # Pre-startup checks
│   ├── initial_data.py     # Initial data
│   ├── log_info.py         # Logging utility
│   └── main.py             # Application entry point
├── config/                 # Configuration files directory
│   ├── .env                # Environment variable configuration
│   ├── .env.staging        # Testing environment configuration
│   └── alembic.ini         # Alembic migration configuration
├── docker/                 # Docker-related files
│   ├── Dockerfile          # Application container configuration
│   └── docker-compose.yml  # Container orchestration configuration
├── docs/                   # Documentation directory
│   └── PUBLISH.md          # NPM package publishing guide
├── scripts/                # Scripts directory
│   ├── quickstart.sh       # Quick start script
│   └── start.sh            # Application startup script
├── tools/                  # Development tools
│   ├── create-lighting-fastapi.js # NPX project creation script
│   └── package.json        # NPM package configuration
├── .github/                # GitHub workflow configuration
├── .gitignore              # Git ignore file
├── LICENSE                 # Project license
├── poetry.lock             # Poetry locked dependencies
├── pyproject.toml          # Python project configuration
└── README.md               # Project documentation
```

### Directory Description

- **app/** - Core application code containing all business logic, API routes, and data models
- **config/** - Project configuration files, such as environment variables and database migration settings
- **docker/** - Docker-related files for containerized deployment
- **docs/** - Project documentation directory
- **scripts/** - Automation scripts for deployment, startup, and configuration
- **tools/** - Development tools, such as NPX scripts for quick project creation

## Complete Setup Guide

Here is a complete step-by-step guide to setting up the FastAPI Backend Starter project from scratch. Follow each step in order to quickly build a fully functional backend service.

### 1. Get the Code

```bash
# Clone the repository
git clone [repository URL] lighting-fastapi
cd lighting-fastapi

# Remove existing Git version control (if creating your own project)
rm -rf .git
```

### 2. Configure Environment Variables

Modify the `.env` file in the project root directory, updating the following configurations based on your PostgreSQL setup:

```
# Database configuration - Local development environment
POSTGRES_SERVER=host.docker.internal  # Address for connecting to local database from Docker
# POSTGRES_SERVER=localhost  # Use localhost if not using Docker
POSTGRES_PORT=5432  # PostgreSQL default port
POSTGRES_USER=postgres  # Change to your PostgreSQL username
POSTGRES_PASSWORD=postgres  # Change to your PostgreSQL password
POSTGRES_DB=fastapi_starter  # The database name you created

# Superadmin configuration - Please modify to your own settings
FIRST_SUPERUSER=admin
FIRST_SUPERUSER_PHONE_NUMBER=13800138000
FIRST_SUPERUSER_PASSWORD=admin123

# Whether to open registration
USERS_OPEN_REGISTRATION=True
```

### 3. Start the Project with Docker

Make sure you have Docker and Docker Compose installed, then execute the following commands:

```bash
# Build and start containers
docker compose -f docker/docker-compose-local.yml up -d

# Check running status
docker compose -f docker/docker-compose-local.yml ps
```

> **Note**: First startup requires downloading images and installing dependencies, which may take several minutes. Please be patient.

### 4. Verify Project Status

You can verify if the project is running normally using the following methods:

```bash
# View container logs
docker compose -f docker/docker-compose-local.yml logs -f
```

After successful startup, you will see output similar to the following:

```
app-1  | 🚀 —————————————————— Program started
app-1  | 🌍 Running environment: development
app-1  | 📝 Project name: lightning-fastapi
app-1  | 🔗 API path: /api/v1
app-1  | ✅ —————————————————— Program started
```

Also, opening http://localhost:8000/docs in your browser should display the API documentation interface.

### 5. Database Migration (If Needed)

If you have modified the data models and need to update the database structure, follow these steps:

```bash
# Enter the application container
docker compose -f docker/docker-compose-local.yml exec app bash

# Generate migration script
alembic revision --autogenerate -m "describe your changes"

# Apply migration
alembic upgrade head

# Exit container
exit
```

### 6. Initialize New Git Repository (Optional)

If you plan to use this starter project as the foundation for your own project, you can initialize a new Git repository:

```bash
# Initialize new Git repository
git init

# Add all files
git add .

# Commit initial code
git commit -m "Initialize FastAPI Backend Starter Project"

# Add remote repository (replace with your own GitHub repository address)
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

## Troubleshooting

If the project does not start normally, check the following points:

1. **Port conflicts**:
   - Ensure port 8000 is not occupied by other applications
   - To use another port, modify the port mapping in the `docker/docker-compose-local.yml` file (e.g., "8080:8000")

2. **Docker-related issues**:
   - Ensure Docker and Docker Compose are correctly installed (check using `docker --version` and `docker compose version`)
   - Try rebuilding containers: `docker compose -f docker/docker-compose-local.yml up -d --build --force-recreate`

3. **Permission issues**:
   - On Linux systems, you may need to use `sudo` to run Docker commands

4. **Clear Docker cache** (if encountering strange issues):
   ```bash
   docker compose -f docker/docker-compose-local.yml down
   docker system prune -a
   docker compose -f docker/docker-compose-local.yml up -d
   ```

## Development Guide

### Project Structure

```
app/
├── alembic/              # Database migration configuration
├── api/                  # API routes and dependencies
│   ├── routes/           # API endpoint definitions
│   └── depends.py        # Dependency injection
├── core/                 # Core configuration
│   ├── config.py         # Application configuration
│   ├── db.py             # Database connection
│   └── security.py       # Security-related
├── crud/                 # Database operations
├── models/               # Data models
│   ├── base_models/      # Base models
│   ├── public_models/    # Public models
│   └── table.py          # Table definitions
├── tool/                 # Utility functions
├── backend_pre_start.py  # Pre-startup checks
├── initial_data.py       # Initial data
├── log_info.py           # Logging utility
└── main.py               # Application entry point
```

### API Documentation

After starting the project, access the API documentation:
```
http://localhost:8000/docs
```

### Dependency Management

The project uses Poetry for dependency management, which is independent of the `lightning-fastapi` tool:

- Install project dependencies:
```bash
# Enter your created project directory
cd your-project-name
poetry install
```

- Add new dependencies:
```bash
poetry add [package name]
```

- Remove dependencies:
```bash
poetry remove [package name]
```

- Activate virtual environment:
```bash
poetry shell
```

- Run commands in virtual environment:
```bash
poetry run uvicorn app.main:app --reload
```

> **Tip**: Do not confuse the `lightning-fastapi` command-line tool with the project's own dependency management. The former is a tool for creating new projects, while the latter is the dependency management system for the project itself.

### Custom Development

1. Add new models:
   - Create new base models in `app/models/base_models/`
   - Add table definitions in `app/models/table.py`

2. Add new CRUD operations:
   - Create new CRUD files in `app/crud/`

3. Add new API routes:
   - Create new route files in `app/api/routes/`
   - Register new routes in `app/api/main.py`

## Deployment & Customization

### Deployment Configuration

This project includes complete deployment workflows and configuration files:

1. **Local Development Environment**:
   - `docker/docker-compose-local.yml` - Docker Compose configuration for local development environment

2. **Production/Testing Environment**:
   - `docker/docker-compose.yml` - Docker Compose configuration for production environment
   - `config/.env.staging` - Configuration file for testing environment
   - `scripts/deploy.sh` - Deployment script for deploying and restarting the application on servers

3. **CI/CD Workflow**:
   - `.github/workflows/deploy-staging.yml` - GitHub Actions workflow file for automatic deployment to testing environment

### Project Customization

When using this Starter for your own project, remember to modify the following:

1. **Project Name**:
   - Update `PROJECT_NAME` in the `.env` and `.env.staging` files
   - Update image name and container name in `docker/docker-compose.yml` and `docker/docker-compose-local.yml`
   - Update the following in `scripts/deploy.sh`:
     ```bash
     # Change DEPLOY_DIR=/home/ubuntu/lightning-fastapi to
     DEPLOY_DIR=/home/ubuntu/your-project-name
     
     # Change ARCHIVE_NAME="lightning-fastapi.tar.gz" to
     ARCHIVE_NAME="your-project-name.tar.gz"
     ```

2. **Deployment Path**:
   - Update the `DEPLOY_DIR` variable in `scripts/deploy.sh`
   - Update deployment path in `.github/workflows/deploy-staging.yml`

3. **Database Configuration**:
   - Update database connection information in all environment files

4. **Keys**:
   - Generate a new `SECRET_KEY` for JWT token signing, using the following command:
     ```bash
     openssl rand -base64 32
     ```

5. **Logo and Branding**:
   - Update startup logo and project information in `app/main.py`

## Error Handling

### Database Migration Issues

If you encounter database table not existing errors when starting the application (e.g., `relation "user" does not exist`), you can resolve it using the following steps:

1. Stop all running containers:
```bash
docker compose -f docker/docker-compose-quickstart.yml down
```

2. Run the fix script:
```bash
chmod +x scripts/fix_migration.sh
./scripts/fix_migration.sh
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.