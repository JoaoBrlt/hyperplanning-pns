# Dates.
from datetime import datetime
from dateutil.tz import tz


class Course:
    """
    Represents a course of the schedule.
    """

    def __init__(self, description: str, start: datetime, end: datetime):
        """
        Initializes the course.

        :param description: The course description.
        :param start: The course start datetime.
        :param end: The course end datetime.
        """
        self.description = description
        self.start = start
        self.end = end

    def __str__(self):
        """
        Returns the string representation of the course.

        :return: The string representation of the course.
        """
        return "{description} | {start} - {end}".format(
            description=self.description,
            start=self.start.replace(tzinfo=tz.tzlocal()).strftime("%d/%m/%Y %Hh%M"),
            end=self.end.replace(tzinfo=tz.tzlocal()).strftime("%Hh%M")
        )
