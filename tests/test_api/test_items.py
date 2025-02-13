from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_item():
    response = client.post(
        "/api/v1/items/", json={"name": "Test Item", "description": "Test Description"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
