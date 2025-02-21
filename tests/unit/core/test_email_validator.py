import unittest
from fastapi import HTTPException, status
from app.core.email_validator import validate_email


class TestValidateEmail(unittest.TestCase):

    def test_valid_email(self):
        # Test valid email addresses
        valid_emails = [
            "test@example.com",
            "user.name+tag+sorting@example.com",
            "user@sub.example.com",
        ]
        for email in valid_emails:
            try:
                validate_email(email)
            except HTTPException:
                self.fail(
                    f"validate_email() raised HTTPException unexpectedly for {email}"
                )

    def test_invalid_email(self):
        # Test invalid email addresses
        invalid_emails = [
            "invalid-email",
            "user@.com",
            "user@com",
            "user@.com.",
            "@example.com",
        ]
        for email in invalid_emails:
            with self.assertRaises(HTTPException) as context:
                validate_email(email)
            self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(context.exception.detail, "Invalid email address")
