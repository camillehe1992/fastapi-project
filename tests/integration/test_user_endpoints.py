import pytest
from fastapi import status

API_PREFIX = "/api/v1/users"


@pytest.mark.usefixtures("client")
class TestUserEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_register_user(self):
        # Test data
        user_data = {
            "email": "test@example.com",
            "password": "Mypassword@123",
            "username": "testuser",
        }

        # Make the request to the /api/v1/users/register endpoint
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)

        # Assert the response
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["message"] == "User is registered successfully."
        assert response_data["data"]["email"] == user_data["email"]
        assert response_data["data"]["username"] == user_data["username"]

    def test_register_user_already_exists(self):
        # Test data
        user_data = {
            "email": "test@example.com",
            "password": "Mypassword@123",
            "username": "testuser",
        }

        # Register the user for the first time
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Try to register the same user again
        response = self.client.post(f"{API_PREFIX}/register", json=user_data)

        # Assert the response status code
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), f"Expected 400, got {response.status_code}. Response: {response.json()}"

        # Assert the response message
        response_data = response.json()
        assert "detail" in response_data
        assert "already exists" in response_data["detail"].lower()

    def test_login_user(self):
        # Test data
        user_data = {
            "email": "test@example.com",
            "password": "Mypassword@123",
            "username": "testuser",
        }
        login_data = {
            "email": "test@example.com",
            "password": "Mypassword@123",
        }

        # First, register the user
        self.client.post(f"{API_PREFIX}/register", json=user_data)

        # Then, login
        response = self.client.post(f"{API_PREFIX}/login", json=login_data)

        # Assert the response
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data

    def test_get_me(self):
        # Test data
        user_data = {
            "email": "test@example.com",
            "password": "Mypassword@123",
            "username": "testuser",
        }

        # Register and login to get the token
        self.client.post(f"{API_PREFIX}/register", json=user_data)
        login_response = self.client.post(
            f"{API_PREFIX}/login",
            json={"email": user_data["email"], "password": user_data["password"]},
        )
        token = login_response.json()["access_token"]

        # Use the token to access the /api/v1/users/me endpoint
        response = self.client.get(
            f"{API_PREFIX}/me", headers={"Authorization": f"Bearer {token}"}
        )

        # Assert the response
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["email"] == user_data["email"]
        assert response_data["username"] == user_data["username"]
