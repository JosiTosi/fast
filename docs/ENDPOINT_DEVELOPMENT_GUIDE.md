# Endpoint Development Guide

This guide provides a step-by-step process for developing new API endpoints in the FastAPI application.

## Overview

The FastAPI application follows a structured approach with:
- **Router-based architecture** for organizing endpoints
- **Dependency injection** for configuration and services
- **Comprehensive testing** with pytest
- **Type hints and validation** with Pydantic
- **Automatic API documentation** with OpenAPI/Swagger

## Step-by-Step Development Process

### Step 1: Plan Your Endpoint

Before coding, define:
- **Purpose**: What does this endpoint do?
- **HTTP Method**: GET, POST, PUT, DELETE, etc.
- **URL Path**: Following REST conventions
- **Request/Response Models**: Data structures
- **Dependencies**: Authentication, database, etc.
- **Error Cases**: What can go wrong?

**Example Planning:**
- Purpose: Manage user tasks
- Method: POST
- Path: `/api/v1/tasks`
- Request: Task creation data
- Response: Created task with ID
- Errors: Validation errors, duplicate tasks

### Step 2: Create Pydantic Models

Create data models for request/response validation in a new or existing models file.

```bash
# Create models directory if it doesn't exist
mkdir -p src/fast_api/models
touch src/fast_api/models/__init__.py
```

**Create model file:** `src/fast_api/models/task.py`

```python
"""
Task Models

Pydantic models for task-related data validation.
"""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreate(BaseModel):
    """Model for task creation request."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    priority: int = Field(default=1, ge=1, le=5, description="Task priority (1-5)")


class Task(BaseModel):
    """Model for task response."""

    id: str = Field(..., description="Unique task ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    priority: int = Field(..., description="Task priority (1-5)")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")


class TaskUpdate(BaseModel):
    """Model for task update request."""

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[int] = Field(None, ge=1, le=5, description="Task priority (1-5)")


class TaskList(BaseModel):
    """Model for task list response."""

    tasks: list[Task] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
```

### Step 3: Create the Router

Create a new router file for your endpoint group.

**Create router file:** `src/fast_api/routes/tasks.py`

```python
"""
Tasks Router

Provides endpoints for task management.
"""

from datetime import datetime
from typing import List, Optional
import uuid

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse

from ..models.task import Task, TaskCreate, TaskUpdate, TaskList, TaskStatus
from ..config import Settings, get_settings

router = APIRouter()

# In-memory storage (replace with database in production)
tasks_db: dict[str, Task] = {}


@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(
    task_data: TaskCreate,
    settings: Settings = Depends(get_settings)
) -> Task:
    """
    Create a new task.

    Args:
        task_data: Task creation data
        settings: Application settings

    Returns:
        Created task

    Raises:
        HTTPException: If task creation fails
    """
    try:
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()

        task = Task(
            id=task_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            created_at=now,
            updated_at=now
        )

        tasks_db[task_id] = task
        return task

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/tasks", response_model=TaskList)
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    settings: Settings = Depends(get_settings)
) -> TaskList:
    """
    Get list of tasks with optional filtering and pagination.

    Args:
        status: Optional status filter
        page: Page number for pagination
        per_page: Number of items per page
        settings: Application settings

    Returns:
        Paginated list of tasks
    """
    # Filter tasks by status if provided
    filtered_tasks = list(tasks_db.values())
    if status:
        filtered_tasks = [task for task in filtered_tasks if task.status == status]

    # Apply pagination
    total = len(filtered_tasks)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_tasks = filtered_tasks[start_idx:end_idx]

    return TaskList(
        tasks=paginated_tasks,
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    settings: Settings = Depends(get_settings)
) -> Task:
    """
    Get a specific task by ID.

    Args:
        task_id: Task unique identifier
        settings: Application settings

    Returns:
        Task details

    Raises:
        HTTPException: If task is not found
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )

    return tasks_db[task_id]


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    settings: Settings = Depends(get_settings)
) -> Task:
    """
    Update an existing task.

    Args:
        task_id: Task unique identifier
        task_update: Task update data
        settings: Application settings

    Returns:
        Updated task

    Raises:
        HTTPException: If task is not found
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )

    task = tasks_db[task_id]

    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    return task


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    settings: Settings = Depends(get_settings)
) -> None:
    """
    Delete a task.

    Args:
        task_id: Task unique identifier
        settings: Application settings

    Raises:
        HTTPException: If task is not found
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )

    del tasks_db[task_id]


@router.get("/tasks/stats/summary")
async def get_task_stats(
    settings: Settings = Depends(get_settings)
) -> dict:
    """
    Get task statistics summary.

    Args:
        settings: Application settings

    Returns:
        Task statistics
    """
    total_tasks = len(tasks_db)

    if total_tasks == 0:
        return {
            "total_tasks": 0,
            "by_status": {},
            "by_priority": {},
            "avg_priority": 0
        }

    # Calculate statistics
    status_counts = {}
    priority_counts = {}
    total_priority = 0

    for task in tasks_db.values():
        # Count by status
        status_counts[task.status] = status_counts.get(task.status, 0) + 1

        # Count by priority
        priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
        total_priority += task.priority

    avg_priority = round(total_priority / total_tasks, 2)

    return {
        "total_tasks": total_tasks,
        "by_status": status_counts,
        "by_priority": priority_counts,
        "avg_priority": avg_priority
    }
```

