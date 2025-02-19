from unittest import TestCase
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Import the module to be tested
from app.db.base import engine, get_db, SessionLocal


class TestDatabaseConfig(TestCase):

    # @patch("app.settings.settings")
    # @patch("app.db.base.create_engine")
    # def test_database_url_configuration(self, mock_create_engine, mock_settings):
    #     """
    #     Test that the correct database URL is used based on the DEBUG setting.
    #     """
    #     # Test case 1: DEBUG is True (SQLite)
    #     mock_settings.DEBUG = True
    #     mock_settings.SQLITE_CONNECTION_STRING = "sqlite:///test.db"
    #     mock_settings.POSTGRES_CONNECTION_STRING = (
    #         "postgresql://user:password@localhost/dbname"
    #     )

    #     # Re-import the module to reinitialize the engine with the mocked settings
    #     with patch.dict("sys.modules", {"app.db.base": MagicMock()}):
    #         import app.db.base

    #         app.db.base.engine = create_engine(mock_settings.SQLITE_CONNECTION_STRING)

    #     # Verify the engine was created with the SQLite connection string
    #     # mock_create_engine.assert_called_once_with(
    #     #     mock_settings.SQLITE_CONNECTION_STRING
    #     # )

    #     # Test case 2: DEBUG is False (PostgreSQL)
    #     mock_create_engine.reset_mock()  # Reset the mock for the next test case
    #     mock_settings.DEBUG = False

    #     # Re-import the module to reinitialize the engine with the mocked settings
    #     with patch.dict("sys.modules", {"app.db.base": MagicMock()}):
    #         import app.db.base

    #         app.db.base.engine = create_engine(mock_settings.POSTGRES_CONNECTION_STRING)

    #     # Verify the engine was created with the PostgreSQL connection string
    #     mock_create_engine.assert_called_once_with(
    #         mock_settings.POSTGRES_CONNECTION_STRING
    #     )

    # @patch("app.db.base.settings")
    # @patch("app.db.base.sessionmaker")
    # def test_sessionmaker_configuration(self, mock_sessionmaker, mock_settings):
    #     """
    #     Test that sessionmaker is configured correctly.
    #     """
    #     mock_settings.DEBUG = False
    #     # Verify sessionmaker is called with the correct parameters
    #     mock_sessionmaker.assert_called_once_with(
    #         autocommit=False,
    #         autoflush=False,
    #         bind=engine,
    #     )

    @patch("app.db.base.SessionLocal")
    def test_get_db(self, mock_session_local):
        """
        Test the get_db function.
        """
        # Mock the session
        mock_session = MagicMock(spec=Session)
        mock_session_local.return_value = mock_session

        # Call get_db and verify the session is yielded and closed
        db_gen = get_db()
        db = next(db_gen)

        # Verify the session is yielded
        self.assertEqual(db, mock_session)

        # Simulate the end of the context manager
        with self.assertRaises(StopIteration):
            next(db_gen)

        # Verify the session is closed
        mock_session.close.assert_called_once()
