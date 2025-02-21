import unittest
from unittest.mock import Mock, patch
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exception_handlers import global_exception_handler


class TestExceptionHandlers(unittest.IsolatedAsyncioTestCase):
    @patch("app.exception_handlers.logger.error")
    async def test_global_exception_handler(self, mock_logger_error):
        # Mock the Request object
        mock_request = Mock(spec=Request)

        # Mock the Exception
        mock_exception = Exception("Test exception")

        # Call the exception handler
        response = await global_exception_handler(mock_request, mock_exception)

        # Assert that the logger was called with the correct message
        mock_logger_error.assert_called_once_with(
            "Unhandled exception: Test exception", exc_info=True
        )

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        assert response.body == b'{"message":"An internal server error occurred."}'
