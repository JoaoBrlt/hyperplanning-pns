# Data.
import pandas as pd

# Schedules.
from schedule import Schedule
from location import Location

# Dates.
from datetime import datetime
from helper import Helper

# Colors.
from colorama import Fore, Style


class Classroom:
    """
    Represents a classroom on the schedule system.
    """

    def __init__(
        self,
        name: str,
        description: str,
        floor: int,
        sub_building: Location,
        building: Location,
        location: Location,
        places: int,
        outlets: int,
        computers: int,
        projector: bool,
        audio: bool
    ):
        """
        Initializes the classroom.

        :param name: The classroom name.
        :param description: The classroom description.
        :param floor: The classroom floor in the building.
        :param sub_building: The sub-building in which the classroom is located.
        :param building: The building in which the classroom is located.
        :param location: The campus in which the classroom is located.
        :param places: The number of seats in the classroom.
        :param outlets: The number of outlets in the classroom.
        :param computers: The number of computers in the classroom.
        :param projector: Whether the classroom has a projector.
        :param audio: Whether the classroom has an audio system.
        """
        # Initialize the attributes.
        self.name = name
        self.description = description
        self.floor = floor
        self.sub_building = sub_building
        self.building = building
        self.location = location
        self.places = places
        self.outlets = outlets
        self.computers = computers
        self.projector = projector
        self.audio = audio
        self.schedule = None

    def set_schedule(self, info: dict):
        """
        Sets the classroom schedule.

        :param info: The schedule information.
        """
        self.schedule = Schedule(info["id"], info["folder"], info["url"], info["reload"])

    def is_available(self, date: datetime = datetime.now()):
        """
        Checks if the schedule is free at a given datetime.

        :param date: The datetime to check.
        :return: Whether the schedule is free at the given datetime.
        """
        return self.schedule.is_available(date)

    def get_current_course(self, date: datetime = datetime.now()):
        """
        Returns the current course at a given datetime, if any.

        :param date: The datetime to check.
        :return: The current course, if any.
        """
        return self.schedule.get_current_course(date)

    def get_next_course(self, date: datetime = datetime.now()):
        """
        Returns the next course at a given datetime, if any.

        :param date: The datetime to check.
        :return: The next course, if any.
        """
        return self.schedule.get_next_course(date)

    def get_available_duration(self, date: datetime = datetime.now()):
        """
        Returns the duration until the next course, if any.
        Hypothesis: The classroom is available.

        :param date: The datetime to check.
        :return: The duration until the next course, if any.
        """
        return self.schedule.get_available_duration(date)

    def get_unavailable_duration(self, date: datetime = datetime.now()):
        """
        Returns the duration until the next course, if any.
        Hypothesis: The classroom is unavailable.

        :param date: The datetime to check.
        :return: The duration until the next course, if any.
        """
        return self.schedule.get_unavailable_duration(date)

    def get_minimum_information(self, date: datetime = datetime.now(), color: bool = False):
        """
        Returns the minimum information about the classroom.

        :param date: The datetime to check for availability.
        :param color: Whether to color the output.
        :return: The minimum information about the classroom.
        """
        return "{color}{name}{reset}".format(
            color=(Fore.GREEN if self.is_available(date) else Fore.RED) if color else "",
            name=self.name,
            reset=Style.RESET_ALL if color else ""
        )

    def get_regular_information(self, date: datetime = datetime.now(), color: bool = False):
        """
        Returns the regular information about the classroom.

        :param date: The datetime to check for availability.
        :param color: Whether to color the output.
        :return: The regular information about the classroom.
        """
        # Name.
        result = "{color}{name}{reset} | ".format(
            color=(Fore.GREEN if self.is_available(date) else Fore.RED) if color else "",
            name=self.name,
            reset=Style.RESET_ALL if color else ""
        )

        # Building.
        if self.building is not None:
            result += "{building} | ".format(
                building=self.building
            )

        # Location.
        if self.location is not None:
            result += "{location} | ".format(
                location=self.location
            )

        # Available.
        if self.is_available(date):
            result += "{color}Available{reset} for {duration}".format(
                color=Fore.GREEN if color else "",
                reset=Style.RESET_ALL if color else "",
                duration=Helper.format_duration(self.get_available_duration(date))
            )

        # Unavailable.
        else:
            result += "{color}Unavailable{reset} for {duration}".format(
                color=Fore.RED if color else "",
                reset=Style.RESET_ALL if color else "",
                duration=Helper.format_duration(self.get_unavailable_duration(date))
            )

        return result

    def get_full_information(self, date: datetime = datetime.now(), color: bool = False):
        """
        Returns the full information about the classroom.

        :param date: The datetime to check for availability.
        :param color: Whether to color the output.
        :return: The full information about the classroom.
        """
        # Colors.
        label_color = Fore.BLUE if color else ""
        reset_color = Style.RESET_ALL if color else ""

        # Name.
        result = "{color}Name{reset}: {color2}{name}{reset}\n".format(
            color=label_color,
            color2=(Fore.GREEN if self.is_available(date) else Fore.RED) if color else "",
            name=self.name,
            reset=reset_color
        )

        # Description.
        if pd.notna(self.description):
            result += "{color}Description{reset}: {description}\n".format(
                color=label_color,
                description=self.description,
                reset=reset_color
            )

        # Floor.
        result += "{color}Floor{reset}: {floor}\n".format(
            color=label_color,
            floor=str(int(self.floor)),
            reset=reset_color
        )

        # Sub-building.
        if self.sub_building is not None:
            result += "{color}Sub-building{reset}: {sub_building}\n".format(
                color=label_color,
                sub_building=self.sub_building,
                reset=reset_color
            )

        # Building.
        if self.building is not None:
            result += "{color}Building{reset}: {building}\n".format(
                color=label_color,
                building=self.building,
                reset=reset_color
            )

        # Location.
        if self.location is not None:
            result += "{color}Location{reset}: {location}\n".format(
                color=label_color,
                location=self.location,
                reset=reset_color
            )

        # Places.
        if pd.notna(self.places):
            result += "{color}Places{reset}: {places}\n".format(
                color=label_color,
                places=str(int(self.places)),
                reset=reset_color
            )

        # Outlets.
        if pd.notna(self.outlets):
            result += "{color}Outlets{reset}: {outlets}\n".format(
                color=label_color,
                outlets=str(int(self.outlets)),
                reset=reset_color
            )

        # Computers.
        if pd.notna(self.computers):
            result += "{color}Computers{reset}: {computers}\n".format(
                color=label_color,
                computers=str(int(self.computers)),
                reset=reset_color
            )

        # Projector.
        result += "{color}Projector{reset}: {projector}\n".format(
            color=label_color,
            projector="Yes" if self.projector else "No",
            reset=reset_color
        )

        # Audio.
        result += "{color}Audio{reset}: {audio}\n".format(
            color=label_color,
            audio="Yes" if self.audio else "No",
            reset=reset_color
        )

        # Available.
        if self.is_available(date):
            # Status.
            result += "{color}Available{reset}: {color2}Yes{reset}\n".format(
                color=label_color,
                color2=Fore.GREEN if color else "",
                reset=reset_color
            )

            # Duration.
            result += "{color}Available duration{reset}: {duration}\n".format(
                color=label_color,
                duration=Helper.format_duration(self.get_available_duration(date)),
                reset=reset_color
            )

            # Next course.
            next_course = self.get_next_course(date)
            if next_course is not None:
                result += "{color}Next course{reset}: {next_course}".format(
                    color=label_color,
                    next_course=next_course,
                    reset=reset_color
                )

        # Unavailable.
        else:
            # Status.
            result += "{color}Available: {color2}No{reset}\n".format(
                color=label_color,
                color2=Fore.RED if color else "",
                reset=reset_color
            )

            # Duration.
            result += "{color}Unavailable duration{reset}: {duration}".format(
                color=label_color,
                duration=Helper.format_duration(self.get_unavailable_duration(date)),
                reset=reset_color
            )

            # Next course.
            current_course = self.get_current_course(date)
            if current_course is not None:
                result += "{color}Current course{reset}: {current_course}".format(
                    color=label_color,
                    current_course=current_course,
                    reset=reset_color
                )

        return result
