from typing import List
from fastapi import APIRouter
from schemas.user import UserResponse
from core.api_client import ApiClient

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def read_users():
    client = ApiClient()
    return client.get("/users")
