import unittest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the function to be tested
from app.middlewares.cors import add_cors_middleware


class TestAddCorsMiddleware(unittest.TestCase):
    @patch("app.middlewares.settings.DEBUG", True)  # Mock DEBUG to True
    def test_add_cors_middleware_debug_mode(self):
        """
        Test that the CORS middleware is added with allow_origins=["*"] when DEBUG is True.
        """
        # Arrange
        mock_app = MagicMock(spec=FastAPI)

        # Act
        add_cors_middleware(mock_app)

        # Assert
        mock_app.add_middleware.assert_called_once_with(
            CORSMiddleware,
            allow_origins=["*"],  # Should allow all origins in debug mode
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @patch("app.middlewares.settings.DEBUG", False)  # Mock DEBUG to False
    @patch(
        "app.middlewares.settings.ORIGINS",
        ["https://example.com", "https://another.com"],
    )  # Mock ORIGINS
    def test_add_cors_middleware_production_mode(self):
        """
        Test that the CORS middleware is added with allow_origins from settings.ORIGINS when DEBUG is False.
        """
        # Arrange
        mock_app = MagicMock(spec=FastAPI)

        # Act
        add_cors_middleware(mock_app)

        # Assert
        mock_app.add_middleware.assert_called_once_with(
            CORSMiddleware,
            allow_origins=[
                "https://example.com",
                "https://another.com",
            ],  # Should use ORIGINS in production mode
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @patch("app.middlewares.settings.DEBUG", False)  # Mock DEBUG to False
    @patch(
        "app.middlewares.settings.ORIGINS",
        ["https://example.com,", "https://another.com,"],
    )  # Mock ORIGINS with commas
    def test_add_cors_middleware_origins_stripped(self):
        """
        Test that the CORS middleware strips commas from ORIGINS when DEBUG is False.
        """
        # Arrange
        mock_app = MagicMock(spec=FastAPI)

        # Act
        add_cors_middleware(mock_app)

        # Assert
        mock_app.add_middleware.assert_called_once_with(
            CORSMiddleware,
            allow_origins=[
                "https://example.com",
                "https://another.com",
            ],  # Should strip commas from ORIGINS
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
