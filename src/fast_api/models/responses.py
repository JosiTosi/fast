"""
Response Models

Pydantic models for API response validation and documentation.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """
    Simple message response model.

    Attributes:
        message: The response message
    """

    message: str = Field(..., description="Response message")


class StatusResponse(BaseModel):
    """
    API status response model.

    Attributes:
        status: Current operational status
        version: API version
        environment: Current environment
        timestamp: Response timestamp
    """

    status: str = Field(..., description="Current operational status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Current environment")
    timestamp: datetime = Field(..., description="Response timestamp")


# Additional response models can be added here as needed
# Example:
# class YourResponse(BaseModel):
#     """Your response model description."""
#     field: str = Field(..., description="Field description")
