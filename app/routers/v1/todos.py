from pydantic import UUID4
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from schemas.response import CommonResponse
from schemas.todo import TodoInput, TodoOutput, TodoList
from schemas.user import UserInDBBase
from services.todo_service import TodoService
from db.base import get_db
from core.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=CommonResponse[TodoOutput]
)
def create_new_todo(
    data: TodoInput,
    session: Session = Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user),
):
    data.user_id = current_user.id
    _service = TodoService(session)
    created_todo = _service.create(data)
    return CommonResponse[TodoOutput](
        message="Todo is created successfully.", data=created_todo
    )


@router.get("", status_code=status.HTTP_200_OK, response_model=TodoList)
def get_all_todos(
    session: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(15, gt=0),
):
    _service = TodoService(session)
    total_count, todos = _service.get_all(page=page, page_size=page_size)
    return TodoList(
        todos=todos, page=page, page_size=len(todos), total_count=total_count
    )


@router.get("/{_id}", response_model=TodoOutput)
def get_todo_details(_id: UUID4, session: Session = Depends(get_db)):
    _service = TodoService(session)
    return _service.get_by_id(_id)


@router.delete(
    "/{_id}", status_code=status.HTTP_200_OK, response_model=CommonResponse[TodoOutput]
)
def delete_todo(
    _id: UUID4,
    session: Session = Depends(get_db),
    _: UserInDBBase = Depends(get_current_user),
):
    deleted_todo = TodoService(session).delete(_id)
    return CommonResponse[TodoOutput](
        message="Todo is deleted successfully.", data=deleted_todo
    )


@router.put(
    "/{_id}", status_code=status.HTTP_200_OK, response_model=CommonResponse[TodoOutput]
)
def update_todo(
    _id: UUID4,
    data: TodoInput,
    session: Session = Depends(get_db),
    _: UserInDBBase = Depends(get_current_user),
):
    _service = TodoService(session)
    updated_todo = _service.update(_id, data)
    return CommonResponse[TodoOutput](
        message="Todo is updated successfully.", data=updated_todo
    )
