# Data.
import pandas as pd


class Location:
    """
    Represents the location of a classroom.
    """

    def __init__(self, alias: str, name: str, indication: str):
        """
        Initializes the location.

        :param alias: The location alias.
        :param name: The location name.
        :param indication: An indication to find the location.
        """
        self.alias = alias
        self.name = name
        self.indication = indication

    def __str__(self):
        """
        Returns the string representation of the location.

        :return: The string representation of the location.
        """
        return "{name}{indication}".format(
            name=self.name,
            indication=" (" + self.indication + ")" if pd.notna(self.indication) else ""
        )
