import unittest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from app.settings import settings
from app.main import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        pass

    def test_app_initialization(self):
        self.assertIsInstance(app, FastAPI)
        self.assertEqual(app.debug, bool(settings.DEBUG))

    def test_middleware(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Add assertions to verify middleware behavior (e.g., logging, CORS)

    def test_router_endpoint(self):
        response = self.client.get("/api/v1/system/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_exception_handler(self):
        response = self.client.get("/non-existent-route")  # Trigger a 404 error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
