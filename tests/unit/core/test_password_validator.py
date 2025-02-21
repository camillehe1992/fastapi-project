import unittest
from fastapi import HTTPException, status
from app.core.password_validator import validate_password


class TestValidatePassword(unittest.TestCase):

    def test_valid_password(self):
        # Test a valid password
        valid_password = "ValidPass1!"
        try:
            validate_password(valid_password)
        except HTTPException:
            self.fail(
                "validate_password() raised HTTPException unexpectedly for a valid password"
            )

    def test_password_too_short(self):
        # Test a password that is too short
        short_password = "Short1!"
        with self.assertRaises(HTTPException) as context:
            validate_password(short_password)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "Password must be at least 8 characters long"
        )

    def test_password_no_uppercase(self):
        # Test a password without an uppercase letter
        no_uppercase_password = "nopassword1!"
        with self.assertRaises(HTTPException) as context:
            validate_password(no_uppercase_password)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail,
            "Password must contain at least one uppercase letter",
        )

    def test_password_no_number(self):
        # Test a password without a number
        no_number_password = "NoNumberPass!"
        with self.assertRaises(HTTPException) as context:
            validate_password(no_number_password)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "Password must contain at least one number"
        )

    def test_password_no_special_character(self):
        # Test a password without a special character
        no_special_char_password = "NoSpecialChar1"
        with self.assertRaises(HTTPException) as context:
            validate_password(no_special_char_password)

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail,
            "Password must contain at least one special character",
        )
