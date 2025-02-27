from typing import Optional

from pydantic import BaseModel, UUID4, Field


class UserBase(BaseModel):
    email: str = Field(examples=["john.doe@example.com"])
    username: str = Field(examples=["John Doe"])
    is_superuser: bool = Field(
        False, description="Whether the user has admin privileges"
    )
    is_active: bool = Field(True, description="Whether the user is active")


class UserRegister(BaseModel):
    email: str = Field(examples=["john.doe@example.com"])
    username: str = Field(examples=["John Doe"])
    password: str = Field(examples=["Password@123"])


class UserLogin(BaseModel):
    email: str = Field(examples=["john.doe@example.com"])
    password: str = Field(examples=["Password@123"])


class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: UUID4

    class ConfigDict:
        from_attributes = True


class UserInDB(UserInDBBase):
    hashed_password: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    expired_at: str
