import os
import importlib
from unittest import TestCase

import app.settings


class TestSettings(TestCase):
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


# def test_settings_default_values():
#     """
#     Test that the Settings class uses default values when environment variables are not set.
#     """
#     # Patch os.getenv before importing the module that contains Settings
#     with patch.dict("os.getenv", clear=True):
#         # Configure mock_getenv to return None for most keys, but return valid values for fields that require conversion
#         # mock_getenv.return_value = None
#         # mock_getenv.side_effect = lambda key, default=None: (
#         #     "3600" if key == "ACCESS_TOKEN_EXPIRE_MINUTES" else None
#         # )

#         settings = Settings()

#         # Assert default values
#         assert settings.DEBUG is True  # Default value
#         assert settings.TITLE == "RestAPI"  # Default value
#         assert settings.VERSION == "1.0.0"  # Default value
#         assert settings.NICKNAME == "fastapi"  # Default value
#         assert (
#             settings.SQLITE_CONNECTION_STRING == "sqlite:///sqlite.db"
#         )  # Default value
#         assert settings.SECRET_KEY is None  # Default value
#         assert settings.ALGORITHM == "HS256"  # Default value
#         assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 3600  # Default value
#         assert settings.ORIGINS == ""  # Default value
#         assert settings.POSTGRES_DB is None  # Default value
#         assert settings.POSTGRES_USER is None  # Default value
#         assert settings.POSTGRES_PASSWORD is None  # Default value
#         assert settings.POSTGRES_HOST == "127.0.0.1"  # Default value
#         assert (
#             settings.POSTGRES_CONNECTION_STRING
#             == "postgresql://None:None@127.0.0.1/None"  # Default value
#         )


# def test_settings_with_environment_variables_in_pytest_ini():
#     settings = Settings()

#     assert settings.DEBUG is False
#     assert settings.TITLE == "TestApp"
#     assert settings.VERSION == "1.0.0"
#     assert settings.NICKNAME == "testapp"
#     assert settings.SQLITE_CONNECTION_STRING == "sqlite:///test.db"
#     assert settings.SECRET_KEY == "testsecretkey"
#     assert settings.ALGORITHM == "HS256"
#     assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60
#     assert settings.ORIGINS == "http://localhost:3000"
#     assert settings.POSTGRES_DB == "testdb"
#     assert settings.POSTGRES_USER == "testuser"
#     assert settings.POSTGRES_PASSWORD == "testpassword"
#     assert settings.POSTGRES_HOST == "localhost"
#     assert (
#         settings.POSTGRES_CONNECTION_STRING
#         == "postgresql://testuser:testpassword@localhost/testdb"
#     )
