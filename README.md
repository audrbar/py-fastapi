# FastAPI Backend

## 🎯 Overview

This is a modern, production-ready FastAPI backend application that demonstrates best practices for building scalable REST APIs. It features a clean architecture with proper separation of concerns, following the latest SQLAlchemy 2.0 patterns and FastAPI conventions.

The application provides a complete user management system with CRUD operations, showcasing:
- RESTful API design
- Database session management with proper cleanup
- Connection pooling for PostgreSQL
- Docker containerization with multi-stage builds
- Development and production environments
- Comprehensive error handling

## ✨ Features

- **FastAPI Framework** - Modern, fast web framework with automatic API documentation
- **SQLAlchemy 2.0** - Latest ORM patterns with type hints and modern query syntax
- **PostgreSQL Database** - Production-grade relational database
- **Docker Support** - Multi-stage Dockerfile with dev and prod targets
- **Docker Compose** - Easy orchestration of app and database containers
- **Proper Session Management** - Database sessions with guaranteed cleanup
- **Connection Pooling** - Optimized database connection handling
- **Type Safety** - Full type hints using Python 3.12+ features
- **Clean Architecture** - Layered structure (routes → services → models)
- **Environment Configuration** - Pydantic settings with .env support
- **UV Package Manager** - Fast, modern Python package management

## 🏗️ Architecture

The application follows a layered architecture pattern:

```
┌─────────────────────────────────────┐
│     API Layer (Routes/Endpoints)    │
│         app/api/v1/*.py             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Service Layer (Business Logic) │
│         app/services/*.py           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Data Layer (Models/Schema)      │
│    app/db/schema.py, app/models/    │
└─────────────────────────────────────┘
```

**Key Components:**

- **Routes** (`app/api/v1/`): Handle HTTP requests/responses, dependency injection
- **Services** (`app/services/`): Business logic, data manipulation
- **Models** (`app/models/`): Pydantic models for request/response validation
- **Schema** (`app/db/schema.py`): SQLAlchemy ORM models and database configuration
- **Config** (`app/core/config.py`): Application settings and environment variables
- **Logging** (`app/core/logging.py`): Centralized logging configuration

## 🛠️ Technology Stack

- **Python 3.12+** - Modern Python with latest type hint features
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - ORM with modern query patterns
- **PostgreSQL 15** - Production-grade relational database
- **Pydantic v2** - Data validation using Python type hints
- **Uvicorn** - Lightning-fast ASGI server
- **psycopg2** - PostgreSQL adapter for Python
- **Docker** - Containerization platform
- **UV** - Fast Python package manager
- **Alpine Linux** - Minimal Docker base image

## 📁 Project Structure

```
py-fastapi/
├── app/
│   ├── main.py              # Application entry point
│   ├── api/
│   │   └── v1/
│   │       └── user.py      # User endpoints and dependencies
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   └── logging.py       # Logging setup
│   ├── db/
│   │   └── schema.py        # SQLAlchemy models and engine
│   ├── models/
│   │   └── user.py          # Pydantic models
│   └── services/
│       └── user_service.py  # Business logic layer
├── tests/
│   ├── test_db.py
│   └── api/v1/
│       └── test_user.py
├── docker-compose.yaml      # Docker orchestration
├── Dockerfile               # Multi-stage Docker build
├── pyproject.toml          # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example            # Environment template
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- UV package manager (or pip)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <https://github.com/audrbar/py-fastapi>
cd py-fastapi
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Install dependencies**
```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

4. **Start PostgreSQL database**
```bash
docker compose up db -d
```

5. **Run the application**
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### 1️⃣ Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'
```

**Response:**
```json
{"id": 1, "name": "John Doe"}
```

#### 2️⃣ Get All Users
```bash
curl -X GET "http://localhost:8000/api/v1/users"
```

**Response:**
```json
[
  {"id": 1, "name": "John Doe"},
  {"id": 2, "name": "Jane Smith"}
]
```

#### 3️⃣ Get a User by ID
(Replace 1 with the actual ID from the create response)
```bash
curl -X GET "http://localhost:8000/api/v1/users/1"
```

**Response:**
```json
{"id": 1, "name": "John Doe"}
```

#### 4️⃣ Update a User
```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Grace Hopper"}'
```

**Response:**
```json
{"id": 1, "name": "Grace Hopper"}
```

#### 5️⃣ Delete a User
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```

