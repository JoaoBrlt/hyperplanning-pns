# Regex.
import re

# Dates.
from datetime import datetime, timedelta


class Helper:
    """
    Helper for parsing and formatting.
    """

    @staticmethod
    def parse_datetime(text: str):
        """
        Parses a datetime.

        :param text: The input text.
        :return: The parsed datetime.
        """
        # Parse the input.
        try:
            return datetime.strptime(text, "%d/%m/%Y %Hh%M")

        # Invalid input.
        except ValueError:
            error = "Unable to parse a datetime from '{}'. ".format(text)
            error += "Example of valid datetime: '01/01/1970 08h00'."
            raise ValueError(error)

    @staticmethod
    def parse_duration(text: str):
        """
        Parses a duration.

        :param text: The input text.
        :return: The parsed duration.
        """
        # Parse the input.
        regex = re.compile(
            r'^((?P<days>[.\d]+?)d)?((?P<hours>[.\d]+?)h)?((?P<minutes>[.\d]+?)m)?((?P<seconds>[.\d]+?)s)?$')
        parts = regex.match(text)

        # Invalid input.
        if not parts:
            error = "Unable to parse a duration from '{}'. ".format(text)
            error += "Examples of valid durations: '4h', '5m34s', '10d8h5m20s'."
            raise ValueError(error)

        # Create the duration.
        time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
        return timedelta(**time_params)

    @staticmethod
    def format_duration(duration: timedelta):
        """
        Formats a duration.

        :param duration: The duration to format.
        :return: The formatted duration.
        """
        # Initialize the result.
        result = []

        # Initialize the duration periods.
        seconds = int(duration.total_seconds())
        periods = [
            ('day', 86400),
            ('hour', 3600),
            ('minute', 60)
        ]

        # For each duration period.
        for period_name, period_seconds in periods:
            if seconds >= period_seconds:
                period_value, seconds = divmod(seconds, period_seconds)
                has_s = "s" if period_value > 1 else ""
                result.append("%s %s%s" % (period_value, period_name, has_s))

        return ", ".join(result)
