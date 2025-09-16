"""Test API endpoints."""

from fastapi.testclient import TestClient


# Health Check Tests
def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "application" in data
    assert data["application"]["name"] == "Fast API"
    assert data["application"]["version"] == "1.0.0"
    assert data["service"] == "fast-api"


def test_readiness_check(client: TestClient) -> None:
    """Test readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "external_services" in data["checks"]


def test_liveness_check(client: TestClient) -> None:
    """Test liveness check endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


# TODO: Add your custom API tests here when you implement your endpoints
# Example:
# def test_your_endpoint(client: TestClient) -> None:
#     """Test your custom endpoint."""
#     response = client.get("/api/v1/your-endpoint")
#     assert response.status_code == 200
#     assert "expected_field" in response.json()
