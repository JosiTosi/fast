"""Test API endpoints."""

from fastapi.testclient import TestClient


# Health Check Tests (keep these)
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


def test_api_info(client: TestClient) -> None:
    """Test API info endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "API v1 is running"
    assert "version" in data
    assert "status" in data


# TODO: Add your API tests here
# Example:
# def test_your_endpoint(client: TestClient) -> None:
#     """Test your endpoint."""
#     response = client.get("/api/v1/your-endpoint")
#     assert response.status_code == 200
#     assert "expected_field" in response.json()
