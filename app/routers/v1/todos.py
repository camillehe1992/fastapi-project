from fastapi import APIRouter, Depends, Query

from core.api_client import ApiClient
from schemas.todo import TodoList
from services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", status_code=200, response_model=TodoList)
def get_todos(
    page: int = Query(1, gt=0),
    page_size: int = Query(15, gt=0),
):
    _service = TodoService(client=ApiClient())
    return _service.get_all(page=page, page_limit=page_size)
