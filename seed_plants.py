
import requests

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"

def get_plant_data(plant_id: int) -> list[dict]:
        """Gets plant data from API using ID."""
        return requests.get(BASE_URL + str(plant_id), timeout=100).json()


def parse_location()


def cross_reference_location(location_info: list) -> int:
     """
     Checks if location has been stored before and adds it to the database if not.
     Returns the assigned ID to the location.
     """
     pass


def get_plant_details(data: dict) -> dict:
    """Returns plant data as dictionary."""

    relevant_cols = ['plant_id', 'name', 'scientific_name', 'origin_location']

    details = {key: data.get(key) for key in relevant_cols}
    details["origin_location"] = cross_reference_location(details["origin_location"])
    return details


if __name__ == "__main__":

    plant_info = []

    for plant_id in range(51):
        get_plant_data(plant_id)