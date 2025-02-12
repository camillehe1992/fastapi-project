from config.database import Base, engine
from models.album import Album
from models.photo import Photo
from models.post import Post
from models.user import User


def drop_tables():
    """
    Drops all database tables defined in the application.
    """
    Base.metadata.drop_all(bind=engine)
    Album.metadata.drop_all(bind=engine)
    Photo.metadata.drop_all(bind=engine)
    Post.metadata.drop_all(bind=engine)
    User.metadata.drop_all(bind=engine)
