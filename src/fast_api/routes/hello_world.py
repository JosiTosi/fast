"""
Hello World Router

Provides a simple hello world endpoint for demonstration purposes.
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/hello-world")
def hello_world() -> dict[str, Any]:
    """
    Simple hello world endpoint.

    Returns:
        Dict containing a hello world message
    """
    return {"message": "Hello World!", "status": "success", "endpoint": "/hello-world"}
