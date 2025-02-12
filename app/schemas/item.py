from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
