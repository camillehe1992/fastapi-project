import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserRegister, UserInDBBase
from app.repositories.user_repository import (
    UserRepository,
)


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        # Mock the SQLAlchemy session
        self.mock_session = MagicMock(spec=Session)
        self.user_repository = UserRepository(self.mock_session)

        # Common mock data
        self.user_id = UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")
        self.email = "test@example.com"
        self.username = "testuser"
        self.hashed_password = "hashed_password"

        # Mock User instance
        self.mock_db_user = MagicMock(spec=User)
        self.mock_db_user.id = self.user_id
        self.mock_db_user.email = self.email
        self.mock_db_user.username = self.username
        self.mock_db_user.hashed_password = self.hashed_password
        self.mock_db_user.is_active = True

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    @patch("app.repositories.user_repository.User")  # Patch the User model
    def test_create(self, mock_user_model):
        # Arrange
        user_register = UserRegister(
            email=self.email, username=self.username, password="password123"
        )
        mock_user_model.return_value = self.mock_db_user
        self.mock_session.add.return_value = None
        self.mock_session.commit.return_value = None
        self.mock_session.refresh.return_value = None

        # Act
        result = self.user_repository.create(user_register, self.hashed_password)

        # Assert
        mock_user_model.assert_called_once_with(
            email=self.email,
            username=self.username,
            hashed_password=self.hashed_password,
        )
        self.mock_session.add.assert_called_once_with(self.mock_db_user)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.mock_db_user)
        self.assertIsInstance(result, User)
        self.assertEqual(result.id, self.mock_db_user.id)
        self.assertEqual(result.email, self.mock_db_user.email)
        self.assertEqual(result.username, self.mock_db_user.username)
        self.assertEqual(result.hashed_password, self.mock_db_user.hashed_password)

    def test_user_exists_by_email(self):
        # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = (
            self.mock_db_user
        )

        # Act
        result = self.user_repository.user_exists_by_email(self.email)

        # Assert
        self.mock_session.query.return_value.filter.assert_called_once()
        self.assertTrue(result)

    def test_user_exists_by_username(self):
        # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = (
            self.mock_db_user
        )

        # Act
        result = self.user_repository.user_exists_by_username(self.username)

        # Assert
        self.mock_session.query.return_value.filter.assert_called_once()
        self.assertTrue(result)

    def test_get_user_by_email(self):
        # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = (
            self.mock_db_user
        )

        # Act
        result = self.user_repository.get_user_by_email(self.email)

        # Assert
        self.mock_session.query.return_value.filter.assert_called_once()
        self.assertIsInstance(result, User)
        self.assertEqual(result.id, self.mock_db_user.id)
        self.assertEqual(result.email, self.mock_db_user.email)
        self.assertEqual(result.username, self.mock_db_user.username)
        self.assertEqual(result.hashed_password, self.mock_db_user.hashed_password)

    def test_get_user_by_username(self):
        # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = (
            self.mock_db_user
        )

        # Act
        result = self.user_repository.get_user_by_username(self.username)

        # Assert
        self.mock_session.query.return_value.filter.assert_called_once()
        self.assertIsInstance(result, User)
        self.assertEqual(result.id, self.mock_db_user.id)
        self.assertEqual(result.email, self.mock_db_user.email)
        self.assertEqual(result.username, self.mock_db_user.username)
        self.assertEqual(result.hashed_password, self.mock_db_user.hashed_password)

    def test_get_user_object_by_id(self):
        # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = (
            self.mock_db_user
        )

        # Act
        result = self.user_repository.get_user_object_by_id(self.user_id)

        # Assert
        self.mock_session.query.return_value.filter.assert_called_once()
        self.assertIsInstance(result, User)
        self.assertEqual(result.id, self.mock_db_user.id)
        self.assertEqual(result.email, self.mock_db_user.email)
        self.assertEqual(result.username, self.mock_db_user.username)
        self.assertEqual(result.hashed_password, self.mock_db_user.hashed_password)

    def test_user_exists_by_id(self):
        # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = (
            self.mock_db_user
        )

        # Act
        result = self.user_repository.user_exists_by_id(self.user_id)

        # Assert
        self.mock_session.query.return_value.filter.assert_called_once()
        self.assertTrue(result)

    def test_inactive_user(self):
        # Arrange
        self.mock_session.commit.return_value = None
        self.mock_session.refresh.return_value = None

        # Act
        result = self.user_repository.inactive_user(self.mock_db_user)

        # Assert
        self.assertEqual(self.mock_db_user.is_active, False)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.mock_db_user)
        self.assertTrue(result)

    def test_delete_user(self):
        # Arrange
        self.mock_session.delete.return_value = None
        self.mock_session.commit.return_value = None

        # Act
        result = self.user_repository.delete_user(self.mock_db_user)

        # Assert
        self.mock_session.delete.assert_called_once_with(self.mock_db_user)
        self.mock_session.commit.assert_called_once()
        self.assertTrue(result)
