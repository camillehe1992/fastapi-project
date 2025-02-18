from unittest import TestCase
from datetime import datetime
from zoneinfo import ZoneInfo
from app.utils.datetime_helper import DateTimeHelper


class TestDateTimeHelper(TestCase):
    def setUp(self):
        """Initialize the DateTimeHelper with a default time zone for all tests."""
        self.helper = DateTimeHelper(timezone="UTC")

    def test_initialize_with_timezone(self):
        """Test Initialize the DateTimeHelpe with specific time zone.r"""
        self.helper = DateTimeHelper(timezone="Asia/Shanghai")

    def test_now(self):
        """Test the `now` method to ensure it returns the current time in the default time zone."""
        now = self.helper.now()
        self.assertIsInstance(now, datetime)
        self.assertEqual(now.tzinfo, ZoneInfo("UTC"))

    def test_to_timezone(self):
        """Test the `to_timezone` method to ensure it converts a datetime to the target time zone."""
        dt = datetime(2025, 2, 18, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        converted_dt = self.helper.to_timezone(dt, "Asia/Shanghai")
        self.assertEqual(converted_dt.tzinfo, ZoneInfo("Asia/Shanghai"))
        self.assertEqual(converted_dt.hour, 20)  # UTC+8

    def test_format(self):
        """Test the `format` method to ensure it formats a datetime object correctly."""
        dt = datetime(2025, 2, 18, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        formatted = self.helper.format(dt)
        self.assertEqual(formatted, "2025-02-18 12:00:00 UTC+0000")

    def test_parse(self):
        """Test the `parse` method to ensure it parses a string into a datetime object."""
        date_string = "2025-02-18 12:00:00"
        parsed_dt = self.helper.parse(date_string)
        self.assertEqual(
            parsed_dt, datetime(2025, 2, 18, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        )

    def test_iso_format(self):
        """Test the `iso_format` method to ensure it returns the ISO 8601 formatted string."""
        dt = datetime(2025, 2, 18, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        iso_string = self.helper.iso_format(dt)
        self.assertEqual(iso_string, "2025-02-18T12:00:00+00:00")

    def test_diff(self):
        """Test the `diff` method to ensure it calculates the difference between two datetimes in seconds."""
        dt1 = datetime(2025, 2, 18, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
        dt2 = datetime(2025, 2, 18, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
        diff = self.helper.diff(dt1, dt2)
        self.assertEqual(diff, 7200.0)  # 2 hours in seconds