### Step 4: Register the Router

Add your new router to the main application.

**Update:** `src/fast_api/main.py`

```python
# Add import
from fast_api.routes import health, hello_world, tasks

# Add router registration in create_app()
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
```

**Complete updated main.py example:**
```python
"""
Main FastAPI application module.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from fast_api.config import get_settings
from fast_api.routes import health, hello_world, tasks  # Add tasks import


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    # Startup
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="A professional FastAPI application with modern DevOps practices",
        version="0.1.0",
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Include routers
    app.include_router(health.router, tags=["health"])
    app.include_router(hello_world.router, prefix="/api/v1", tags=["hello-world"])
    app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])  # Add this line
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
```

### Step 5: Write Tests

Create comprehensive tests for your endpoints.

**Create test file:** `tests/test_tasks.py`

```python
"""Test task endpoints."""

from fastapi.testclient import TestClient


def test_create_task(client: TestClient) -> None:
    """Test task creation."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": 3
    }

    response = client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_validation_error(client: TestClient) -> None:
    """Test task creation with invalid data."""
    # Missing required title
    task_data = {
        "description": "Task without title",
        "priority": 3
    }

    response = client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 422


def test_get_tasks_empty(client: TestClient) -> None:
    """Test getting tasks when none exist."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    data = response.json()
    assert data["tasks"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["per_page"] == 10


def test_get_tasks_with_data(client: TestClient) -> None:
    """Test getting tasks with data."""
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": 2
    }

    create_response = client.post("/api/v1/tasks", json=task_data)
    assert create_response.status_code == 201

    # Get tasks
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["total"] == 1
    assert data["tasks"][0]["title"] == task_data["title"]


def test_get_task_by_id(client: TestClient) -> None:
    """Test getting a specific task by ID."""
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": 1
    }

    create_response = client.post("/api/v1/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Get task by ID
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_get_task_not_found(client: TestClient) -> None:
    """Test getting a non-existent task."""
    response = client.get("/api/v1/tasks/non-existent-id")
    assert response.status_code == 404


def test_update_task(client: TestClient) -> None:
    """Test task update."""
    # Create a task first
    task_data = {
        "title": "Original Title",
        "description": "Original description",
        "priority": 1
    }

    create_response = client.post("/api/v1/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Update task
    update_data = {
        "title": "Updated Title",
        "status": "in_progress",
        "priority": 4
    }

    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]
    assert data["priority"] == update_data["priority"]
    # Description should remain unchanged
    assert data["description"] == task_data["description"]


def test_delete_task(client: TestClient) -> None:
    """Test task deletion."""
    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "priority": 2
    }

    create_response = client.post("/api/v1/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Delete task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204

    # Verify task is deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_task_stats(client: TestClient) -> None:
    """Test task statistics endpoint."""
    # Test with no tasks
    response = client.get("/api/v1/tasks/stats/summary")
    assert response.status_code == 200

    data = response.json()
    assert data["total_tasks"] == 0
    assert data["by_status"] == {}
    assert data["avg_priority"] == 0

    # Create some tasks
    tasks = [
        {"title": "Task 1", "priority": 1, "status": "pending"},
        {"title": "Task 2", "priority": 3, "status": "in_progress"},
        {"title": "Task 3", "priority": 5, "status": "completed"},
    ]

    for task in tasks:
        client.post("/api/v1/tasks", json=task)

    # Get stats again
    response = client.get("/api/v1/tasks/stats/summary")
    assert response.status_code == 200

    data = response.json()
    assert data["total_tasks"] == 3
    assert data["avg_priority"] == 3.0  # (1+3+5)/3 = 3
    assert "by_status" in data
    assert "by_priority" in data


def test_filter_tasks_by_status(client: TestClient) -> None:
    """Test filtering tasks by status."""
    # Create tasks with different statuses
    tasks = [
        {"title": "Pending Task", "status": "pending"},
        {"title": "In Progress Task", "status": "in_progress"},
        {"title": "Completed Task", "status": "completed"},
    ]

    for task in tasks:
        client.post("/api/v1/tasks", json=task)

    # Filter by status
    response = client.get("/api/v1/tasks?status=pending")
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["status"] == "pending"


def test_pagination(client: TestClient) -> None:
    """Test task pagination."""
    # Create multiple tasks
    for i in range(15):
        task_data = {
            "title": f"Task {i+1}",
            "priority": (i % 5) + 1
        }
        client.post("/api/v1/tasks", json=task_data)

    # Test first page
    response = client.get("/api/v1/tasks?page=1&per_page=5")
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 5
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["per_page"] == 5

    # Test second page
    response = client.get("/api/v1/tasks?page=2&per_page=5")
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 5
    assert data["page"] == 2
```

