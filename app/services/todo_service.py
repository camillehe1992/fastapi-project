from typing import Dict, Any
from pydantic import UUID4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from services.user_service import UserService
from schemas.todo import TodoInput, TodoOutput
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

        return self.repository.create(data)

    def get_all(self, page: int = 1, page_size: int = 15) -> Dict[str, Any]:
        return self.repository.get_all(page=page, page_size=page_size)

    def get_by_id(self, _id: UUID4) -> Dict[str, Any]:
        return self.repository.get_by_id(_id)

    def delete(self, _id: int) -> Dict[str, Any]:
        if not self.repository.exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {_id} not found",
            )
        todo = self.repository.get_by_id(_id)
        self.repository.delete(todo)
        return todo

    def update(self, _id: UUID4, data: Dict) -> Dict[str, Any]:
        if not self.repository.exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {_id} not found",
            )

        todo = self.repository.get_by_id(_id)
        return self.repository.update(todo, data)
