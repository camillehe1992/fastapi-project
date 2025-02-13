from typing import Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from db.models import Item
from schemas.item import ItemCreate, ItemResponse


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session
        pass

    def create(self, data: ItemCreate) -> ItemCreate:
        db_item = Item(**data.model_dump())
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return ItemResponse(**db_item.__dict__)
