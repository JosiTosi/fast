"""Test configuration and fixtures."""

import pytest
from fast_api.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)
