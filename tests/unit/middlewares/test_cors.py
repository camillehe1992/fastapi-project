from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middlewares import add_cors_middleware

app = FastAPI()
add_cors_middleware(app)

client = TestClient(app)


@patch("app.middlewares.settings")
def test_cors_middleware_debug_mode(mock_settings):
    """
    Test that CORS headers are set correctly in debug mode.
    """
    mock_settings.DEBUG.return_value = True
    response = client.options("/", headers={"Origin": "http://example.com"})
    assert response.headers["access-control-allow-origin"] == "*"


# @patch("app.middlewares.settings")
# def test_cors_middleware_production_mode(mock_settings):
#     """
#     Test that CORS headers are set correctly in production mode.
#     """
#     mock_settings.DEBUG.return_value = False
#     mock_settings.ORIGINS.return_value = "http://example.com,http://localhost"

#     response = client.options("/", headers={"Origin": "http://example.com"})
#     assert response.headers["access-control-allow-origin"] == "http://example.com"
