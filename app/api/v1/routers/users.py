from fastapi import APIRouter
from core.api_client import ApiClient

router = APIRouter()


@router.get("/")
async def read_users():
    client = ApiClient()
    return client.get("/users")
