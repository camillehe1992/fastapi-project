import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import get_session
from app.db.models import Base
from app.main import app

# Configure a test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Fixture to create a new database session for each test
@pytest.fixture
async def session():
    # Create all database tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Provide a session for the test
    async with TestingSessionLocal() as session:
        yield session

    # Drop all database tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Fixture to override the get_session dependency and provide a TestClient
@pytest.fixture
def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)  # Return a TestClient instance
