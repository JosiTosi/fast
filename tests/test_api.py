"""Test API endpoints."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert data["service"] == "fast-api"


def test_readiness_check(client: TestClient) -> None:
    """Test readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "checks" in data


def test_liveness_check(client: TestClient) -> None:
    """Test liveness check endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_get_items_empty(client: TestClient) -> None:
    """Test getting items when empty."""
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client: TestClient) -> None:
    """Test creating an item."""
    item_data = {"name": "Test Item", "description": "A test item"}
    response = client.post("/api/v1/items", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    assert "created_at" in data


def test_get_item(client: TestClient) -> None:
    """Test getting a specific item."""
    # First create an item
    item_data = {"name": "Test Item", "description": "A test item"}
    create_response = client.post("/api/v1/items", json=item_data)
    item_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["id"] == item_id


def test_get_nonexistent_item(client: TestClient) -> None:
    """Test getting a non-existent item."""
    response = client.get("/api/v1/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_item(client: TestClient) -> None:
    """Test updating an item."""
    # First create an item
    item_data = {"name": "Original Item", "description": "Original description"}
    create_response = client.post("/api/v1/items", json=item_data)
    item_id = create_response.json()["id"]

    # Then update it
    updated_data = {"name": "Updated Item", "description": "Updated description"}
    response = client.put(f"/api/v1/items/{item_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]
    assert data["id"] == item_id


def test_delete_item(client: TestClient) -> None:
    """Test deleting an item."""
    # First create an item
    item_data = {"name": "Item to Delete", "description": "Will be deleted"}
    create_response = client.post("/api/v1/items", json=item_data)
    item_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()

    # Verify it's gone
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


def test_example_endpoint(client: TestClient) -> None:
    """Test example endpoint."""
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "timestamp" in data
    assert "data" in data
    assert "numbers" in data["data"]
    assert "nested" in data["data"]
