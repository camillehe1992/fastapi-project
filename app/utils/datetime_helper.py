from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+


class DateTimeHelper:
    """
    A helper class for working with dates, times, and time zones.
    """

    def __init__(self, timezone: str = "UTC"):
        """
        Initialize the DateTimeHelper with a default time zone.

        :param timezone: The default time zone (e.g., "UTC", "Asia/Shanghai").
        """
        self.timezone = ZoneInfo(timezone)

    def now(self) -> datetime:
        """
        Get the current time in the default time zone.

        :return: Current datetime in the default time zone.
        """
        return datetime.now(self.timezone)

    def to_timezone(self, dt: datetime, timezone: str) -> datetime:
        """
        Convert a datetime object to a different time zone.

        :param dt: The datetime object to convert.
        :param timezone: The target time zone (e.g., "Asia/Shanghai").
        :return: Datetime object in the target time zone.
        """
        target_timezone = ZoneInfo(timezone)
        return dt.astimezone(target_timezone)

    def format(self, dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S %Z%z") -> str:
        """
        Format a datetime object as a human-readable string.

        :param dt: The datetime object to format.
        :param fmt: The format string (default: "%Y-%m-%d %H:%M:%S %Z%z").
        :return: Formatted datetime string.
        """
        return dt.strftime(fmt)

    def parse(self, date_string: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """
        Parse a string into a datetime object.

        :param date_string: The string to parse.
        :param fmt: The format of the string (default: "%Y-%m-%d %H:%M:%S").
        :return: Parsed datetime object.
        """
        return datetime.strptime(date_string, fmt).replace(tzinfo=self.timezone)

    def iso_format(self, dt: datetime) -> str:
        """
        Get the ISO 8601 formatted string for a datetime object.

        :param dt: The datetime object to format.
        :return: ISO 8601 formatted string.
        """
        return dt.isoformat()

    def diff(self, dt1: datetime, dt2: datetime) -> float:
        """
        Calculate the difference between two datetime objects in seconds.

        :param dt1: The first datetime object.
        :param dt2: The second datetime object.
        :return: Difference in seconds.
        """
        return (dt1 - dt2).total_seconds()
