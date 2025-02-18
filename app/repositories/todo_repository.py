from typing import Type, Tuple
from pydantic import UUID4
from sqlalchemy.orm import Session

from db.models import Todo
from schemas.todo import TodoInput, TodoList, TodoOutput


class TodoRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: TodoInput) -> TodoOutput:
        db_item = Todo(**data.model_dump())
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return TodoOutput(**db_item.__dict__)

    def get_all(self, page: int = 1, page_size: int = 15) -> Tuple[int, TodoList]:
        offset = (page - 1) * page_size
        limit = page_size
        total_count = self.session.query(Todo).count()
        db_items = self.session.query(Todo).offset(offset).limit(limit).all()
        return total_count, [TodoOutput(**db_item.__dict__) for db_item in db_items]

    def get_by_id(self, _id: UUID4) -> TodoOutput:
        return self.session.query(Todo).filter_by(id=_id).first()

    def delete(self, db_item: Type[Todo]) -> bool:
        self.session.delete(db_item)
        self.session.commit()
        return True

    def exists_by_id(self, _id: UUID4) -> bool:
        db_item = self.session.query(Todo).filter_by(id=_id).first()
        return db_item is not None

    def update(self, db_item: Todo, data: TodoInput) -> TodoInput:
        db_item.title = data.title
        db_item.description = data.description
        db_item.completed = data.completed
        self.session.commit()
        self.session.refresh(db_item)
        return TodoInput(**db_item.__dict__)
