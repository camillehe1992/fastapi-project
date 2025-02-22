import unittest
from unittest.mock import patch, MagicMock
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserInDBBase,
    Token,
    UserBase,
    UserIn,
)

# Import the functions directly
from app.routers.v1 import users


class TestUserRouter(unittest.TestCase):

    def setUp(self):
        # Common mock objects
        self.mock_session = MagicMock(spec=Session)
        self.mock_current_user = MagicMock(spec=UserIn)
        self.mock_current_user.id = UUID4("f47ac10b-58cc-4372-a567-0e02b2c3d479")

        # Patch get_session and get_current_user
        self.mock_get_session = patch("app.routers.v1.users.get_session").start()
        self.mock_get_session.return_value = self.mock_session

        self.mock_get_current_user = patch(
            "app.routers.v1.users.get_current_user"
        ).start()
        self.mock_get_current_user.return_value = self.mock_current_user

        # Patch UserService
        self.mock_user_service = patch("app.routers.v1.users.UserService").start()
        self.mock_user_service_instance = self.mock_user_service.return_value

        self.mock_created_user = UserInDBBase(
            id=UUID4("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            email="test@example.com",
            username="Test User",
            is_active=True,
            is_superuser=False,
        )

        self.mock_user = UserIn(
            id=UUID4("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            email="test@example.com",
            username="Test User",
            password="Test@Password123",
            is_active=True,
            is_superuser=False,
        )

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    def test_register(self):
        # Arrange
        user_register_data = UserRegister(
            email="test@example.com", password="password123", username="Test User"
        )

        self.mock_user_service_instance.create.return_value = (
            self.mock_created_user.model_dump()
        )

        # Act
        response = users.register(data=user_register_data, session=self.mock_session)

        # Assert
        self.mock_user_service.assert_called_once_with(self.mock_session)
        self.mock_user_service_instance.create.assert_called_once_with(
            user_register_data
        )
        self.assertEqual(response.message, "User is registered successfully.")
        self.assertEqual(response.data.id, self.mock_created_user.id)
        self.assertEqual(response.data.email, self.mock_created_user.email)
        self.assertEqual(response.data.username, self.mock_created_user.username)

    def test_login(self):
        # Arrange
        user_login_data = UserLogin(email="test@example.com", password="password123")
        mock_token = Token(
            access_token="mock_access_token",
            token_type="bearer",
            expired_at="1970-01-01 00:00:00 UTC+0000",
        )
        self.mock_user_service_instance.login.return_value = mock_token

        # Act
        response = users.login(data=user_login_data, session=self.mock_session)

        # Assert
        self.mock_user_service.assert_called_once_with(self.mock_session)
        self.mock_user_service_instance.login.assert_called_once_with(user_login_data)

        self.assertIsInstance(response, Token)
        self.assertEqual(response.access_token, "mock_access_token")
        self.assertEqual(response.token_type, "bearer")
        self.assertEqual(response.expired_at, "1970-01-01 00:00:00 UTC+0000")

    def test_get_me(self):
        # Arrange
        self.mock_get_current_user.return_value = self.mock_user

        # Act
        response = users.get_me(user=self.mock_user)

        # Assert
        self.assertIsInstance(response, UserBase)
        self.assertEqual(response.email, self.mock_user.email)
        self.assertEqual(response.username, self.mock_user.username)
