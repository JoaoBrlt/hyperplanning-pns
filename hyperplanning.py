# Data.
import pandas as pd

# Types.
from typing import List

# Classrooms.
from classroom import Classroom

# Locations.
from location import Location

# Dates.
from datetime import datetime, timedelta


class Hyperplanning:
    """
    Represents the schedule system of the school.
    """

    def __init__(self, data_folder: str, schedule_folder: str, schedule_url: str, schedule_reload: bool = True):
        """
        Initializes the hyperplanning.

        :param data_folder: The storage folder of the data files.
        :param schedule_folder: The storage folder of the schedules.
        :param schedule_url: The URL pattern to download the schedules.
        :param schedule_reload: Whether to force the reloading of schedules.
        """
        # Load the locations.
        self.sub_buildings = self.__load_locations(data_folder + "/sub_buildings.csv")
        self.buildings = self.__load_locations(data_folder + "/buildings.csv")
        self.locations = self.__load_locations(data_folder + "/locations.csv")

        # Load the classrooms.
        self.classrooms = self.__load_classrooms(
            data_folder + "/classrooms.csv",
            self.sub_buildings,
            self.buildings,
            self.locations,
            schedule_folder,
            schedule_url,
            schedule_reload
        )

    @staticmethod
    def __load_locations(path: str):
        """
        Loads the locations from a file.

        :param path: The storage path of the locations file.
        :return: The list of locations.
        """
        # Read the locations.
        locations_data = pd.read_csv(path)

        # Save the locations.
        locations = {}
        for index, row in locations_data.iterrows():
            # Not defined.
            if pd.isna(row["alias"]):
                locations[row["alias"]] = None
            # Defined.
            else:
                locations[row["alias"]] = Location(row["alias"], row["name"], row["indication"])

        return locations

    @staticmethod
    def __load_classrooms(
        path: str,
        sub_buildings: List[Location],
        buildings: List[Location],
        locations: List[Location],
        schedule_folder: str,
        schedule_url: str,
        schedule_reload: bool = True
    ):
        """
        Loads the classrooms from a file.

        :param path: The storage path of the classrooms file.
        :param sub_buildings: The dictionary of sub-buildings.
        :param buildings: The dictionary of buildings.
        :param locations: The dictionary of locations.
        :param schedule_folder: The storage folder of the schedules.
        :param schedule_url: The URL pattern to download the schedules.
        :param schedule_reload: Whether to force the reloading of schedules.
        :return: The list of classrooms.
        """
        # Read the classrooms.
        classrooms_data = pd.read_csv(path)

        # Save the classrooms.
        classrooms = []
        for index, row in classrooms_data.iterrows():
            classroom = Classroom(
                row["name"],
                row["description"],
                row["floor"],
                sub_buildings[row["sub_building"]],
                buildings[row["building"]],
                locations[row["location"]],
                row["places"],
                row["outlets"],
                row["computers"],
                row["projector"] == "Yes",
                row["audio"] == "Yes",
                row["schedule_id"],
                schedule_folder,
                schedule_url,
                schedule_reload
            )
            classrooms.append(classroom)

        return classrooms

    @staticmethod
    def __filter_by_availability(classrooms: List[Classroom], available: bool = True, date: datetime = datetime.now()):
        """
        Filters a list of classrooms by availability.

        :param classrooms: The list of classrooms to filter.
        :param available: Whether the classrooms need to be available.
        :param date: The datetime to check for availability.
        :return: The list of classrooms with the specified availability.
        """
        results = []
        for classroom in classrooms:
            if classroom.is_available(date) == available:
                results.append(classroom)
        return results

    @staticmethod
    def __filter_by_min_availability_duration(
        classrooms: List[Classroom],
        min_duration: timedelta,
        date: datetime = datetime.now()
    ):
        """
        Filters a list of classrooms by minimal availability duration.

        :param classrooms: The list of classrooms to filter.
        :param min_duration: The minimum availability duration.
        :param date: The datetime to check for availability.
        :return: The list of classrooms with the specified minimum availability duration.
        """
        results = []
        for classroom in classrooms:
            if classroom.is_available(date):
                duration = classroom.get_available_duration(date)
                if duration >= min_duration:
                    results.append(classroom)
        return results

    @staticmethod
    def __filter_by_location(classrooms: List[Classroom], location_type, location_value):
        """
        Filters a list of classrooms by location.

        :param classrooms: The list of classrooms to filter.
        :param location_type: The location type.
        :param location_value: The expected location.
        :return: The list of classrooms at the specified location.
        """
        results = []
        for classroom in classrooms:
            location = getattr(classroom, location_type)
            if location is not None and (location.name == location_value or location.alias == location_value):
                results.append(classroom)
        return results

    @staticmethod
    def __filter_by_value(classrooms: List[Classroom], value_name, expected_value):
        """
        Filters a list of classrooms by attribute value.

        :param classrooms: The list of classrooms to filter.
        :param value_name: The name of the attribute to check.
        :param expected_value: The expected value.
        :return: The list of classrooms with the specified attribute value.
        """
        results = []
        for classroom in classrooms:
            value = getattr(classroom, value_name)
            if not pd.isna(value) and value == expected_value:
                results.append(classroom)
        return results

    @staticmethod
    def __filter_by_min_value(classrooms: List[Classroom], value_name, min_value):
        """
        Filters a list of classrooms by minimal attribute value.

        :param classrooms: The list of classrooms to filter.
        :param value_name: The name of the attribute to check.
        :param min_value: The minimum value.
        :return: The list of classrooms with the specified minimal attribute value.
        """
        results = []
        for classroom in classrooms:
            value = getattr(classroom, value_name)
            if not pd.isna(value) and value >= min_value:
                results.append(classroom)
        return results

    def get_classrooms(
        self,
        name: str = None,
        floor: int = None,
        sub_building: Location = None,
        building: Location = None,
        location: Location = None,
        places: int = None,
        outlets: int = None,
        computers: int = None,
        projector: bool = None,
        audio: bool = None,
        available: bool = True,
        duration: timedelta = None,
        date: datetime = datetime.now(),
    ):
        """
        Returns a filtered list of classrooms.

        :param name: The name to find.
        :param floor: The floor to find.
        :param sub_building: The sub-building to find.
        :param building: The building to find.
        :param location: The location to find.
        :param places: The minimum number of places.
        :param outlets: The minimum number of outlets.
        :param computers: The minimum number of computers.
        :param projector: Whether the classroom has a projector.
        :param audio: Whether the classroom has an audio system.
        :param available: Whether the classroom must be available.
        :param duration: The minimum availability duration.
        :param date: The datetime to check for availability.
        :return: The filtered list of classrooms.
        """
        # Get the classrooms.
        results = self.classrooms

        # Filter by name.
        if name is not None:
            results = self.__filter_by_value(results, "name", name)

        # Filter by availability.
        if available is not None:
            results = self.__filter_by_availability(results, available, date)

        # Filter by duration.
        if duration is not None:
            results = self.__filter_by_min_availability_duration(results, duration, date)

        # Filter by floor.
        if floor is not None:
            results = self.__filter_by_value(results, "floor", floor)

        # Filter by sub-building.
        if sub_building is not None:
            results = self.__filter_by_location(results, "sub_building", sub_building)

        # Filter by building.
        if building is not None:
            results = self.__filter_by_location(results, "building", building)

        # Filter by location.
        if location is not None:
            results = self.__filter_by_location(results, "location", location)

        # Filter by places.
        if places is not None:
            results = self.__filter_by_min_value(results, "places", places)

        # Filter by outlets.
        if outlets is not None:
            results = self.__filter_by_min_value(results, "outlets", outlets)

        # Filter by computers.
        if computers is not None:
            results = self.__filter_by_min_value(results, "computers", computers)

        # Filter by projector.
        if projector is not None:
            results = self.__filter_by_value(results, "projector", projector)

        # Filter by audio.
        if audio is not None:
            results = self.__filter_by_value(results, "audio", audio)

        return results
