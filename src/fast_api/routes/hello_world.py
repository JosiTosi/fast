"""
Hello World Router

Provides a simple hello world endpoint for demonstration purposes.
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/hello-world")
def hello_world() -> dict[str, Any]:
    return {"message": "Hello World!", "status": "success", "endpoint": "/hello-world"}
