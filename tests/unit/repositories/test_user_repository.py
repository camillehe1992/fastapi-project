from pydantic import UUID4
from unittest import TestCase
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserIn, UserInDBBase
from app.repositories.user_repository import UserRepository


class TestUserRepository(TestCase):
    def setUp(self):
        self.mock_session = Mock(spec=Session)
        self.user_repo = UserRepository(self.mock_session)

    # def test_create_user(self):
    #     # Create a mock user input data
    #     user_data = UserIn(
    #         username="testuser", email="test@example.com", password="password123"
    #     )

    #     # Mock the hashed password
    #     hashed_password = "hashed_password123"

    #     # Mock the database user object
    #     mock_db_user = Mock()
    #     mock_db_user.__dict__ = {
    #         "id": UUID4("123e4567-e89b-12d3-a456-426614174000"),
    #         "username": "testuser",
    #         "email": "test@example.com",
    #         # "hashed_password": hashed_password,
    #         "is_superuser": False,
    #         "is_active": True,
    #     }

    #     # Mock the session methods
    #     self.mock_session.add.return_value = None
    #     self.mock_session.commit.return_value = None
    #     self.mock_session.refresh.return_value = None

    #     # Patch the User model to return the mock_db_user
    #     with patch("app.db.models.User", return_value=mock_db_user):
    #         # Call the create method
    #         result = self.user_repo.create(user_data, hashed_password)

    #         # Assertions
    #         assert isinstance(result, UserInDBBase)
    #         assert result.username == "testuser"
    #         assert result.email == "test@example.com"
    #         assert result.hashed_password == hashed_password

    #         # Verify that the session methods were called
    #         self.mock_session.add.assert_called_once_with(mock_db_user)
    #         self.mock_session.commit.assert_called_once()
    #         self.mock_session.refresh.assert_called_once_with(mock_db_user)
