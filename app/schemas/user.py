from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str
    username: str
    is_superuser: bool = Field(
        False, description="Whether the user has admin privileges"
    )
    is_active: bool = Field(True, description="Whether the user is active")


class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
