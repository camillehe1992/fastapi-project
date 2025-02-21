from db.base import engine
from db.models import Base, User, Todo


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Base.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Todo.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drops all database tables defined in the application.
    """
    Base.metadata.drop_all(bind=engine)
    User.metadata.drop_all(bind=engine)
    Todo.metadata.drop_all(bind=engine)
