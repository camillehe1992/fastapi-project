import unittest
import pytest
from fastapi import status
from tests.conftest import generate_random_username

API_PREFIX = "/api/v1/users"


@pytest.mark.usefixtures("client")
class TestUserEndpoints(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

        # Generate a random username
        self.random_username = generate_random_username()

        self.email = f"{self.random_username}@example.com"
        self.password = "Mypassword@123"

        self.invalid_passwords = [
            "Short1!",
            "nopassword1!",
            "NoNumberPass!",
            "NoSpecialChar1",
        ]

    def test_register_user(self):
        # Test data
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }

        # Make the request to the /api/v1/users/register endpoint
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User is registered successfully.")
        self.assertEqual(response_data["data"]["email"], user_data["email"])
        self.assertEqual(response_data["data"]["username"], user_data["username"])

    def test_register_user_failure(self):
        # Test data
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }

        # Register user
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)
        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Register user again with same email
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)
        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Register user again with same username
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)
        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_invalid_password(self):
        # Test data

        for invalid_password in self.invalid_passwords:
            user_data = {
                "email": self.email,
                "password": invalid_password,
                "username": self.random_username,
            }

            # Make the request to the /api/v1/users/register endpoint
            response = self.client.post(f"{API_PREFIX}/register", json=user_data)

            # Assert the response
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_success(self):
        # Test data
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }
        login_data = {
            "email": self.email,
            "password": self.password,
        }

        # First register a new user
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then, login
        response = self.client.post(f"{API_PREFIX}/login", json=login_data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("access_token", response_data)
        self.assertIn("token_type", response_data)

    def test_login_user_failure_with_invalid_password(self):
        # Test data
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }
        login_data = {
            "email": self.email,
            "password": f"Invalid{self.password}",
        }

        # First register a new user
        self.client.post(f"{API_PREFIX}/register", json=user_data)

        # Then, attempt to login with invalid credentials
        response = self.client.post(f"{API_PREFIX}/login", json=login_data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Incorrect email or password")

    def test_login_user_failure_with_invalid_email(self):
        # Test data
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }
        login_data = {
            "email": f"Invalid{self.email}",
            "password": self.password,
        }

        # First register a new user
        self.client.post(f"{API_PREFIX}/register", json=user_data)

        # Then, attempt to login with invalid credentials
        response = self.client.post(f"{API_PREFIX}/login", json=login_data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Incorrect email or password")

    def test_get_me(self):
        # Test data
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }
        login_data = {
            "email": self.email,
            "password": self.password,
        }

        # First register a new user
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then, login to get the token
        login_response = self.client.post(f"{API_PREFIX}/login", json=login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.json()["access_token"]

        # Use the access_token to access the /api/v1/users/me endpoint
        response = self.client.get(
            f"{API_PREFIX}/me", headers={"Authorization": f"Bearer {access_token}"}
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["email"], user_data["email"])
        self.assertEqual(response_data["username"], user_data["username"])

        # Use invalid access_token to access the /api/v1/users/me endpoint
        response = self.client.get(
            f"{API_PREFIX}/me",
            headers={"Authorization": f"Bearer Invalid{access_token}"},
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
