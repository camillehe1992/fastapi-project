import pytest
from unittest.mock import MagicMock, patch
from fastapi import Request
from fastapi.responses import JSONResponse

from app.middlewares import log_requests_middleware


# @patch("app.middlewares.logger.info")
# @pytest.mark.asyncio
# async def test_log_requests_middleware_success(mock_logger_info):
#     """
#     Test that the middleware logs the incoming request and outgoing response correctly.
#     """
#     # Mock the Request object
#     mock_request = MagicMock(spec=Request)
#     mock_request.method = "GET"
#     mock_request.url = "http://example.com"

#     # Mock the call_next function to return a response
#     mock_response = JSONResponse(content={"message": "Success"}, status_code=200)
#     mock_call_next = MagicMock(return_value=mock_response)

#     # Call the middleware
#     response = await log_requests_middleware(mock_request, mock_call_next)

#     # Assert that the logger was called with the correct messages
#     mock_logger_info.assert_any_call("Incoming request: GET http://example.com")
#     mock_logger_info.assert_any_call("Outgoing response: 200")

#     # Assert that the response is returned correctly
#     assert response == mock_response


@patch("app.middlewares.logger.error")
@patch("app.middlewares.logger.info")
@pytest.mark.asyncio
async def test_log_requests_middleware_exception(mock_logger_info, mock_logger_error):
    """
    Test that the middleware logs an exception when the request fails.
    """
    # Mock the Request object
    mock_request = MagicMock(spec=Request)
    mock_request.method = "GET"
    mock_request.url = "http://example.com"

    # Mock the call_next function to raise an exception
    mock_exception = Exception("Test exception")
    mock_call_next = MagicMock(side_effect=mock_exception)

    # Call the middleware and expect an exception
    with pytest.raises(Exception, match="Test exception"):
        await log_requests_middleware(mock_request, mock_call_next)

    # Assert that the logger was called with the correct messages
    mock_logger_info.assert_called_once_with(
        f"Incoming request: GET http://example.com"
    )
    mock_logger_error.assert_called_once_with(
        "Request failed: Test exception", exc_info=True
    )
