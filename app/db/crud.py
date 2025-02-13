from sqlalchemy.orm import Session
from .models import Item


def create_item(db: Session, item):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, id: str):
    return db.query(Item).filter(Item.id == id).first()


def list_items(db: Session):
    return db.query(Item).all()
