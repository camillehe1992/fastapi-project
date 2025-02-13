from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: object
    phone: str
    website: str
    company: object
