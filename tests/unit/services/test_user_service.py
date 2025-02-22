import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister, UserLogin, UserInDBBase
from app.services.user_service import UserService


class TestUserService(unittest.TestCase):

    def setUp(self):
        # Mock the SQLAlchemy session
        self.mock_session = MagicMock(spec=Session)

        # Mock the UserRepository
        self.mock_user_repository = MagicMock(spec=UserRepository)

        # Initialize the UserService with mocked dependencies
        self.user_service = UserService(self.mock_session)
        self.user_service.repository = self.mock_user_repository

        # Common mock data
        self.user_id = UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")
        self.email = "test@example.com"
        self.username = "testuser"
        self.password = "Password@123"
        self.hashed_password = get_password_hash(self.password)

        # Mock User instance
        self.mock_db_user = MagicMock()
        self.mock_db_user.id = self.user_id
        self.mock_db_user.email = self.email
        self.mock_db_user.username = self.username
        self.mock_db_user.hashed_password = self.hashed_password
        self.mock_db_user.is_superuser = False
        self.mock_db_user.as_dict.return_value = {
            "id": self.user_id,
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "is_superuser": False,
        }

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    @patch("app.services.user_service.get_password_hash")
    @patch("app.services.user_service.validate_password")
    @patch("app.services.user_service.validate_email")
    def test_create(
        self, mock_validate_email, mock_validate_password, mock_get_password_hash
    ):
        # Arrange
        user_register = UserRegister(
            email=self.email, username=self.username, password=self.password
        )
        self.mock_user_repository.user_exists_by_email.return_value = False
        self.mock_user_repository.user_exists_by_username.return_value = False
        self.mock_user_repository.create.return_value = self.mock_db_user

        # Mock the get_password_hash function to return a consistent value
        mock_get_password_hash.return_value = self.hashed_password

        # Act
        result = self.user_service.create(user_register)

        # Assert
        mock_validate_password.assert_called_once_with(self.password)
        mock_validate_password.assert_called_once_with(self.password)
        mock_validate_email.assert_called_once_with(self.email)
        self.mock_user_repository.user_exists_by_email.assert_called_once_with(
            self.email
        )
        self.mock_user_repository.user_exists_by_username.assert_called_once_with(
            self.username
        )
        self.mock_user_repository.create.assert_called_once_with(
            user_register, self.hashed_password
        )
        self.assertEqual(result.id, self.user_id)
        self.assertEqual(result.email, self.email)
        self.assertEqual(result.username, self.username)

    @patch("app.services.user_service.validate_password")
    @patch("app.services.user_service.validate_email")
    def test_create_email_already_registered(
        self, mock_validate_email, mock_validate_password
    ):
        # Arrange
        user_register = UserRegister(
            email=self.email, username=self.username, password=self.password
        )
        self.mock_user_repository.user_exists_by_email.return_value = True

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.user_service.create(user_register)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, f"Email {self.email} already registered"
        )

    @patch("app.services.user_service.validate_password")
    @patch("app.services.user_service.validate_email")
    def test_create_username_already_registered(
        self, mock_validate_email, mock_validate_password
    ):
        # Arrange
        user_register = UserRegister(
            email=self.email, username=self.username, password=self.password
        )
        self.mock_user_repository.user_exists_by_email.return_value = False
        self.mock_user_repository.user_exists_by_username.return_value = True

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.user_service.create(user_register)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, f"Username {self.username} already registered"
        )

    @patch("app.services.user_service.pwd_context")
    @patch("app.services.user_service.create_access_token")
    @patch("app.services.user_service.DateTimeHelper")
    def test_login(
        self, mock_datetime_helper, mock_create_access_token, mock_pwd_context
    ):
        # Arrange
        user_login = UserLogin(email=self.email, password=self.password)
        self.mock_user_repository.get_user_by_email.return_value = self.mock_db_user
        mock_pwd_context.verify.return_value = True

        mock_datetime_instance = MagicMock()
        mock_datetime_instance.now.return_value = datetime.now()
        mock_datetime_instance.format.return_value = "2023-10-01T00:00:00Z"
        mock_datetime_helper.return_value = mock_datetime_instance

        mock_create_access_token.return_value = "mock_access_token"

        # Act
        result = self.user_service.login(user_login)

        # Assert
        self.mock_user_repository.get_user_by_email.assert_called_once_with(self.email)
        mock_pwd_context.verify.assert_called_once_with(
            self.password, self.hashed_password
        )
        mock_create_access_token.assert_called_once()
        self.assertEqual(result["access_token"], "mock_access_token")
        self.assertEqual(result["token_type"], "bearer")
        self.assertEqual(result["expired_at"], "2023-10-01T00:00:00Z")

    def test_login_incorrect_email_or_password(self):
        # Arrange
        user_login = UserLogin(email=self.email, password=self.password)
        self.mock_user_repository.get_user_by_email.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.user_service.login(user_login)
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Incorrect email or password")

    def test_is_superuser(self):
        # Arrange
        self.mock_user_repository.user_exists_by_id.return_value = True
        self.mock_user_repository.get_user_object_by_id.return_value = self.mock_db_user

        # Act
        result = self.user_service.is_superuser(self.user_id)

        # Assert
        self.mock_user_repository.user_exists_by_id.assert_called_once_with(
            self.user_id
        )
        self.mock_user_repository.get_user_object_by_id.assert_called_once_with(
            self.user_id
        )
        self.assertFalse(result)

    def test_is_superuser_user_not_found(self):
        # Arrange
        self.mock_user_repository.user_exists_by_id.return_value = False

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.user_service.is_superuser(self.user_id)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, f"User {self.user_id} not found")

    def test_delete_user(self):
        # Arrange
        self.mock_user_repository.user_exists_by_id.return_value = True
        self.mock_user_repository.get_user_object_by_id.return_value = self.mock_db_user

        # Act
        result = self.user_service.delete_user(self.user_id)

        # Assert
        self.mock_user_repository.user_exists_by_id.assert_called_once_with(
            self.user_id
        )
        self.mock_user_repository.get_user_object_by_id.assert_called_once_with(
            self.user_id
        )
        self.mock_user_repository.delete_user.assert_called_once_with(self.mock_db_user)
        self.assertTrue(result)

    def test_delete_user_not_found(self):
        # Arrange
        self.mock_user_repository.user_exists_by_id.return_value = False

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.user_service.delete_user(self.user_id)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, f"User {self.user_id} not found")
