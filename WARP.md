# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a professional FastAPI application with modern DevOps practices and production-ready setup.

## Repository Information

- **Remote Origin**: `git@github.com:JosiTosi/fast.git`
- **Technology Stack**: FastAPI, Python 3.11+, UV package manager
- **Architecture**: REST API with in-memory storage (no database)
- **Deployment**: Docker containers with GitHub Actions CI/CD

## Common Commands

### Development Setup
```bash
# Quick setup (runs the setup script)
./scripts/dev-setup.sh

# Manual setup
uv sync --all-extras --dev
cp .env.example .env
uv run pre-commit install
```

### Running the Application
```bash
# Start development server with auto-reload
uv run uvicorn src.fast_api.main:app --reload

# Run with Docker (development)
docker-compose up --build

# Run with Docker (production-like)
docker-compose --profile production up --build
```

### Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_api.py

# Run tests in watch mode
uv run ptw
```

### Code Quality
```bash
# Lint and format code
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy src/

# Run all pre-commit hooks
uv run pre-commit run --all-files

# Security scan
uv run bandit -r src/
```

### Docker Commands
```bash
# Build production image
docker build -f docker/Dockerfile -t fast-api .

# Build development image
docker build -f docker/Dockerfile.dev -t fast-api-dev .

# Run production container
docker run -p 8000:8000 fast-api
```

## Architecture Overview

### Project Structure
- **src/fast_api/**: Main application code
  - **main.py**: FastAPI application factory and configuration
  - **config.py**: Pydantic settings management with environment variables
  - **routers/**: API route modules (health checks, main API)
- **tests/**: Comprehensive test suite with fixtures
- **docker/**: Production and development Dockerfiles
- **.github/workflows/**: CI/CD pipeline with testing, security, and deployment

### Key Design Patterns
- **Dependency Injection**: Using FastAPI's dependency system for configuration
- **Router Pattern**: Organized endpoints in separate router modules
- **Factory Pattern**: Application creation through `create_app()` function
- **Settings Management**: Centralized configuration with Pydantic Settings
- **Health Checks**: Kubernetes-ready health, readiness, and liveness probes

### API Structure
- **Health Endpoints**: `/health`, `/health/ready`, `/health/live`
- **API v1**: All business logic under `/api/v1/` prefix
- **CRUD Operations**: Full REST API for items management
- **Error Handling**: Structured HTTP exceptions with proper status codes
- **Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs`

### Development Workflow
1. **Feature Development**: Create feature branches from `main`
2. **Code Quality**: Pre-commit hooks ensure code quality before commits
3. **Testing**: Comprehensive test coverage with pytest
4. **CI/CD**: Automated testing, linting, security scanning, and Docker builds
5. **Deployment**: Production-ready Docker images pushed to GitHub Container Registry

## Important Environment Variables

- `DEBUG`: Enable/disable debug mode and API documentation
- `HOST` / `PORT`: Server binding configuration
- `ALLOWED_HOSTS`: CORS allowed origins
- `LOG_LEVEL`: Application logging level

## Monitoring and Health Checks

The application includes production-ready health endpoints:
- `/health`: General application health with version info
- `/health/ready`: Kubernetes readiness probe
- `/health/live`: Kubernetes liveness probe

All endpoints return structured JSON responses suitable for monitoring systems.
