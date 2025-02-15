from fastapi.testclient import TestClient

from app.main import app
from app.core.auth import get_current_user
from tests.conftest import test_db

client = TestClient(app)

PREFIX = "api/v1/users"


def mock_get_current_user():
    return {
        "username": "John Doe",
        "email": "john.doe@example.com",
        "password": "Mypassword@123",
    }


app.dependency_overrides[get_current_user] = mock_get_current_user

# Test cases
# def test_user_register(client, test_db):
#     response = client.post(
#         f"{PREFIX}/register",
#         json={
#             "username": "John Doe",
#             "email": "john.doe@example.com",
#             "password": "Mypassword@123",
#         },
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["username"] == "John Doe"
#     assert data["email"] == "john.doe@example.com"
#     assert "id" in data


def test_get_me(client, test_db):
    headers = {"Authorization": f"Bearer fake-token"}
    response = client.get(f"{PREFIX}/me", headers=headers)
    print(response.json())
    assert response.status_code == 200
    me = response.json()
    assert me["username"] == "John Doe"
    assert me["email"] == "john.doe@example.com"


# def test_read_user(client, test_db):
#     # Create a user first
#     response = client.post(
#         f"{PREFIX}/users",
#         json={"name": "Alice", "email": "alice@example.com"},
#     )
#     user_id = response.json()["id"]

#     response = client.get(f"/users/{user_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Alice"
#     assert data["email"] == "alice@example.com"


# def test_read_user_not_found(client, test_db):
#     response = client.get(
#         f"{PREFIX}/users/123",
#     )
#     assert response.status_code == 404
#     assert response.json() == {"detail": "User not found"}
