from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

# Generic type for the data payload
T = TypeVar("T")


class CommonResponse(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None
