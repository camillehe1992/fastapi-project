from typing import Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from db.models import Item
from schemas.item import ItemInput, ItemOutput, ItemList


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session
        pass

    def create(self, data: ItemInput) -> ItemOutput:
        db_item = Item(**data.model_dump())
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return ItemOutput(**db_item.__dict__)

    def get_by_id(self, _id: UUID4) -> ItemOutput:
        return self.session.query(Item).filter_by(id=_id).first()

    def get_all(self, offset: int = 1, page_limit: int = 15) -> ItemList:
        items = self.session.query(Item).offset(offset).limit(page_limit).all()
        item_list = [ItemOutput(**item.__dict__) for item in items]

        result = ItemList(items=item_list, page=offset, page_size=len(item_list))
        return result

    def delete(self, item: Type[Item]) -> bool:
        self.session.delete(item)
        self.session.commit()
        return True

    def item_exists_by_id(self, _id: UUID4) -> bool:
        item = self.session.query(Item).filter_by(id=_id).first()
        return item is not None

    def update(self, item: Item, data: ItemInput) -> ItemInput:
        item.name = data.name
        item.description = data.description
        self.session.commit()
        self.session.refresh(item)
        return ItemInput(**item.__dict__)
