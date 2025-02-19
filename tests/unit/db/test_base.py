# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session

# # from app.settings import settings
# from app.db.base import get_db, Base, settings


# @pytest.fixture
# def mock_debug_true(monkeypatch):
#     """Fixture to mock DEBUG=True."""
#     monkeypatch.setattr(settings, "DEBUG", True)
#     monkeypatch.setattr(settings, "SQLITE_CONNECTION_STRING", "sqlite:///:memory:")


# @pytest.fixture
# def mock_debug_false(monkeypatch):
#     """Fixture to mock DEBUG=False."""
#     monkeypatch.setattr(settings, "DEBUG", False)
#     monkeypatch.setattr(
#         settings,
#         "POSTGRES_CONNECTION_STRING",
#         "postgresql://user:password@localhost/test_db",
#     )


# @pytest.fixture
# def db_session(mock_debug_true):
#     """Fixture to create a database session for testing."""
#     engine = create_engine(settings.SQLITE_CONNECTION_STRING)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = SessionLocal()
#     yield db
#     db.close()
#     Base.metadata.drop_all(bind=engine)


# def test_get_db_with_debug_true(mock_debug_true):
#     """Test that get_db uses SQLite when DEBUG=True."""
#     db_gen = get_db()
#     db = next(db_gen)
#     assert isinstance(db, Session)
#     assert db.bind.url.database == ":memory:"
#     try:
#         next(db_gen)
#     except StopIteration:
#         pass


# def test_get_db_with_debug_false(mock_debug_false):
#     """Test that get_db uses PostgreSQL when DEBUG=False."""
#     db_gen = get_db()
#     db = next(db_gen)
#     assert isinstance(db, Session)
#     assert db.bind.url.database == "test_db"
#     try:
#         next(db_gen)
#     except StopIteration:
#         pass


# def test_db_session_fixture(db_session):
#     """Test the db_session fixture and ensure it works correctly."""
#     assert isinstance(db_session, Session)
#     assert db_session.bind.url.database == ":memory:"
