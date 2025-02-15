from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import test_db

client = TestClient(app)

PREFIX = "api/v1/users"


def test_user_register(client, test_db):
    response = client.post(
        f"{PREFIX}/register",
        json={
            "username": "John Doe",
            "email": "john.doe@example.com",
            "password": "Mypassword@123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data


def test_user_login(client, test_db):
    response = client.post(
        f"{PREFIX}/login",
        json={
            "username": "John Doe",
            "password": "Mypassword@123",
        },
    )
    assert response.status_code == 200
    token = response.json()
    assert len(token["access_token"]) > 0
    assert token["token_type"] == "bearer"


def test_get_me(client, test_db):
    login_response = client.post(
        f"{PREFIX}/login",
        json={
            "username": "John Doe",
            "password": "Mypassword@123",
        },
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"{PREFIX}/me", headers=headers)
    assert response.status_code == 200
    current_user = response.json()
    assert current_user["username"] == "John Doe"
    assert current_user["email"] == "john.doe@example.com"


def test_delete_me(client, test_db):
    login_response = client.post(
        f"{PREFIX}/login",
        json={
            "username": "John Doe",
            "password": "Mypassword@123",
        },
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"{PREFIX}/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == True
