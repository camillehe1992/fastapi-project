from typing import Type, Tuple, List
from pydantic import UUID4

from sqlalchemy.orm import Session

from schemas.todo import TodoInput, TodoOutput
from db.models import Todo


class TodoRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: TodoInput) -> Todo:
        db_item = Todo(**data.model_dump())
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def get_all(self, page: int = 1, page_size: int = 15) -> Tuple[int, List[Todo]]:
        offset = (page - 1) * page_size
        limit = page_size
        total_count = self.session.query(Todo).count()
        db_items = self.session.query(Todo).offset(offset).limit(limit).all()
        return total_count, db_items

    def get_by_id(self, _id: UUID4) -> Todo:
        return self.session.query(Todo).filter_by(id=_id).first()

    def delete(self, db_item: Type[Todo]) -> bool:
        self.session.delete(db_item)
        self.session.commit()
        return True

    def exists_by_id(self, _id: UUID4) -> bool:
        db_item = self.session.query(Todo).filter_by(id=_id).first()
        return db_item is not None

    def update(self, db_item: TodoOutput, updated: TodoInput) -> Todo:
        db_item.title = updated.title
        db_item.completed = updated.completed
        self.session.commit()
        self.session.refresh(db_item)
        updated_item = self.session.query(Todo).filter_by(id=db_item.id).first()
        return updated_item
