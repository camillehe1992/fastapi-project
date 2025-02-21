import os
import importlib
import unittest

import app.settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        # Clear any existing environment variables that might interfere with the tests
        self.original_env = os.environ
        os.environ.clear()

    def tearDown(self):
        # Restore the original environment variables after each test
        os.environ.update(self.original_env)

    def test_default_values(self):
        module = importlib.reload(app.settings)
        settings = module.Settings()

        # settings = Settings()
        self.assertEqual(settings.DEBUG, True)
        self.assertEqual(settings.TITLE, "RestAPI")
        self.assertEqual(settings.VERSION, "1.0.0")
        self.assertEqual(settings.NICKNAME, "fastapi")
        self.assertEqual(settings.SQLITE_CONNECTION_STRING, "sqlite:///sqlite.db")
        self.assertEqual(settings.ALGORITHM, "HS256")
        self.assertEqual(settings.ACCESS_TOKEN_EXPIRE_MINUTES, 3600)
        self.assertEqual(settings.ORIGINS, "")
        self.assertEqual(settings.POSTGRES_HOST, "127.0.0.1")
        self.assertIsNone(settings.SECRET_KEY)
        self.assertIsNone(settings.POSTGRES_DB)
        self.assertIsNone(settings.POSTGRES_USER)
        self.assertIsNone(settings.POSTGRES_PASSWORD)
        self.assertEqual(
            settings.POSTGRES_CONNECTION_STRING,
            "postgresql://None:None@127.0.0.1/None",
        )

    def test_custom_values(self):
        os.environ.update(
            {
                "DEBUG": "False",
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
        module = importlib.reload(app.settings)
        settings = module.Settings()

        self.assertEqual(settings.DEBUG, False)
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
