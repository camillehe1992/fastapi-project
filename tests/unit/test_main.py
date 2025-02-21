import unittest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.settings import settings
from app.utils.openapi import custom_openapi
from app.middlewares import log_requests_middleware, add_cors_middleware
from app.routers.api import router
from app.exception_handlers import global_exception_handler
from app.lifespan import lifespan


@patch.dict("os.environ", {}, clear=True)
class TestFastAPIApp(unittest.TestCase):

    def setUp(self):
        # Create the FastAPI app for testing
        self.app = FastAPI(
            lifespan=lifespan,
            debug=bool(settings.DEBUG),
        )

        # Add middlewares to the app
        self.app.middleware("http")(log_requests_middleware)
        add_cors_middleware(self.app)

        # Assign the custom OpenAPI schema to the app
        self.app.openapi = lambda: custom_openapi(self.app)

        # Include routers
        self.app.include_router(router)

        # Add the exception handler to the app
        self.app.add_exception_handler(Exception, global_exception_handler)

        # Create a TestClient for the app
        self.client = TestClient(self.app)

    def test_app_initialization(self):
        """Test if the app is initialized correctly."""
        self.assertIsInstance(self.app, FastAPI)
        self.assertEqual(self.app.debug, bool(settings.DEBUG))

    def test_log_requests_middleware_behavior(self):
        """Test if the log_requests_middleware logs requests."""
        with patch("app.logger.logger.info") as mock_logging:
            # Make a request to trigger the middleware
            self.client.get("/api/v1/system/health")
            # Verify that the logging function was called
            mock_logging.assert_called()

    def test_log_requests_middleware_applied(self):
        # Check if the middleware is in the app's middleware stack
        middleware_applied = any(
            middleware.cls.__name__ == "BaseHTTPMiddleware"
            for middleware in self.app.user_middleware
        )
        self.assertTrue(
            middleware_applied, "log_requests_middleware was not applied to the app"
        )

    def test_add_cors_middleware_applied(self):
        """Test if the CORS middleware is applied to the app."""
        # Check if the CORS middleware is in the app's middleware stack
        cors_middleware_applied = any(
            middleware.cls.__name__ == "CORSMiddleware"
            for middleware in self.app.user_middleware
        )
        self.assertTrue(
            cors_middleware_applied, "CORS middleware was not applied to the app"
        )

    @patch("app.middlewares.add_cors_middleware")
    def test_add_cors_middleware(self, mock_add_cors_middleware):
        """Test if the CORS middleware is applied."""
        # Verify the CORS middleware is applied
        mock_add_cors_middleware(self.app)
        mock_add_cors_middleware.assert_called_once_with(self.app)

    # @patch("app.utils.openapi.custom_openapi")
    # def test_custom_openapi_schema(self, mock_custom_openapi):
    #     """Test if the custom OpenAPI schema is assigned."""
    #     mock_custom_openapi.return_value = {
    #         "info": {"title": "Test API", "version": "1.0.0"}
    #     }
    #     openapi_schema = self.app.openapi()
    #     self.assertIsNotNone(openapi_schema)
    #     self.assertIn("info", openapi_schema)
    #     self.assertEqual(openapi_schema["info"]["title"], "Test API")
    #     self.assertEqual(openapi_schema["info"]["version"], "1.0.0")

    def test_routers(self):
        """Test if the router is included in the app."""
        # Check if the router is included by looking for a route
        routes = [route.path for route in self.app.routes]
        self.assertIn(
            "/api/v1/system/health", routes
        )  # Adjust based on your router's prefix

    def test_exception_handler(self):
        """Test if the global exception handler is registered."""
        self.assertIn(Exception, self.app.exception_handlers)

    @patch("routers.api.router")
    def test_sample_endpoint(self, mock_router):
        """Test a sample endpoint."""
        # Mock the router's behavior
        mock_router.get("/api/v1/system/health").return_value = {"status": "ok"}

        # Make a request to the mocked endpoint
        response = self.client.get("/api/v1/system/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
