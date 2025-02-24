import pytest
import string
import random
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.utils import create_tables, drop_tables
from app.db.base import get_session
from app.main import app

# Configure a test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Create all tables
create_tables()


# Fixture to override the get_session dependency
@pytest.fixture
def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Fixture to provide a TestClient instance
@pytest.fixture
def client(override_get_session):
    app.dependency_overrides[get_session] = lambda: override_get_session
    with TestClient(app) as test_client:
        yield test_client


# Fixture to clean up the database after tests
@pytest.fixture(autouse=True)
def cleanup():
    yield
    drop_tables()


# Function to generate a random username
def generate_random_username(length=8):
    characters = string.ascii_lowercase + string.digits  # lowercase letters and digits
    username = "".join(random.choice(characters) for _ in range(length))
    return username
