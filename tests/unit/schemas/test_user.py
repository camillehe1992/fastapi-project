import unittest
from uuid import uuid4
from pydantic import ValidationError
from app.schemas.user import (
    UserBase,
    UserRegister,
    UserLogin,
    UserIn,
    UserInDBBase,
    UserInDB,
    TokenData,
    Token,
)


class TestUserModels(unittest.TestCase):
    def test_user_base(self):
        """Test the UserBase model."""
        user = UserBase(
            email="john.doe@example.com",
            username="John Doe",
            is_superuser=False,
            is_active=True,
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.username, "John Doe")
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_user_register(self):
        """Test the UserRegister model."""
        user = UserRegister(
            email="john.doe@example.com", username="John Doe", password="password123"
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.username, "John Doe")
        self.assertEqual(user.password, "password123")

    def test_user_login(self):
        """Test the UserLogin model."""
        user = UserLogin(email="john.doe@example.com", password="password123")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.password, "password123")

    def test_user_in(self):
        """Test the UserIn model."""
        user = UserIn(
            email="john.doe@example.com",
            username="John Doe",
            password="password123",
            is_superuser=False,
            is_active=True,
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.username, "John Doe")
        self.assertEqual(user.password, "password123")
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_user_in_db_base(self):
        """Test the UserInDBBase model."""
        user_id = uuid4()
        user = UserInDBBase(
            id=user_id,
            email="john.doe@example.com",
            username="John Doe",
            is_superuser=False,
            is_active=True,
        )
        self.assertEqual(user.id, user_id)
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.username, "John Doe")
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_user_in_db(self):
        """Test the UserInDB model."""
        user_id = uuid4()
        user = UserInDB(
            id=user_id,
            email="john.doe@example.com",
            username="John Doe",
            is_superuser=False,
            is_active=True,
            hashed_password="hashed_password_123",
        )
        self.assertEqual(user.id, user_id)
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.username, "John Doe")
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.hashed_password, "hashed_password_123")

    def test_token_data(self):
        """Test the TokenData model."""
        token_data = TokenData(email="john.doe@example.com")
        self.assertEqual(token_data.email, "john.doe@example.com")

        token_data_none = TokenData(email=None)
        self.assertIsNone(token_data_none.email)

    def test_token(self):
        """Test the Token model."""
        token = Token(
            access_token="access_token_123",
            token_type="bearer",
            expired_at="2025-02-22 08:38:19 UTC+0000",
        )
        self.assertEqual(token.access_token, "access_token_123")
        self.assertEqual(token.token_type, "bearer")
        self.assertEqual(token.expired_at, "2025-02-22 08:38:19 UTC+0000")

    def test_validation_errors(self):
        """Test validation errors for required fields."""
        with self.assertRaises(ValidationError):
            UserRegister(
                email="john.doe@example.com", username="John Doe"
            )  # Missing password

        with self.assertRaises(ValidationError):
            UserLogin(username="John Doe")  # Missing password
