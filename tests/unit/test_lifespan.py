import unittest
from unittest.mock import patch
from fastapi import FastAPI

from app.lifespan import lifespan


@patch("app.lifespan.logger.info")
@patch("app.lifespan.create_tables")
class TestLifespan(unittest.IsolatedAsyncioTestCase):

    async def test_lifespan(self, mock_create_tables, mock_logger_info):
        # Create a mock FastAPI app
        app = FastAPI()
        # Call the lifespan function
        async with lifespan(app) as _:
            pass  # The application runs here

        # Verify startup logic
        mock_logger_info.assert_any_call("Creating database tables...")
        mock_create_tables.assert_called_once()

        # Verify shutdown logic
        mock_logger_info.assert_any_call("Shutting down...")
