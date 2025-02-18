from unittest import TestCase
from unittest.mock import Mock
from fastapi import FastAPI
from app.utils.openapi import (
    custom_openapi,
    settings,
)


class TestCustomOpenAPI(TestCase):

    def setUp(self):
        # Create a FastAPI app instance for testing
        self.app = FastAPI()

    def test_with_default_openapi(self):
        self.app.openapi_schema = Mock()
        schema = custom_openapi(self.app)
        self.assertEqual(schema, self.app.openapi_schema)

    def test_custom_openapi(self):
        # Call the custom_openapi function
        schema = custom_openapi(self.app)

        # Verify the schema contains the expected fields
        self.assertIsInstance(schema, dict)
        self.assertEqual(schema["info"]["title"], settings.TITLE)
        self.assertEqual(schema["info"]["version"], settings.VERSION)
        self.assertEqual(
            schema["info"]["description"], "A Swagger for FastAPI Application"
        )

        # Verify the securitySchemes are correctly added
        # self.assertIn("components", schema)
        self.assertIn("securitySchemes", schema["components"])
        self.assertEqual(
            schema["components"]["securitySchemes"]["OAuth2PasswordBearer"],
            {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",  # Optional: Specify the token format
            },
        )

        # Verify the schema is cached in the app instance
        self.assertEqual(self.app.openapi_schema, schema)
