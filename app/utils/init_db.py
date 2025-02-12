from config.database import Base, engine
from db.models import Item, Album, Photo, User, Post


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Base.metadata.create_all(bind=engine)
    Item.metadata.create_all(bind=engine)
    Album.metadata.create_all(bind=engine)
    Photo.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Post.metadata.create_all(bind=engine)
