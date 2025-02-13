from pydantic import UUID4
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from schemas.item import ItemInput, ItemOutput, ItemList
from services.item_service import ItemService
from db.base import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", status_code=201, response_model=ItemOutput)
def create_new_item(data: ItemInput, session: Session = Depends(get_db)):
    _service = ItemService(session)
    return _service.create(data)


@router.get("/{_id}", response_model=ItemOutput)
def get_item_details(_id: UUID4, session: Session = Depends(get_db)):
    _service = ItemService(session)
    return _service.get_by_id(_id)


@router.get("", status_code=200, response_model=ItemList)
def get_all_items(
    session: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(15, gt=0),
):
    offset = (page - 1) * page_size
    _service = ItemService(session)
    return _service.get_all(offset=offset, page_size=page_size)


@router.delete("/{_id}", status_code=204)
def delete_item(_id: UUID4, session: Session = Depends(get_db)):
    _service = ItemService(session).delete(_id)
    return _service


@router.put("/{_id}", status_code=200, response_model=ItemInput)
def update_item(_id: UUID4, data: ItemInput, session: Session = Depends(get_db)):
    _service = ItemService(session)
    return _service.update(_id, data)
