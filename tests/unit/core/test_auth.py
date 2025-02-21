import pytest
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression
from jose import JWTError
from app.core import security
from app.core.auth import get_user, get_current_user, User, TokenData


class TestGetUser(unittest.TestCase):
    def setUp(self):
        # Mock the dependencies for both functions
        self.mock_session_patcher = patch("app.core.auth.Session", autospec=True)
        self.mock_session = self.mock_session_patcher.start()
        self.mock_db_session = MagicMock(spec=Session)
        self.mock_session.return_value = self.mock_db_session

        self.mock_oauth2_scheme = patch(
            "app.core.auth.oauth2_scheme", new_callable=AsyncMock
        ).start()
        self.mock_get_db = patch("app.core.auth.get_db", new_callable=AsyncMock).start()
        self.mock_get_db.return_value = self.mock_db_session

    def tearDown(self):
        patch.stopall()

    def test_get_user_found(self):
        # Arrange
        mock_user = User(email="test@example.com")
        self.mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_user
        )

        # Act
        result = get_user(self.mock_db_session, "test@example.com")

        # Assert
        self.assertEqual(result, mock_user)
        self.mock_db_session.query.assert_called_once_with(User)

        # Check that filter was called with the correct condition
        filter_call_args = self.mock_db_session.query.return_value.filter.call_args[0][
            0
        ]
        self.assertIsInstance(filter_call_args, BinaryExpression)
        self.assertEqual(str(filter_call_args), str(User.email == "test@example.com"))

        # Check that first was called
        self.mock_db_session.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_user_not_found(self):
        # Arrange
        self.mock_db_session.query.return_value.filter.return_value.first.return_value = (
            None
        )

        # Act
        result = get_user(self.mock_db_session, "nonexistent@example.com")

        # Assert
        self.assertIsNone(result)
        self.mock_db_session.query.assert_called_once_with(User)

        # Check that filter was called with the correct condition
        filter_call_args = self.mock_db_session.query.return_value.filter.call_args[0][
            0
        ]
        self.assertIsInstance(filter_call_args, BinaryExpression)
        self.assertEqual(
            str(filter_call_args), str(User.email == "nonexistent@example.com")
        )

        # Check that first was called
        self.mock_db_session.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_user_exception_handling(self):
        # Arrange
        self.mock_db_session.query.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_user(self.mock_db_session, "error@example.com")

        self.assertEqual(str(context.exception), "Database error")
        self.mock_db_session.query.assert_called_once_with(User)


@patch("app.core.auth.oauth2_scheme")  # Mock the OAuth2PasswordBearer dependency
@patch("app.core.auth.get_db")  # Mock the database session
@patch("app.core.auth.jwt.decode")  # Mock jwt.decode
@patch("app.core.auth.get_user")  # Mock the get_user function
class TestGetCurrentUser(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Common setup for all test methods
        self.mock_token = "test_token"
        self.mock_email = "test@example.com"
        self.mock_user = MagicMock(spec=User)
        self.mock_get_db = MagicMock(spec=Session)

    async def test_get_current_user_valid_token(
        self, mock_get_user, mock_jwt_decode, mock_get_db, mock_oauth2_scheme
    ):
        """
        Test that get_current_user returns the correct user when the token is valid.
        """
        # Arrange
        mock_oauth2_scheme.return_value = self.mock_token
        mock_jwt_decode.return_value = {"sub": self.mock_email}
        mock_get_user.return_value = self.mock_user
        mock_get_db.return_value = self.mock_get_db

        # Act
        result = await get_current_user(token=self.mock_token, db=self.mock_get_db)

        # Assert
        mock_jwt_decode.assert_called_once_with(
            self.mock_token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        mock_get_user.assert_called_once_with(
            mock_get_db.return_value, email=self.mock_email
        )
        self.assertEqual(result, self.mock_user)

    async def test_get_current_user_invalid_token(
        self, mock_get_user, mock_jwt_decode, mock_get_db, mock_oauth2_scheme
    ):
        """
        Test that get_current_user raises an HTTPException when the token is invalid.
        """
        # Arrange
        mock_oauth2_scheme.return_value = self.mock_token
        mock_jwt_decode.side_effect = JWTError("Invalid token")

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await get_current_user(token=self.mock_token, db=MagicMock(spec=Session))

        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
        self.assertEqual(context.exception.headers, {"WWW-Authenticate": "Bearer"})

    async def test_get_current_user_missing_email(
        self, mock_get_user, mock_jwt_decode, mock_get_db, mock_oauth2_scheme
    ):
        """
        Test that get_current_user raises an HTTPException when the token payload is missing the email.
        """
        # Arrange
        mock_oauth2_scheme.return_value = self.mock_token
        mock_jwt_decode.return_value = {"sub": None}  # Missing email

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await get_current_user(token=self.mock_token, db=MagicMock(spec=Session))

        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
        self.assertEqual(context.exception.headers, {"WWW-Authenticate": "Bearer"})

    async def test_get_current_user_user_not_found(
        self, mock_get_user, mock_jwt_decode, mock_get_db, mock_oauth2_scheme
    ):
        """
        Test that get_current_user raises an HTTPException when the user is not found in the database.
        """
        # Arrange
        mock_oauth2_scheme.return_value = self.mock_token
        mock_jwt_decode.return_value = {"sub": self.mock_email}
        mock_get_user.return_value = None  # User not found

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await get_current_user(token=self.mock_token, db=MagicMock(spec=Session))

        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
        self.assertEqual(context.exception.headers, {"WWW-Authenticate": "Bearer"})
