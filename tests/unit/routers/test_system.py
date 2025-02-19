from unittest import TestCase
from unittest.mock import patch

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from app.routers.v1 import system

API_PREFIX = "/api/v1"


class TestSystemRouter(TestCase):
    def setUp(self):
        # Create a FastAPI app and include the router
        self.app = FastAPI()
        router = APIRouter(prefix=API_PREFIX)
        router.include_router(system.router)
        self.app.include_router(router)
        self.client = TestClient(self.app)

    def test_health_endpoint(self):
        """
        Test that the /system/health endpoint returns the correct response.
        """
        response = self.client.get(f"{API_PREFIX}/system/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("settings.settings.NICKNAME", "test_nickname")
    @patch("settings.settings.VERSION", "1.0.0")
    @patch("utils.datetime_helper.DateTimeHelper.now")
    @patch("utils.datetime_helper.DateTimeHelper.iso_format")
    def test_info_endpoint(self, mock_iso_format, mock_now):
        """
        Test that the /system/info endpoint returns the correct response.
        """
        # Mock the DateTimeHelper methods
        mock_now.return_value = "2025-02-19T12:00:00"
        mock_iso_format.return_value = "2025-02-19T12:00:00Z"

        response = self.client.get(f"{API_PREFIX}/system/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "nickname": "test_nickname",
                "version": "1.0.0",
                "iso_time": "2025-02-19T12:00:00Z",
            },
        )
