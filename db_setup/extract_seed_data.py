"""This script extracts data required for the plant & location tables in the database."""


import requests
import pandas as pd


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
LOCATION_LIST_LEN = 5
LAT_INDEX = 0
LONG_INDEX = 1
TOWN_INDEX = 2
COCO_INDEX = 3
CONTINENT_CITY_INDEX = 4
PLANT_RANGE = 51
GERTRUDE_ID = 1
CARL_ID = 2
ELIZA_ID = 3


def get_plant_data(plant_id: int) -> list[dict]:
    """Gets plant data from API using ID."""
    return requests.get(BASE_URL + str(plant_id), timeout=100).json()


def parse_location(location_info: list) -> dict:
    """Turns a list with location info into a dictionary."""
    location = {}
    if not location_info:
        return location

    if len(location_info) == LOCATION_LIST_LEN:
        location["latitude"] = location_info[LAT_INDEX]
        location["longitude"] = location_info[LONG_INDEX]
        location["town"] = location_info[TOWN_INDEX]
        location["country_code"] = location_info[COCO_INDEX]
        location["continent"], location["city"] = location_info[CONTINENT_CITY_INDEX].split("/")
    return location


def generate_location_id(locations: list[dict]) -> int:
    """Finds the highest ID number and returns the following number in the sequence."""
    if not locations:
        return None
    return int(max([loc["id"] for loc in locations]) + 1)


def cross_reference_location(location_info: list[str], unique_locations: list[dict]) -> int:
    """
    Checks if location has been stored before and adds it to the database if not.
    Returns the assigned ID to the location.
    """
    current_location = parse_location(location_info)
    if not current_location:
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
    if details["scientific_name"]:
        details["scientific_name"] = details["scientific_name"][0]
    details["origin_location"] = cross_reference_location(details["origin_location"], locations)
    return details


def get_duty_information(data: dict) -> dict:
    """Returns the associated duty for a given plant."""
    duty_dict = {}
    plant_id = data.get("plant_id")
    botanist = data.get("botanist")
    if not plant_id or not botanist:
        return None
    duty_dict["plant_id"] = plant_id
    botanist_name = botanist.get("name")
    if botanist_name == "Gertrude Jekyll":
        duty_dict["botanist_id"] = GERTRUDE_ID
    if botanist_name == "Carl Linnaeus":
        duty_dict["botanist_id"] = CARL_ID
    if botanist_name == "Eliza Andrews":
        duty_dict["botanist_id"] = ELIZA_ID
    
    return duty_dict
    

if __name__ == "__main__":

    plant_info = []
    unique_locations = []
    duties = []

    for plant_id in range(PLANT_RANGE):
        result = get_plant_data(plant_id)
        details = get_plant_details(result, unique_locations)
        duty_info = get_duty_information(result)
        if duty_info:
            duties.append(duty_info)
        plant_info.append(details)


    location_details = pd.DataFrame(unique_locations)
    plant_details = pd.DataFrame(plant_info)
    duty_details = pd.DataFrame(duties)

    location_details.to_csv("seed_locations.csv", index=False)
    plant_details.to_csv("seed_plants.csv", index=False)
    duty_details.to_csv("seed_duties.csv", index=False)
