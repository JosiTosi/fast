"""
Health Check Router

Provides health check endpoints for monitoring and Kubernetes probes.
Includes general health, readiness, and liveness probes.
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ..config import Settings, get_settings

router = APIRouter()


@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    """
    General health check endpoint.

    Returns basic application information and health status.
    Suitable for general monitoring and load balancer health checks.

    Args:
        settings: Application settings

    Returns:
        Dict containing health status and application metadata
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "application": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        },
        "service": "fast-api",
    }


@router.get("/health/ready")
async def readiness_probe(settings: Settings = Depends(get_settings)) -> JSONResponse:
    """
    Kubernetes readiness probe endpoint.

    Indicates whether the application is ready to receive requests.
    This should check dependencies like databases, external services, etc.
    For this demo, we always return ready since there are no external dependencies.

    Args:
        settings: Application settings

    Returns:
        JSONResponse with readiness status
    """
    # In a real application, you would check:
    # - Database connectivity
    # - External service availability
    # - Critical system resources

    ready = True
    status_code = 200 if ready else 503

    response_data = {
        "status": "ready" if ready else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": "ok",  # Would be actual check result
            "external_services": "ok",  # Would be actual check result
        },
    }

    return JSONResponse(
        status_code=status_code,
        content=response_data,
    )


@router.get("/health/live")
async def liveness_probe() -> JSONResponse:
    """
    Kubernetes liveness probe endpoint.

    Indicates whether the application is running and not stuck.
    This should be a lightweight check that doesn't depend on external resources.
    If this fails, Kubernetes will restart the pod.

    Returns:
        JSONResponse with liveness status
    """
    # This should be a very simple check
    # In a real application, you might check:
    # - Application is not deadlocked
    # - Critical threads are running
    # - Memory usage is within limits

    return JSONResponse(
        status_code=200,
        content={
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )
