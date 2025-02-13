from pydantic import BaseModel, UUID4


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(BaseModel):
    id: UUID4
    name: str
    description: str
