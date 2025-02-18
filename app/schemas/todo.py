from typing import List, Any, Optional
from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class TodoInput(BaseModel):
    title: str = Field(
        None, description="Required title of the todo item", examples=["Watch a movie"]
    )
    completed: bool = Field(
        False, description="Whether the todo item is completed or not"
    )
    # user_id is set to None, and it's defined as Optional
    # because user_id is assigned on the app site not from client
    user_id: Optional[UUID4] = Field(None, description="The authenticated user id")


class TodoOutput(BaseModel):
    id: UUID4
    user_id: UUID4
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class TodoList(BaseModel):
    page: int
    page_size: int
    total_count: int
    todos: List[TodoOutput]
