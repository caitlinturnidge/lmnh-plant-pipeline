
import requests

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(plant_id: int) -> list[dict]:
    """Gets plant data from API using ID."""
    return requests.get(BASE_URL + str(plant_id), timeout=100).json()


def 