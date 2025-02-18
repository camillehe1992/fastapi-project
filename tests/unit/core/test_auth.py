# import unittest
# from unittest.mock import MagicMock, patch

# from app.core.auth import get_current_user, get_user, User
# from tests.conftest import override_get_db

# MOCK_DB = override_get_db()


# # Unit Tests
# class TestGetUser(unittest.TestCase):

#     @patch("app.core.auth.Session")
#     def test_get_user_found(self, MOCK_DB):
#         # Mock the database session and query
#         mock_user = MagicMock(spec=User)
#         MOCK_DB.query.return_value.filter.return_value.first.return_value = mock_user

#         # Call the function
#         result = get_user(MOCK_DB, "test@example.com")

#         # Assertions
#         self.assertEqual(result, mock_user)
#         MOCK_DB.query.assert_called_once_with(User)
#         MOCK_DB.query.return_value.filter.assert_called_once_with(
#             User.email == "test@example.com"
#         )
#         MOCK_DB.query.return_value.filter.return_value.first.assert_called_once()

#     @patch("app.core.auth.Session")
#     def test_get_user_not_found(self, MOCK_DB):
#         # Mock the database session and query to return None
#         MOCK_DB.query.return_value.filter.return_value.first.return_value = None

#         # Call the function
#         result = get_user(MOCK_DB, "nonexistent@example.com")

#         # Assertions
#         self.assertIsNone(result)
#         MOCK_DB.query.assert_called_once_with(User)
#         MOCK_DB.query.return_value.filter.assert_called_once_with(
#             User.email == "nonexistent@example.com"
#         )
#         MOCK_DB.query.return_value.filter.return_value.first.assert_called_once()
