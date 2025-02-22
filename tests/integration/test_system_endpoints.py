import unittest
from fastapi.testclient import TestClient
from app.main import app

API_PREFIX = "/api/v1/system"


class TestSystemRouterIntegration(unittest.TestCase):

    def setUp(self):
        # Create a TestClient for the FastAPI app
        self.client = TestClient(app)

    def test_health_endpoint(self):
        # Test the /system/health endpoint
        response = self.client.get(f"{API_PREFIX}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_info_endpoint(self):
        # Test the /system/info endpoint
        response = self.client.get(f"{API_PREFIX}/info")
        self.assertEqual(response.status_code, 200)

        # Verify the response structure and values
        response_data = response.json()
        self.assertIn("nickname", response_data)
        self.assertIn("version", response_data)
        self.assertIn("iso_time", response_data)

        # Verify that the nickname and version match the settings
        from app.settings import settings

        self.assertEqual(response_data["nickname"], settings.NICKNAME)
        self.assertEqual(response_data["version"], settings.VERSION)

        # Verify that the iso_time is a valid ISO format datetime string
        from datetime import datetime

        try:
            datetime.fromisoformat(response_data["iso_time"])
        except ValueError:
            self.fail("iso_time is not a valid ISO format datetime string")
