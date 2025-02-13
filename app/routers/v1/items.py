from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.item import ItemCreate, ItemResponse
from services.item_service import ItemService
from db.base import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", status_code=201, response_model=ItemResponse)
def create_new_item(data: ItemCreate, session: Session = Depends(get_db)):
    _service = ItemService(session)
    return _service.create(data)


@router.get("/{id}", response_model=ItemResponse)
def get_a_item():
    pass


@router.get("", response_model=List[ItemResponse])
def list_all_items():
    pass
