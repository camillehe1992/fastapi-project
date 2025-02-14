from uuid import UUID
from typing import List, Any, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class TodoInput(BaseModel):
    title: str
    description: Optional[str] = Field(
        None, description="Optional description of the todo item"
    )
    completed: bool = Field(
        False, description="Whether the todo item is completed or not"
    )


class TodoOutput(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = Field(
        None, description="Optional description of the todo item"
    )
    completed: bool = Field(
        False, description="Whether the todo item is completed or not"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="The time the todo item was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="The time the todo item was last updated",
    )

    class Config:
        from_attributes = True


class TodoList(BaseModel):
    page: int
    page_size: int
    todos: List[Any]
