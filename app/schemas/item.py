from typing import List, Any
from datetime import datetime

from pydantic import BaseModel, UUID4


class ItemInput(BaseModel):
    name: str
    description: str


class ItemResponse(BaseModel):
    id: UUID4
    name: str
    description: str


class ItemOutput(BaseModel):
    id: UUID4
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class ItemList(BaseModel):
    page: int
    page_size: int
    items: List[Any]
