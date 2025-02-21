import unittest
from unittest.mock import patch, MagicMock, AsyncMock, call
from fastapi import Request
from fastapi.responses import JSONResponse

# Import the middleware to be tested
from app.middlewares.logging import log_requests_middleware


class TestLogRequestsMiddleware(unittest.IsolatedAsyncioTestCase):

    @patch("app.middlewares.logging.logger")
    async def test_log_requests_middleware_success(self, mock_logger):
        # Arrange
        mock_request = MagicMock(spec=Request)
        mock_request.method = "GET"
        mock_request.url = "http://test.com/endpoint"

        mock_response = JSONResponse(content={"message": "Success"}, status_code=200)
        mock_call_next = AsyncMock(return_value=mock_response)

        # Act
        response = await log_requests_middleware(mock_request, mock_call_next)

        # Assert
        # Verify that the logger was called with the correct messages
        mock_logger.info.assert_has_calls(
            [
                call(f"Incoming request: {mock_request.method} {mock_request.url}"),
                call(f"Outgoing response: {mock_response.status_code}"),
            ]
        )
        mock_call_next.assert_called_once_with(mock_request)
        self.assertEqual(response, mock_response)

    @patch("app.middlewares.logging.logger")
    async def test_log_requests_middleware_exception(self, mock_logger):
        # Arrange
        mock_request = MagicMock(spec=Request)
        mock_request.method = "POST"
        mock_request.url = "http://test.com/error-endpoint"

        mock_exception = Exception("Test exception")
        mock_call_next = AsyncMock(side_effect=mock_exception)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            await log_requests_middleware(mock_request, mock_call_next)

        # Verify that the exception was logged
        mock_logger.info.assert_called_once_with(
            f"Incoming request: {mock_request.method} {mock_request.url}"
        )
        mock_logger.error.assert_called_once_with(
            f"Request failed: {str(context.exception)}", exc_info=True
        )
        mock_call_next.assert_called_once_with(mock_request)
