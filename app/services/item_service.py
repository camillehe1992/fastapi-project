from typing import List, Dict, Any

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository
from schemas.item import ItemInput, ItemResponse


class ItemService:

    def __init__(self, session: Session):
        self.repository = ItemRepository(session)
        pass

    def create(self, data: dict) -> Dict[str, Any]:
        item = self.repository.create(data)
        return ItemResponse(**item.model_dump())

    def get_by_id(self, _id: UUID4) -> Dict[str, Any]:
        return self.repository.get_by_id(_id)

    def get_all(self, offset: int = 1, page_size: int = 15) -> Dict[str, Any]:
        return self.repository.get_all(offset, page_size)

    def delete(self, _id: int) -> bool:
        if not self.repository.item_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Item not found")
        item = self.repository.get_by_id(_id)
        self.repository.delete(item)
        return True

    def update(self, _id: UUID4, data: ItemInput) -> ItemInput:
        if not self.repository.item_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Item not found")

        item = self.repository.get_by_id(_id)
        return self.repository.update(item, data)