### Step 6: Run Tests

Execute the tests to ensure everything works correctly.

```bash
# Run all tests
uv run pytest

# Run only your new tests
uv run pytest tests/test_tasks.py

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run in verbose mode to see individual test results
uv run pytest -v tests/test_tasks.py
```

### Step 7: Test the API Manually

Start the development server and test your endpoints.

```bash
# Start the development server
uv run uvicorn src.fast_api.main:app --reload

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

**Test with curl:**
```bash
# Create a task
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "This is a test task",
    "priority": 3
  }'

# Get all tasks
curl "http://localhost:8000/api/v1/tasks"

# Get task by ID (replace {task_id} with actual ID from creation response)
curl "http://localhost:8000/api/v1/tasks/{task_id}"

# Update a task
curl -X PUT "http://localhost:8000/api/v1/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task Title",
    "status": "in_progress"
  }'

# Delete a task
curl -X DELETE "http://localhost:8000/api/v1/tasks/{task_id}"

# Get task statistics
curl "http://localhost:8000/api/v1/tasks/stats/summary"
```

### Step 8: Code Quality and Documentation

Run code quality checks and ensure proper documentation.

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

### Step 9: Commit Your Changes

Follow the Git workflow to commit your changes.

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat: add task management endpoints

- Add Task models for CRUD operations
- Add tasks router with full CRUD functionality
- Add comprehensive test suite for all endpoints
- Add pagination and filtering capabilities
- Add task statistics endpoint"

# Push to feature branch
git push origin feature/task-endpoints
```

## Best Practices

### 1. **Follow REST Conventions**
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Use plural nouns for resource endpoints (`/tasks`, not `/task`)
- Use hierarchical URLs (`/api/v1/tasks/{id}/comments`)

### 2. **Comprehensive Error Handling**
```python
from fastapi import HTTPException

# Use appropriate status codes
raise HTTPException(status_code=404, detail="Task not found")
raise HTTPException(status_code=400, detail="Invalid task data")
raise HTTPException(status_code=409, detail="Task already exists")
```

### 3. **Input Validation**
- Use Pydantic models for request/response validation
- Set appropriate field constraints (min/max length, ranges)
- Provide clear field descriptions for API documentation

### 4. **Response Models**
- Always define response models
- Use consistent response structures
- Include metadata for lists (pagination, total counts)

### 5. **Testing Strategy**
- Test happy paths and error cases
- Test validation errors
- Test edge cases (empty data, large datasets)
- Use parametrized tests for multiple scenarios

### 6. **Documentation**
- Write comprehensive docstrings
- Use clear parameter descriptions
- Document error responses
- Provide example requests/responses

### 7. **Security Considerations**
- Validate all inputs
- Use HTTPS in production
- Implement rate limiting
- Add authentication/authorization as needed

### 8. **Performance**
- Use async/await for I/O operations
- Implement pagination for large datasets
- Consider caching for expensive operations
- Monitor performance with profiling tools

## Common Patterns and Examples

### Authentication Dependency
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """Validate JWT token and return user."""
    # Validate token logic here
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

# Use in endpoint
@router.get("/protected")
async def protected_endpoint(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

### Database Dependency (if using SQLAlchemy)
```python
from sqlalchemy.orm import Session
from database import get_db

@router.get("/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    """Get tasks from database."""
    tasks = db.query(TaskModel).all()
    return tasks
```

### Background Tasks
```python
from fastapi import BackgroundTasks

def send_notification(email: str, message: str):
    """Send email notification."""
    # Email sending logic
    pass

@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks
):
    """Create task and send notification."""
    task = create_task_in_db(task_data)

    # Send notification in background
    background_tasks.add_task(
        send_notification,
        email="admin@example.com",
        message=f"New task created: {task.title}"
    )

    return task
```

## Next Steps

After successfully implementing your first endpoint:

1. **Add Database Integration**: Replace in-memory storage with a real database
2. **Implement Authentication**: Add JWT-based authentication
3. **Add Rate Limiting**: Protect your API from abuse
4. **Implement Caching**: Add Redis or in-memory caching
5. **Add Monitoring**: Integrate logging and metrics
6. **API Versioning**: Plan for future API versions
7. **Deployment**: Deploy to production environment

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all imports are correct and files exist
2. **Validation Errors**: Check Pydantic model field types and constraints
3. **Test Failures**: Verify test data matches your model requirements
4. **Documentation Not Loading**: Ensure debug mode is enabled for `/docs` access

### Debugging Tips

```python
# Add logging for debugging
import logging

logger = logging.getLogger(__name__)

@router.post("/tasks")
async def create_task(task_data: TaskCreate):
    logger.info(f"Creating task with data: {task_data}")
    # Your code here
    logger.info(f"Task created successfully: {task.id}")
    return task
```

This guide provides a comprehensive foundation for developing robust, well-tested API endpoints in your FastAPI application. Follow these steps and best practices to maintain high code quality and consistent architecture throughout your project.
