from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

if settings.DEBUG:
    SQLALCHEMY_DATABASE_URL = settings.SQLITE_CONNECTION_STRING
else:
    SQLALCHEMY_DATABASE_URL = settings.POSTGRES_CONNECTION_STRING

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session():
    """
    Create a database session.

    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
