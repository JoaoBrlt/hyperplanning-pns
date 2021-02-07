# Files.
import os
from urllib.request import urlretrieve

# Calendars.
import icalendar

# Courses.
from course import Course

# Dates.
from datetime import datetime, timedelta
from dateutil.tz import tz


class Schedule:
    """
    Represents the schedule of a classroom.
    """

    def __init__(self, identifier: str, folder: str, url: str, reload: bool = True):
        """
        Initializes the schedule.

        :param identifier: The schedule identifier.
        :param folder: The storage folder of the schedules.
        :param url: The URL pattern to download schedules.
        :param reload: Whether to force the reloading of schedules.
        """
        # Initialize the identifier.
        self.identifier = identifier

        # Initialize the path.
        self.path = "{folder}/{identifier}.ics".format(folder=folder, identifier=identifier)
        self.url = url.format(identifier=identifier)

        # Download the schedule.
        self.__download_schedule(self.url, self.path, folder, reload)

        # Load the schedule.
        self.courses = self.__load_schedule(self.path)

    @staticmethod
    def __download_schedule(url: str, path: str, folder: str, reload: bool = True):
        """
        Downloads a schedule file.

        :param url: The URL to download the schedule file.
        :param path: The storage path of the schedule file.
        :param folder: The storage folder of the schedules.
        :param reload: Whether to force the reloading of schedules.
        """
        # Create the parent folder.
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Download the schedule.
        if not os.path.exists(path) or reload:
            urlretrieve(url, path)

    @staticmethod
    def __load_schedule(path: str):
        """
        Loads the schedule from a schedule file.

        :param path: The storage path of the schedule file.
        :return: The list of scheduled courses.
        """
        # Read the schedule.
        file = open(path, "r")
        schedule = icalendar.Calendar.from_ical(file.read())

        # Save the courses.
        courses = []
        for component in schedule.walk():
            if component.name == "VEVENT":
                # Get the course.
                summary = component.get("summary")
                start = component.get("dtstart").dt
                end = component.get("dtend").dt

                # Validate the course.
                if isinstance(summary, str) and isinstance(start, datetime) and isinstance(end, datetime):
                    course = Course(summary, start, end)
                    courses.append(course)

        # Sort the courses by start date.
        courses.sort(key=lambda x: x.start)
        file.close()

        return courses

    def is_available(self, date: datetime = datetime.now()):
        """
        Checks if the schedule is free at a given datetime.

        :param date: The datetime to check.
        :return: Whether the schedule is free at the given datetime.
        """
        # Convert datetime to UTC timezone.
        date = date.astimezone(tz.tzutc())

        # Browse sorted courses.
        for course in self.courses:
            # Current course.
            if course.start <= date < course.end:
                return False
            # No current course.
            if date < course.start:
                return True
        # No current course.
        return True

    def get_current_course(self, date: datetime = datetime.now()):
        """
        Returns the current course at a given datetime, if any.

        :param date: The datetime to check.
        :return: The current course, if any.
        """
        # Convert datetime to UTC timezone.
        date = date.astimezone(tz.tzutc())

        # Browse sorted courses.
        for course in self.courses:
            # Current course.
            if course.start <= date < course.end:
                return course
            # No current course.
            if date < course.start:
                return None
        # No current course.
        return None

    def get_next_course(self, date: datetime = datetime.now()):
        """
        Returns the next course at a given datetime, if any.

        :param date: The datetime to check.
        :return: The next course, if any.
        """
        # Convert datetime to UTC timezone.
        date = date.astimezone(tz.tzutc())

        # Browse sorted courses.
        for course in self.courses:
            if date < course.start:
                return course
        return None

    def get_available_duration(self, date: datetime = datetime.now()):
        """
        Returns the duration until the next course, if any.
        Hypothesis: The schedule is free.

        :param date: The datetime to check.
        :return: The duration until the next course, if any.
        """
        # Convert datetime to UTC timezone.
        date = date.astimezone(tz.tzutc())

        # Duration until the next course.
        next_course = self.get_next_course(date)
        if next_course is not None:
            return next_course.start - date

        # No next course.
        return timedelta(365)

    def get_unavailable_duration(self, date: datetime = datetime.now()):
        """
        Returns the duration until the end of the current course, if any.
        Hypothesis: The schedule is not free.

        :param date: The datetime to check.
        :return: The duration until the end of the current course, if any.
        """
        # Convert datetime to UTC timezone.
        date = date.astimezone(tz.tzutc())

        # Duration until the end of the current course.
        current_course = self.get_current_course(date)
        if current_course is not None:
            return current_course.end - date

        # No current course.
        return timedelta(0)
