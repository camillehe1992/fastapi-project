import pytest
from unittest import TestCase
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression
from jose import JWTError
from app.core import security
from app.core.auth import get_user, get_current_user, User, TokenData


class TestAuthFunctions(TestCase):
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

    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self):
        # Arrange
        self.mock_oauth2_scheme.return_value = "valid_token"
        print(f"Mocked token: {self.mock_oauth2_scheme.return_value}")
        mock_user = User(email="test@example.com")
        with patch(
            "app.core.auth.jwt.decode", return_value={"sub": "test@example.com"}
        ):
            with patch("app.core.auth.get_user", return_value=mock_user):
                # Act
                result = await get_current_user(
                    token="valid_token", db=self.mock_db_session
                )

                # Assert
                self.assertEqual(result, mock_user)

    @patch("app.core.auth.jwt.decode", return_value={"sub": "test@example.com"})
    async def test_get_current_user_valid_token(self):
        # Arrange
        mock_user = User(email="test@example.com")
        self.mock_oauth2_scheme.return_value = "valid_token"
        with patch("app.core.auth.get_user", return_value=mock_user):
            # Act
            result = await get_current_user(
                token="valid_token", db=self.mock_db_session
            )

            # Assert
            self.assertEqual(result, mock_user)

    @patch("app.core.auth.jwt.decode", side_effect=JWTError)
    async def test_get_current_user_invalid_token(self, mock_decode):
        # Arrange
        self.mock_oauth2_scheme.return_value = "invalid_token"

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await get_current_user(token="invalid_token", db=self.mock_db_session)
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")

        mock_decode.assert_not_called()

    @patch("app.core.auth.jwt.decode", return_value={"sub": None})
    async def test_get_current_user_missing_email(self):
        # Arrange
        self.mock_oauth2_scheme.return_value = "token_without_email"

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await get_current_user(token="token_without_email", db=self.mock_db_session)
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")

    @patch("app.core.auth.jwt.decode", return_value={"sub": "nonexistent@example.com"})
    async def test_get_current_user_not_found(self):
        # Arrange
        self.mock_oauth2_scheme.return_value = "valid_token"

        with patch("app.core.auth.get_user", return_value=None):
            # Act & Assert
            with self.assertRaises(HTTPException) as context:
                await get_current_user(token="valid_token", db=self.mock_db_session)
            self.assertEqual(
                context.exception.status_code, status.HTTP_401_UNAUTHORIZED
            )
            self.assertEqual(context.exception.detail, "Could not validate credentials")

    @patch("app.core.auth.jwt.decode", side_effect=JWTError)
    async def test_get_current_user_jwt_decode_error(self):
        # Arrange
        self.mock_oauth2_scheme.return_value = "invalid_token"

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await get_current_user(token="invalid_token", db=self.mock_db_session)

        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
