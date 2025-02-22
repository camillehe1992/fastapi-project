import unittest
import pytest
from fastapi import status
from tests.conftest import generate_random_username

# Define API_PREFIX for todos and users
API_PREFIX_TODOS = "/api/v1/todos"
API_PREFIX_USERS = "/api/v1/users"


@pytest.mark.usefixtures("client")
class TestTodoEndpoints(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client  # Inject the client fixture

        # Generate a random username
        self.random_username = generate_random_username()

        self.email = f"{self.random_username}@example.com"
        self.password = "Mypassword@123"

        # Register and log in a user to get a valid token
        user_data = {
            "email": self.email,
            "password": self.password,
            "username": self.random_username,
        }

        # Register the user
        self.client.post(
            f"{API_PREFIX_USERS}/register",
            json=user_data,
        )

        # Log in the user to get the token
        login_data = {
            "email": self.email,
            "password": self.password,
        }
        login_response = self.client.post(
            f"{API_PREFIX_USERS}/login",
            json=login_data,
        )
        self.access_token = login_response.json()["access_token"]

    def test_create_new_todo(self):
        # Test data
        todo_data = {
            "title": "Test Todo",
            "completed": False,
        }

        # Make the request to the /api/v1/todos endpoint
        response = self.client.post(
            f"{API_PREFIX_TODOS}",
            json=todo_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Todo is created successfully.")
        self.assertEqual(response_data["data"]["title"], todo_data["title"])
        self.assertEqual(response_data["data"]["completed"], todo_data["completed"])

    def test_get_all_todos(self):
        # Make the request to the /api/v1/todos endpoint
        response = self.client.get(
            f"{API_PREFIX_TODOS}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("todos", response_data)
        self.assertIn("page", response_data)
        self.assertIn("page_size", response_data)
        self.assertIn("total_count", response_data)

    def test_get_todo_details(self):
        # Create a todo first
        todo_data = {
            "title": "Test Todo",
            "completed": False,
        }
        create_response = self.client.post(
            f"{API_PREFIX_TODOS}",
            json=todo_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        todo_id = create_response.json()["data"]["id"]

        # Make the request to the /api/v1/todos/{_id} endpoint
        response = self.client.get(
            f"{API_PREFIX_TODOS}/{todo_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["id"], todo_id)
        self.assertEqual(response_data["title"], todo_data["title"])
        self.assertEqual(response_data["completed"], todo_data["completed"])

    def test_delete_todo(self):
        # Create a todo first
        todo_data = {
            "title": "Test Todo",
            "completed": False,
        }
        create_response = self.client.post(
            f"{API_PREFIX_TODOS}",
            json=todo_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        todo_id = create_response.json()["data"]["id"]

        # Make the request to the /api/v1/todos/{_id} endpoint
        response = self.client.delete(
            f"{API_PREFIX_TODOS}/{todo_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Todo is deleted successfully.")
        self.assertEqual(response_data["data"]["id"], todo_id)

    def test_update_todo(self):
        # Create a todo first
        todo_data = {
            "title": "Test Todo",
            "completed": False,
        }
        create_response = self.client.post(
            f"{API_PREFIX_TODOS}",
            json=todo_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        todo_id = create_response.json()["data"]["id"]

        # Update data
        update_data = {
            "title": "Updated Todo",
            "completed": True,
        }

        # Make the request to the /api/v1/todos/{_id} endpoint
        response = self.client.put(
            f"{API_PREFIX_TODOS}/{todo_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Todo is updated successfully.")
        self.assertEqual(response_data["data"]["title"], update_data["title"])
        self.assertEqual(response_data["data"]["completed"], update_data["completed"])
