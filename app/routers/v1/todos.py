from pydantic import UUID4
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from schemas.todo import TodoInput, TodoOutput, TodoList
from schemas.user import UserIn
from services.todo_service import TodoService
from db.base import get_db
from core.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TodoOutput)
def create_new_todo(
    data: TodoInput,
    session: Session = Depends(get_db),
    current_user: UserIn = Depends(get_current_user),
):
    data.user_id = current_user.id
    _service = TodoService(session)
    return _service.create(data)


@router.get("", status_code=status.HTTP_200_OK, response_model=TodoList)
def get_all_todos(
    session: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(15, gt=0),
):
    _service = TodoService(session)
    todos = _service.get_all(page=page, page_size=page_size)
    return TodoList(todos=todos, page=page, page_size=len(todos))


@router.get("/{_id}", response_model=TodoOutput)
def get_todo_details(_id: UUID4, session: Session = Depends(get_db)):
    _service = TodoService(session)
    return _service.get_by_id(_id)


@router.delete("/{_id}", status_code=status.HTTP_200_OK)
def delete_todo(_id: UUID4, session: Session = Depends(get_db)):
    deleted_todo = TodoService(session).delete(_id)
    return {"message": "Item deleted successfully", "deleted_todo": deleted_todo}


@router.put("/{_id}", status_code=status.HTTP_200_OK, response_model=TodoOutput)
def update_todo(_id: UUID4, data: TodoInput, session: Session = Depends(get_db)):
    _service = TodoService(session)
    return _service.update(_id, data)
