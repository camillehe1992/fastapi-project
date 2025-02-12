from fastapi import APIRouter, HTTPException
from schemas.item import ItemCreate, ItemResponse
from db.crud import create_item

router = APIRouter()


@router.post("/", response_model=ItemResponse)
def create_new_item(item: ItemCreate):
    db_item = create_item(item)
    if not db_item:
        raise HTTPException(status_code=400, detail="Item could not be created")
    return db_item
