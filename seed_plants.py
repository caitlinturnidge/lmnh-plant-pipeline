
import requests
import pandas as pd


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(plant_id: int) -> list[dict]:
    """Gets plant data from API using ID."""
    return requests.get(BASE_URL + str(plant_id), timeout=100).json()


def parse_location(location_info: list) -> dict:
    """Turns a list with location info into a dictionary."""
    location = {}
    if not location_info:
        return location
    
    if len(location_info) == 5:
        location["latitude"] = location_info[0]
        location["longitude"] = location_info[1]
        location["town"] = location_info[2]
        location["country_code"] = location_info[3]
        location["continent"], location["city"] = location_info[4].split("/")
    return location


def generate_location_id(locations: list[dict]) -> int:
    """Finds the highest ID number and returns the following number in the sequence."""
    if not locations:
        return 1
    return int(max([loc["id"] for loc in locations]) + 1)


def cross_reference_location(location_info: list[str], unique_locations: list[dict]) -> int:
    """
    Checks if location has been stored before and adds it to the database if not.
    Returns the assigned ID to the location.
    """
    current_location = parse_location(location_info)
    if current_location == {}:
        return None
    
    current_lat = current_location["latitude"]
    current_long = current_location["longitude"]

    for location in unique_locations:
         if location["latitude"] == current_lat and location["longitude"] == current_long:
              return location["id"]
    
    current_location["id"] = generate_location_id(unique_locations)
    unique_locations.append(current_location)
    return current_location["id"]


def get_plant_details(data: dict, locations: list[dict]) -> dict:
    """Returns plant data as dictionary."""

    relevant_cols = ['plant_id', 'name', 'scientific_name', 'origin_location']

    details = {key: data.get(key) for key in relevant_cols}
    details["origin_location"] = cross_reference_location(details["origin_location"], locations)
    return details


if __name__ == "__main__":

    plant_info = []
    unique_locations = []

    for plant_id in range(51):
        result = get_plant_data(plant_id)
        details = get_plant_details(result, unique_locations)
        plant_info.append(details)
    
    
    location_details = pd.DataFrame(unique_locations)
    plant_details = pd.DataFrame(plant_info)
