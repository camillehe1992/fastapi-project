from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository
from schemas.item import ItemResponse


class ItemService:

    def __init__(self, session: Session):
        self.repository = ItemRepository(session)
        pass

    def create(self, data: dict):
        item = self.repository.create(data)
        return ItemResponse(**item.model_dump())
