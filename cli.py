#!/usr/bin/env python

# System.
import os

# Arguments.
import sys
import argparse

# Utility.
from application import Application

# Dates.
from datetime import datetime
from helper import Helper


class CLI:
    """
    Command-line interface.
    """

    @staticmethod
    def __parse_arguments(arguments):
        """
        Parses the arguments.

        :param arguments: The list of arguments.
        :return: The dictionary of options.
        """
        parser = argparse.ArgumentParser()

        # Availability.
        parser.add_argument("--all", dest="available", action="store_const", const=None,
                            help="show all classrooms")
        parser.add_argument("-a", "--available", dest="available", action="store_true",
                            help="show available classrooms only")
        parser.add_argument("-u", "--unavailable", dest="available", action="store_false",
                            help="show unavailable classrooms only")
        parser.set_defaults(available=True)

        # Date.
        parser.add_argument("-d", "--date", type=CLI.__parse_datetime, default=datetime.now(),
                            help="filter classrooms by availability at a specified date")

        # Duration.
        parser.add_argument("-t", "--duration", type=CLI.__parse_duration, default=None,
                            help="filter classrooms by minimum availability duration")

        # Name.
        parser.add_argument("-n", "--name", default=None, help="filter classrooms by name")

        # Location.
        parser.add_argument("-f", "--floor", type=int, default=None, help="filter classrooms by floor")
        parser.add_argument("-s", "--sub-building", default=None, help="filter classrooms by sub-building")
        parser.add_argument("-b", "--building", default=None, help="filter classrooms by building")
        parser.add_argument("-l", "--location", default=None, help="filter classrooms by location")

        # Places.
        parser.add_argument("-p", "--places", type=int, default=None,
                            help="filter classrooms by minimum number of places")

        # Outlets.
        parser.add_argument("-o", "--outlets", type=int, default=None,
                            help="filter classrooms by minimum number of outlets")

        # Computers.
        parser.add_argument("-c", "--computers", type=int, default=None,
                            help="filter classrooms by minimum number of computers")

        # Projector.
        parser.add_argument("--projector", dest="projector", action="store_true",
                            help="show classrooms with a projector")
        parser.add_argument("--no-projector", dest="projector", action="store_false",
                            help="show classrooms without a projector")
        parser.set_defaults(projector=None)

        # Audio.
        parser.add_argument("--audio", dest="audio", action="store_true",
                            help="show classrooms with an audio system")
        parser.add_argument("--no-audio", dest="audio", action="store_false",
                            help="show classrooms without an audio system")
        parser.set_defaults(audio=None)

        # Color.
        parser.add_argument("--color", dest="color", action="store_true",
                            help="enable the use of colors on the output")
        parser.add_argument("--no-color", dest="color", action="store_false",
                            help="disable the use of colors on the output")
        parser.set_defaults(color=True)

        # Reload.
        parser.add_argument("--reload", dest="reload", action="store_true",
                            help="force the reloading of schedules")
        parser.add_argument("--no-reload", dest="reload", action="store_false",
                            help="disable the reloading of schedules")
        parser.set_defaults(reload=True)

        # Verbose.
        parser.add_argument('-v', '--verbose', action='count', default=0,
                            help="enable a more detailed output")

        # Threads.
        parser.add_argument("-j", "--threads", type=int, default=2 * os.cpu_count(),
                            help="set the number of threads to use")

        # Parse the arguments.
        return vars(parser.parse_args(arguments))

    @staticmethod
    def __parse_datetime(text: str):
        """
        Parses a datetime.

        :param text: The input text.
        :return: The parsed datetime.
        """
        try:
            return Helper.parse_datetime(text)
        except ValueError as e:
            raise argparse.ArgumentTypeError(e)

    @staticmethod
    def __parse_duration(text: str):
        """
        Parses a duration.

        :param text: The input text.
        :return: The parsed duration.
        """
        try:
            return Helper.parse_duration(text)
        except ValueError as e:
            raise argparse.ArgumentTypeError(e)

    @staticmethod
    def run():
        """
        Runs the command-line interface.
        """
        # Parse the arguments.
        options = CLI.__parse_arguments(sys.argv[1:])

        # Get the classrooms.
        result = Application.get_classrooms(options)

        # Print the classrooms.
        print(result)


# Run the CLI.
CLI.run()
