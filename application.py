# Environment.
import os
from dotenv import load_dotenv

# Types.
from typing import List

# Hyperplanning.
from hyperplanning import Hyperplanning

# Classrooms.
from classroom import Classroom

# Dates.
from datetime import datetime
from helper import Helper


class Application:
    """
    Application.
    """

    @staticmethod
    def __format_request(hyperplanning: Hyperplanning, options: dict):
        """
        Formats a request.

        :param hyperplanning: The hyperplanning object.
        :param options: The request options.
        :return: The request description.
        """
        # Availability.
        if options["available"] is not None:
            if options["available"]:
                result = "Available classrooms "
            else:
                result = "Unavailable classrooms "
        else:
            result = "All classrooms "

        # Duration.
        if options["duration"] is not None:
            result += f"for at least {Helper.format_duration(options['duration'])} "

        # Name.
        if options["name"] is not None:
            result += f"named '{options['name']}' "

        # Floor.
        if options["floor"] is not None:
            result += f"on the floor {options['floor']} "

        # Sub-building.
        if options["sub_building"] is not None:
            if options["sub_building"] in hyperplanning.sub_buildings:
                sub_building = hyperplanning.sub_buildings[options["sub_building"]]
            else:
                sub_building = options["sub_building"]

            result += f"in the sub-building '{sub_building}' "

        # Building.
        if options["building"] is not None:
            if options["building"] in hyperplanning.buildings:
                building = hyperplanning.buildings[options["building"]]
            else:
                building = options["building"]

            result += f"in the building '{building}' "

        # Location.
        if options["location"] is not None:
            if options["location"] in hyperplanning.locations:
                location = hyperplanning.locations[options["location"]]
            else:
                location = options["location"]

            result += f"at the location '{location}' "

        # Places.
        if options["places"] is not None:
            result += f"with a minimum of {options['places']} places "

        # Outlets.
        if options["outlets"] is not None:
            result += f"with a minimum of {options['outlets']} outlets "

        # Computers.
        if options["computers"] is not None:
            result += f"with a minimum of {options['computers']} computers "

        # Projector.
        if options["projector"] is not None:
            if options["projector"]:
                result += "with a projector "
            else:
                result += "without a projector "

        # Audio.
        if options["audio"] is not None:
            if options["audio"]:
                result += "with an audio system "
            else:
                result += "without an audio system "

        return result + ":\n"

    @staticmethod
    def __format_classrooms(
        classrooms: List[Classroom],
        date: datetime = datetime.now(),
        verbose: int = 0,
        color: bool = False
    ):
        """
        Formats a list of classrooms.

        :param classrooms: The list of classrooms.
        :param date: The date to check for availability.
        :param verbose: The verbosity level of the output.
        :param color: Whether to use color on the output.
        :return: The formatted list of classrooms.
        """
        # No classrooms.
        if len(classrooms) == 0:
            return "No classrooms found."

        # Initialize the result.
        result = ""

        # Format the classrooms.
        for index, classroom in enumerate(classrooms):
            # Minimum.
            if verbose == 0:
                result += classroom.get_minimum_information(date, color)
                if index < len(classrooms) - 1:
                    result += ", "

            # Regular.
            elif verbose == 1:
                result += classroom.get_regular_information(date, color)
                if index < len(classrooms) - 1:
                    result += "\n"

            # Full.
            else:
                result += "=" * 40 + "\n"
                result += classroom.get_full_information(date, color) + "\n"
                result += "=" * 40
                if index < len(classrooms) - 1:
                    result += "\n"

        return result

    @staticmethod
    def get_classrooms(options: dict, color: bool = False):
        """
        Returns a formatted list of classrooms.

        :param options: The request options.
        :param color: Whether to use color on the output.
        :return: The formatted list of classrooms.
        """
        # Load the variables.
        load_dotenv()

        # Create the hyperplanning.
        hyperplanning = Hyperplanning(
            os.getenv("DATA_FOLDER"),
            os.getenv("SCHEDULE_FOLDER"),
            os.getenv("SCHEDULE_URL"),
            options["reload"]
        )

        # Get the description.
        result = Application.__format_request(hyperplanning, options)

        # Get the classrooms.
        classrooms = hyperplanning.get_classrooms(
            options["name"],
            options["floor"],
            options["sub_building"],
            options["building"],
            options["location"],
            options["places"],
            options["outlets"],
            options["computers"],
            options["projector"],
            options["audio"],
            options["available"],
            options["duration"],
            options["date"]
        )

        # Format the classrooms.
        result += Application.__format_classrooms(classrooms, options["date"], options["verbose"], color)

        return result
