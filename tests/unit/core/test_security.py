import unittest
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.security import (
    get_password_hash,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


class TestPasswordAndTokenFunctions(unittest.TestCase):

    def test_get_password_hash(self):
        # Test that the function returns a hashed password
        password = "testpassword"
        hashed_password = get_password_hash(password)
        self.assertIsInstance(hashed_password, str)
        self.assertNotEqual(hashed_password, password)  # Ensure the password is hashed

    def test_create_access_token(self):
        # Test that the function returns a valid JWT token
        data = {"sub": "testuser"}
        token = create_access_token(data)
        self.assertIsInstance(token, str)

        # Decode the token to verify its contents
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded_token["sub"], data["sub"])
        self.assertIn("exp", decoded_token)  # Ensure the token has an expiration time

    def test_create_access_token_with_expires_delta(self):
        # Test that the function respects the provided expiration delta
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta=expires_delta)

        # Decode the token to verify its expiration time
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expected_exp = datetime.now(timezone.utc) + expires_delta
        actual_exp = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
        self.assertAlmostEqual(actual_exp, expected_exp, delta=timedelta(seconds=1))