**Response:**
``o`jns
{"success": true}
```

## 💻 Development

### Running Tests
```bash
uv run pytest
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

### Database Migrations
For production use, consider adding Alembic for database migrations:
```bash
uv add alembic
alembic init migrations
```

## 🐳 Docker

### Multi-Stage Dockerfile

The project uses a multi-stage Dockerfile optimized for both development and production:

- **Base Stage**: Sets up Python environment and PostgreSQL libraries
- **Builder Stage**: Installs dependencies with build tools, then removes them
- **Dev Stage**: Includes debugging tools and hot-reload support
- **Prod Stage**: Minimal image with only runtime dependencies

### Build Docker Images

**Development image:**
```bash
docker build -f Dockerfile --target dev -t fastapi-dev .
docker images --filter 'reference=fastapi-dev'
```

**Production image:**
```bash
docker build -f Dockerfile --target prod -t fastapi-prod .
docker images --filter 'reference=fastapi-prod'
```

### Docker Compose

#### Start Development Environment
```bash
docker compose up dev
```

Or in detached mode:
```bash
docker compose up dev -d
```

#### Rebuild and Restart
```bash
docker compose down && docker compose build dev && docker compose up dev
```

#### View Logs
```bash
docker compose logs dev | tail -20
```

#### Stop All Services
```bash
docker compose down
```

#### Stop and Remove Volumes
```bash
docker compose down -v
```

### Services

The `docker-compose.yaml` defines two services:

- **db**: PostgreSQL 15 database
  - Port: 5433 (host) → 5432 (container)
  - Volume: `postgres_data` for data persistence

- **dev**: FastAPI application in development mode
  - Port: 8000
  - Hot-reload enabled
  - Connected to `db` service

**Note:** PostgreSQL runs on port **5433** on the host (mapped from container's 5432) to avoid conflicts with local PostgreSQL installations.

**Local development connection:**
```bash
# If connecting from host machine to Docker PostgreSQL:
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

## 🗄️ Database

### PostgreSQL Configuration

The application uses PostgreSQL with the following connection settings:

**From Docker containers:**
```
postgresql+psycopg2://user:password@db:5432/test_db
```

**From host machine:**
```
postgresql+psycopg2://user:password@localhost:5433/test_db
```

### SQLAlchemy 2.0 Features

This project uses modern SQLAlchemy 2.0 patterns:

- **Declarative Base with Type Hints**: Using `Mapped[]` annotations
- **Modern Query Syntax**: `select()` instead of legacy `.query()`
- **Session Management**: Proper session lifecycle with context managers
- **Connection Pooling**: Configured with `pool_pre_ping` and `pool_recycle`

### Session Management

Database sessions are properly managed with guaranteed cleanup:

```python
def get_db() -> Generator[Session, None, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
```

This ensures:
- Sessions are always closed after use
- No connection leaks
- Proper transaction handling

### Connection Pool Settings

- `pool_size=5`: Maintains 5 persistent connections
- `max_overflow=10`: Allows up to 15 total connections
- `pool_pre_ping=True`: Validates connections before use
- `pool_recycle=3600`: Recycles connections after 1 hour
- `expire_on_commit=False`: Prevents unnecessary lazy loads

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# PostgreSQL Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=test_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# App Configuration
APP_NAME=FastAPIBackend
DEBUG=False
```

### Configuration Management

The application uses Pydantic Settings for configuration:

```python
from app.core.config import config

# Access configuration
db_url = config.db_url
app_name = config.app_name
```

Configuration is automatically loaded from:
1. Environment variables
2. `.env` file
3. Default values in `config.py`

## 📝 License

See LICENSE file for details.

## 👏 Acknowledgments

This project was inspired by best practices from the following resources:

- [**ArjanCodes**: This Is How You Write an Efficient Python Dockerfile](https://www.youtube.com/watch?v=tc713anE3UY)
- [**ArjanCodes**: How To Use Docker To Make Local Development A Breeze](https://www.youtube.com/watch?v=zkMRWDQV4Tg)
- [**Timnology**: Stop Building 2GB Python Containers](https://www.youtube.com/watch?v=Yg0cW-E4tYc)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Happy coding! 🚀**
