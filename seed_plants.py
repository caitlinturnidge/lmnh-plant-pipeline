
from os import environ

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(plant_id: int) -> list[dict]:
        """Gets plant data from API using ID."""
        return requests.get(BASE_URL + str(plant_id), timeout=100).json()


def parse_location(location_info: list) -> dict:
     """Turns a list with location info into a dictionary."""
     location = {}
     if len(location_info) == 5:
        location["latitute"] = location_info[0]
        location["longitude"] = location_info[1]
        location["town"] = location_info[2]
        location["country_code"] = location_info[3]
        location["continent"] = location_info[4]
     
     return location


def cross_reference_location(location_info: list, connection) -> int:
     """
     Checks if location has been stored before and adds it to the database if not.
     Returns the assigned ID to the location.
     """
     location_dict = parse_location(location_info)

     pass


def get_plant_details(data: dict) -> dict:
    """Returns plant data as dictionary."""

    relevant_cols = ['plant_id', 'name', 'scientific_name', 'origin_location']

    details = {key: data.get(key) for key in relevant_cols}
    
    if details.get("origin_location"):
      details["origin_location"] = cross_reference_location(details["origin_location"])
      
    return details


if __name__ == "__main__":

    plant_info = []

    for plant_id in range(51):
        plant_dict = get_plant_data(plant_id)
        print(plant_dict)
        print(type(plant_dict.get("origin_location")))

