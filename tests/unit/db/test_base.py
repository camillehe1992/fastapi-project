import importlib
import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Import the module to be tested
from app.db.base import get_session


class TestDatabaseConfig(unittest.TestCase):

    @patch("app.db.base.settings.DEBUG", True)  # Mock DEBUG to True
    @patch(
        "app.db.base.settings.SQLITE_CONNECTION_STRING", "sqlite:///debug.db"
    )  # Mock SQLite connection string
    def test_database_url_debug_mode(self):
        """
        Test that SQLALCHEMY_DATABASE_URL is set to SQLITE_CONNECTION_STRING when DEBUG is True.
        """
        import app.db.base

        importlib.reload(app.db.base)

        # Assert
        self.assertEqual(app.db.base.SQLALCHEMY_DATABASE_URL, "sqlite:///debug.db")

    @patch("app.db.base.settings.DEBUG", False)  # Mock DEBUG to False
    @patch(
        "app.db.base.settings.POSTGRES_CONNECTION_STRING",
        "postgresql://user:password@localhost/db",
    )  # Mock Postgres connection string
    def test_database_url_production_mode(self):
        """
        Test that SQLALCHEMY_DATABASE_URL is set to POSTGRES_CONNECTION_STRING when DEBUG is False.
        """
        # Reload the module to apply the mocked settings
        import importlib
        import app.db.base  # Replace 'your_module' with the actual module name

        importlib.reload(app.db.base)

        # Assert
        self.assertEqual(
            app.db.base.SQLALCHEMY_DATABASE_URL,
            "postgresql://user:password@localhost/db",
        )

    @patch("app.db.base.SessionLocal")
    def test_get_session(self, mock_session_local):
        """
        Test the get_session function.
        """
        # Mock the session
        mock_session = MagicMock(spec=Session)
        mock_session_local.return_value = mock_session

        # Call get_session and verify the session is yielded and closed
        db_gen = get_session()
        db = next(db_gen)

        # Verify the session is yielded
        self.assertEqual(db, mock_session)

        # Simulate the end of the context manager
        with self.assertRaises(StopIteration):
            next(db_gen)

        # Verify the session is closed
        mock_session.close.assert_called_once()
