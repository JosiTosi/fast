"""Pydantic models for API request/response schemas."""

# from datetime import datetime
# from typing import Optional

# from pydantic import BaseModel, Field


# TODO: Add your Pydantic models here
# Example:
# class UserCreate(BaseModel):
#     """User creation schema."""
#
#     username: str = Field(..., description="Username", min_length=3, max_length=50)
#     email: str = Field(..., description="Email address")
#     password: str = Field(..., description="Password", min_length=8)


# class User(BaseModel):
#     """User response schema."""
#
#     id: int = Field(..., description="User ID")
#     username: str = Field(..., description="Username")
#     email: str = Field(..., description="Email address")
#     created_at: datetime = Field(..., description="Creation timestamp")
#     is_active: bool = Field(default=True, description="User active status")


# class UserUpdate(BaseModel):
#     """User update schema."""
#
#     username: Optional[str] = Field(None, description="Username", min_length=3, max_length=50)
#     email: Optional[str] = Field(None, description="Email address")
#     is_active: Optional[bool] = Field(None, description="User active status")
