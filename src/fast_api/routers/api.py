"""Main API endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(tags=["api"])


class Item(BaseModel):
    """Item model."""

    id: int = Field(..., description="Item ID")
    name: str = Field(..., description="Item name", min_length=1, max_length=100)
    description: str | None = Field(None, description="Item description")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ItemCreate(BaseModel):
    """Item creation model."""

    name: str = Field(..., description="Item name", min_length=1, max_length=100)
    description: str | None = Field(None, description="Item description")


# In-memory storage (in a real app, you'd use a database)
items_db: dict[int, Item] = {}
next_id = 1


@router.get("/items", response_model=list[Item])
async def get_items() -> list[Item]:
    """Get all items."""
    return list(items_db.values())


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    """Get item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/items", response_model=Item)
async def create_item(item_data: ItemCreate) -> Item:
    """Create a new item."""
    global next_id

    item = Item(
        id=next_id,
        name=item_data.name,
        description=item_data.description,
    )

    items_db[next_id] = item
    next_id += 1

    return item


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_data: ItemCreate) -> Item:
    """Update an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items_db[item_id]
    item.name = item_data.name
    item.description = item_data.description

    return item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int) -> dict[str, str]:
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"message": "Item deleted successfully"}


@router.get("/example")
async def example_endpoint() -> dict[str, Any]:
    """Example endpoint with various data types."""
    return {
        "message": "This is an example endpoint",
        "timestamp": datetime.utcnow(),
        "data": {
            "numbers": [1, 2, 3, 4, 5],
            "nested": {
                "key": "value",
                "active": True,
            },
        },
    }
