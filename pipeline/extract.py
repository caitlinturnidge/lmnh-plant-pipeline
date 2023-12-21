"""Script to extract and clean API data."""
import logging
import pandas as pd
from requests import get
from time
import concurrent.futures

BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
NO_OF_PLANTS = 51


def set_up_logger():
    """Set up a logger, to log pipeline progress to the console."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('logger')


def get_plant_data(plant_id: int) -> dict:
    """Gets plant data from API using ID."""
    logger = set_up_logger()
    api_data = get(BASE_URL + str(plant_id), timeout=100).json()
    if 'error' in api_data:
        logger.info("Error: %s", api_data.get('error'))
    return api_data


def get_recording_data(data: dict) -> dict:
    """Returns recording data as dictionary."""
    relevant_cols = ['plant_id', 'soil_moisture',
                     'temperature', 'recording_taken']
    return {key: data.get(key) for key in relevant_cols}


def get_watering_data(data: dict) -> dict:
    """Returns watering data as dictionary."""
    relevant_cols = ['plant_id', 'last_watered']
    return {key: data.get(key) for key in relevant_cols}


def extract():
    """Function to extract all the soil moisture and temperature readings and save them to dataframes."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        all_data_list = list(executor.map(get_plant_data, range(NO_OF_PLANTS)))

    df = pd.DataFrame(all_data_list)

    recordings = df[['plant_id', 'soil_moisture',
                    'temperature', 'recording_taken']]
    waterings = df[['plant_id', 'last_watered']]

    recording_df = pd.DataFrame(recordings).dropna()
    watering_df = pd.DataFrame(waterings).dropna()

    return recording_df, watering_df


if __name__ == "__main__":
    extract()
