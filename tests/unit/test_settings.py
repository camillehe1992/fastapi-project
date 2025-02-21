import os
import importlib
import unittest
from unittest.mock import patch

import app.settings


@patch("app.settings.load_dotenv")
class TestSettings(unittest.TestCase):
    def setUp(self):
        # Clear any existing environment variables that might interfere with the tests
        self.original_env = os.environ
        os.environ.clear()

    def tearDown(self):
        # Restore the original environment variables after each test
        os.environ.update(self.original_env)

    def test_custom_values(self, mock_load_dotenv):
        os.environ.update(
            {
                "DEBUG": "False",
                "ENVIRONMENT": "local",
                "TITLE": "CustomAPI",
                "VERSION": "2.0.0",
                "NICKNAME": "customapi",
                "SQLITE_CONNECTION_STRING": "sqlite:///custom.db",
                "SECRET_KEY": "custom_secret",
                "ALGORITHM": "RS256",
                "ACCESS_TOKEN_EXPIRE_MINUTES": "7200",
                "ORIGINS": "http://example.com",
                "POSTGRES_HOST": "localhost",
                "POSTGRES_DB": "test_db",
                "POSTGRES_USER": "test_user",
                "POSTGRES_PASSWORD": "test_password",
            }
        )
        # Reload the module to reinitialize the Settings class with the patched os.getenv
        importlib.reload(app.settings)
        settings = app.settings.Settings()

        mock_load_dotenv.assert_not_called()
        self.assertEqual(settings.DEBUG, False)
        self.assertEqual(settings.ENVIRONMENT, "local")
        self.assertEqual(settings.TITLE, "CustomAPI")
        self.assertEqual(settings.VERSION, "2.0.0")
        self.assertEqual(settings.NICKNAME, "customapi")
        self.assertEqual(settings.SQLITE_CONNECTION_STRING, "sqlite:///custom.db")
        self.assertEqual(settings.SECRET_KEY, "custom_secret")
        self.assertEqual(settings.ALGORITHM, "RS256")
        self.assertEqual(settings.ACCESS_TOKEN_EXPIRE_MINUTES, 7200)
        self.assertEqual(settings.ORIGINS, "http://example.com")
        self.assertEqual(settings.POSTGRES_HOST, "localhost")
        self.assertEqual(settings.POSTGRES_DB, "test_db")
        self.assertEqual(settings.POSTGRES_USER, "test_user")
        self.assertEqual(settings.POSTGRES_PASSWORD, "test_password")
        self.assertEqual(
            settings.POSTGRES_CONNECTION_STRING,
            "postgresql://test_user:test_password@localhost/test_db",
        )
