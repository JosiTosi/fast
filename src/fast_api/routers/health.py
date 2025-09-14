"""Health check endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from fast_api import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime
    version: str
    service: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=__version__,
        service="fast-api",
    )


@router.get("/health/ready")
async def readiness_check() -> dict[str, Any]:
    """Readiness check endpoint for Kubernetes."""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow(),
        "checks": {
            "application": "ok",
        },
    }


@router.get("/health/live")
async def liveness_check() -> dict[str, str]:
    """Liveness check endpoint for Kubernetes."""
    return {"status": "alive"}
