from typing import List, Any, Optional
from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class TodoInput(BaseModel):
    title: str = Field(
        None, description="Required title of the todo item", examples=["Watch a movie"]
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the todo item",
        examples=["Watch a movie at Sunday with friends"],
    )
    completed: bool = Field(
        False, description="Whether the todo item is completed or not"
    )
    # user_id is set to None, and it's defined as Optional
    # because user_id is assigned on the app site not from client
    user_id: Optional[UUID4] = None


class TodoOutput(BaseModel):
    id: UUID4
    user_id: UUID4
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
