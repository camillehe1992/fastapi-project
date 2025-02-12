from sqlalchemy.orm import Session
from .models import Item


def create_item(db: Session, item):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
