#!/usr/bin/env python

# System.
import os
from dotenv import load_dotenv

# Discord.
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand, CommandInvokeError
from discord_argparse import ArgumentConverter, OptionalArgument, InvalidArgumentValueError, UnknownArgumentError

# Utility.
from application import Application

# Dates.
from datetime import datetime
from helper import Helper


class CustomHelpCommand(DefaultHelpCommand):
    """
    Custom help command.
    """

    async def send_command_help(self, command):
        """
        Sends the output of the help command.
        """
        self.add_command_formatting(command)
        for key, param in command.clean_params.items():
            # The command has an argument converter.
            if isinstance(param.annotation, ArgumentConverter):
                arguments = param.annotation.arguments
                if not arguments:
                    continue

                # Add a section.
                self.paginator.add_line("Arguments:")
                max_size = max(len(name) for name in arguments)

                # Add the arguments.
                for name, argument in arguments.items():
                    entry = "{0}{1:<{width}} {2}".format(self.indent * " ", name, argument.doc, width=max_size)
                    self.paginator.add_line(self.shorten_text(entry))

        # Send the output.
        self.paginator.close_page()
        await self.send_pages()


# Load the token.
load_dotenv()


# Initialize the bot.
bot = commands.Bot(command_prefix='!', help_command=CustomHelpCommand())


# Initialize the argument parser.
hyperplanning_parser = ArgumentConverter(
    all=OptionalArgument(
        bool,
        doc="Shows all classrooms.",
        default=False
    ),
    available=OptionalArgument(
        bool,
        doc="Filters classrooms by availability.",
        default=True
    ),
    date=OptionalArgument(
        str,
        doc="Filters classrooms by availability at a specified date.",
        default=None
    ),
    duration=OptionalArgument(
        str,
        doc="Filters classrooms by minimum availability duration.",
        default=None
    ),
    name=OptionalArgument(
        str,
        doc="Filters classrooms by name.",
        default=None
    ),
    floor=OptionalArgument(
        int,
        doc="Filters classrooms by floor.",
        default=None
    ),
    sub_building=OptionalArgument(
        str,
        doc="Filters classrooms by sub-building.",
        default=None
    ),
    building=OptionalArgument(
        str,
        doc="Filters classrooms by building.",
        default=None
    ),
    location=OptionalArgument(
        str,
        doc="Filters classrooms by location.",
        default=None
    ),
    places=OptionalArgument(
        int,
        doc="Filters classrooms by minimum number of places.",
        default=None
    ),
    outlets=OptionalArgument(
        int,
        doc="Filters classrooms by minimum number of outlets.",
        default=None
    ),
    computers=OptionalArgument(
        int,
        doc="Filters classrooms by minimum number of computers.",
        default=None
    ),
    projector=OptionalArgument(
        bool,
        doc="Filters classrooms by projector availability.",
        default=None
    ),
    audio=OptionalArgument(
        bool,
        doc="Filters classrooms by audio system availability.",
        default=None
    ),
    reload=OptionalArgument(
        bool,
        doc="Forces the reloading of schedules.",
        default=True
    ),
    verbose=OptionalArgument(
        int,
        doc="Enables a more detailed output (from 0 to 2).",
        default=0
    )
)


@bot.event
async def on_ready():
    """
    Notifies the administrator that the bot is ready.
    """
    print(f"{bot.user.name} has been connected to Discord!")


@bot.command()
async def hyperplanning(ctx, *, options: hyperplanning_parser = hyperplanning_parser.defaults()):
    """
    Shows a list of available classrooms according to the specified filters.
    """
    # Default.
    for name in hyperplanning_parser.arguments.keys():
        if name not in options:
            options[name] = None

    # Date.
    if options["date"] is not None:
        options["date"] = Helper.parse_datetime(options["date"])
    else:
        options["date"] = datetime.now()

    # Duration.
    if options["duration"] is not None:
        options["duration"] = Helper.parse_duration(options["duration"])

    # Availability.
    if options["all"]:
        options["available"] = None

    # System.
    options["threads"] = 2 * os.cpu_count()
    options["color"] = False

    # Get the classrooms.
    result = Application.get_classrooms(options)

    # Send the classrooms.
    await ctx.send(result[:2000])


@hyperplanning.error
async def hyperplanning_error(ctx, error):
    """
    Handles errors that occur while processing hyperplanning hyperplanning.
    """
    # Unknown argument.
    if isinstance(error, UnknownArgumentError):
        await ctx.send(f"Unknown argument '{error.name}'.")

    # Invalid argument.
    elif isinstance(error, InvalidArgumentValueError):
        await ctx.send(f"Invalid argument value for parameter '{error.name}'.")

    # Command failure.
    elif isinstance(error, CommandInvokeError):
        # Invalid date or duration.
        if isinstance(error.original, ValueError):
            await ctx.send(error.original)

    # Other errors.
    else:
        await ctx.send("Unable to process your command.")
        print(error)


# Run the bot.
bot.run(os.getenv("DISCORD_TOKEN"))
