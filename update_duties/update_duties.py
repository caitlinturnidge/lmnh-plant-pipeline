"""
Module containing functions to update duty table in database according to current state of the API
data.
"""

from functools import partial

from dotenv import load_dotenv
import pandas as pd
import requests

import database_functions as dbf


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_api_botanist_name_by_plant_id(plant_id: int) -> list[dict]:
    """Gets plant data from API using ID."""
    api_botanist_info = requests.get(BASE_URL + str(plant_id),
                                     timeout=100).json().get('botanist', {})
    return api_botanist_info.get('name','').split()



def check_if_duty_exists_in_duties(plant_id: int, botanist_id: int, duties: pd.DataFrame) -> bool:
    """Returns whether there is a duty in dataframe matching both plant and botanist id."""
    return not duties[(duties['plant_id'] == plant_id) &
                      (duties['botanist_id'] == botanist_id)].empty


def cross_reference_api_and_db_duties():
    """Checks and updates duty table in db based on current API data."""
    database = dbf.MSSQL_Database()

    plant_ids = dbf.get_db_plant_ids(database)
    active_duties = dbf.get_active_duties(database)

    check_for_existing_duty = partial(check_if_duty_exists_in_duties, duties = active_duties)

    for plant_id in plant_ids:
        botanist_name = get_api_botanist_name_by_plant_id(plant_id)
        print(f'Checking duty for plant with id {plant_id}...')
        if len(botanist_name) == 2:
            botanist_id = dbf.get_botanist_by_name(botanist_name[0], botanist_name[1], database)[0]
            if not check_for_existing_duty(plant_id, botanist_id):
                dbf.add_duty(database, plant_id, botanist_id)


if __name__ == "__main__":
    load_dotenv()

    cross_reference_api_and_db_duties()
