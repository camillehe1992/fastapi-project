from db.base import Base, engine
from db.models import Todo, Item, Album, Photo, User, Post


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Base.metadata.create_all(bind=engine)
    Album.metadata.create_all(bind=engine)
    Photo.metadata.create_all(bind=engine)
    Post.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Item.metadata.create_all(bind=engine)
    Todo.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drops all database tables defined in the application.
    """
    Base.metadata.drop_all(bind=engine)
    Album.metadata.drop_all(bind=engine)
    Photo.metadata.drop_all(bind=engine)
    Post.metadata.drop_all(bind=engine)
    User.metadata.drop_all(bind=engine)
    Item.metadata.drop_all(bind=engine)
    Todo.metadata.drop_all(bind=engine)
