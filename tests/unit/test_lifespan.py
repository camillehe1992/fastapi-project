import pytest
import unittest
from unittest.mock import patch
from fastapi import FastAPI

# from app.logger import logger
from app.lifespan import lifespan


@patch("db.utils.logger.info")
@patch("db.utils.create_tables")
class TestLifespan(unittest.TestCase):

    @pytest.mark.asyncio
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
