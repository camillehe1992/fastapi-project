import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.auth import get_current_user
from app.db.base import get_db, Base


# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# def mock_get_current_user():
#     return {
#         "username": "John Doe",
#         "email": "john.doe@example.com",
#         "password": "Mypassword@123",
#     }


app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[get_current_user] = mock_get_current_user


# Fixture to create the test database
# @pytest.fixture(scope="module")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# Fixture to provide a test client
# @pytest.fixture(scope="module")
# def client():
#     with TestClient(app) as client:
#         yield client
