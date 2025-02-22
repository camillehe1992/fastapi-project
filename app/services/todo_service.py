from typing import Tuple, List
from pydantic import UUID4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from schemas.todo import TodoInput, TodoOutput
from services.user_service import UserService
from repositories.todo_repository import TodoRepository


class TodoService:
    def __init__(self, session: Session):
        self.repository = TodoRepository(session)
        self.user_service = UserService(session)

    def create(self, data: TodoInput) -> TodoOutput:
        # if not self.user_service.is_superuser(data.user_id):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        #     )
        created_todo = self.repository.create(data)
        return TodoOutput(**created_todo.as_dict())

    def get_all(
        self, page: int = 1, page_size: int = 15
    ) -> Tuple[int, List[TodoOutput]]:
        total_count, todos = self.repository.get_all(page=page, page_size=page_size)
        todos = [TodoOutput(**todo.as_dict()) for todo in todos]
        return total_count, todos

    def get_by_id(self, _id: UUID4) -> TodoOutput:
        return TodoOutput(**self.repository.get_by_id(_id).as_dict())

    def delete(self, _id: int) -> TodoOutput:
        if not self.repository.exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {_id} not found",
            )
        todo = self.repository.get_by_id(_id)
        self.repository.delete(todo)
        return TodoOutput(**todo.as_dict())

    def update(self, _id: UUID4, data: TodoInput) -> TodoOutput:
        if not self.repository.exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {_id} not found",
            )

        current_todo = self.repository.get_by_id(_id)
        return TodoOutput(**self.repository.update(current_todo, data).as_dict())
