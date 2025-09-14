# Fast API Application

A professional FastAPI application with modern DevOps practices and production-ready setup.

## Features

- 🚀 FastAPI with async/await support
- 🐍 Python 3.11+ with UV package management
- 🔧 Professional project structure
- 🐳 Docker support (development & production)
- 🧪 Comprehensive test suite with pytest
- 🎯 Code quality tools (ruff, mypy, pre-commit)
- 📦 GitHub Actions CI/CD pipeline
- 🔒 Security scanning with bandit
- 📊 Health checks and monitoring endpoints
- 📖 Auto-generated API documentation

## Quick Start

### Prerequisites

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) package manager
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone git@github.com:JosiTosi/fast.git
   cd fast
   ```

2. **Install UV** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync --all-extras --dev
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   ```

5. **Run the application**
   ```bash
   uv run uvicorn src.fast_api.main:app --reload
   ```

6. **Open your browser**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

### Docker Development

For a containerized development environment:

```bash
# Start development environment
docker-compose up --build

# The API will be available at http://localhost:8000
```

For production-like environment:

```bash
# Start production environment
docker-compose --profile production up --build

# The API will be available at http://localhost:8001
```

## Development

For a detailed step-by-step development workflow, see: **[📋 Developer Workflow Guide](docs/DEVELOPER_WORKFLOW.md)**

### Project Structure

```
├── src/fast_api/          # Application source code
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration management
│   └── routers/          # API route modules
│       ├── __init__.py
│       ├── api.py        # Main API endpoints
│       └── health.py     # Health check endpoints
├── tests/                # Test suite
├── docker/               # Docker configurations
├── .github/workflows/    # GitHub Actions
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

### Available Commands

```bash
# Install dependencies
uv sync --all-extras --dev

# Run the application
uv run uvicorn src.fast_api.main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking
uv run mypy src/

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `APP_NAME`: Application name
- `DEBUG`: Debug mode (true/false)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `ALLOWED_HOSTS`: CORS allowed origins
- `LOG_LEVEL`: Logging level

## API Endpoints

### Health Checks

- `GET /health` - Application health status
- `GET /health/ready` - Kubernetes readiness probe
- `GET /health/live` - Kubernetes liveness probe

### API Endpoints

- `GET /api/v1/` - API information
- **TODO**: Add your custom API endpoints here

## Deployment

### GitHub Actions

The project includes a comprehensive **Modern CI/CD Pipeline** with industry best practices:

1. **🔍 Precommit Checks**: Environment validation and setup
2. **🧹 Code Quality**: Linting, formatting, and type checking
3. **🔨 Build**: Docker image creation with artifact management
4. **🧪 Unit Tests**: Comprehensive testing with 80% coverage enforcement
5. **🔗 Integration Tests**: End-to-end Docker container validation (NEW!)
6. **🔒 Security Scan**: Security vulnerability scanning
7. **🚀 Release**: Production deployment (main branch only)

**📚 For detailed documentation**: See [**CI/CD Pipeline Documentation**](docs/CI-CD-PIPELINE.md)

**Key Features:**
- ⚡ **Parallel execution** of tests for faster feedback
- 📦 **Artifact management** with Docker image sharing
- 🎯 **Coverage threshold** enforcement (80% minimum)
- 🔒 **Production environment** protection
- 🧪 **Integration tests** with real Docker containers

### Docker

Production Docker images are built automatically and pushed to GitHub Container Registry:

```bash
# Pull and run the latest image
docker run -p 8000:8000 ghcr.io/jositosi/fast:latest
```

## Testing

The project includes comprehensive tests:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_api.py

# Run tests in watch mode (install pytest-watch first)
uv add --dev pytest-watch
uv run ptw
```

## Code Quality

The project uses several tools to maintain code quality:

- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker
- **pre-commit**: Git hooks for code quality
- **bandit**: Security linter

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and linting: `uv run pytest && uv run ruff check .`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
