"""Script to extract and clean API data."""
import logging
import pandas as pd
from requests import get

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
    logger = set_up_logger()
    recording_data_list, watering_data_list = [], []

    for plant_id in range(NO_OF_PLANTS):

        data = get_plant_data(plant_id)

        recording_data = get_recording_data(data)
        watering_data = get_watering_data(data)

        recording_data_list.append(recording_data)
        watering_data_list.append(watering_data)

        if plant_id % 5 == 0 and plant_id > 0:
            logger.info('Data has been retrieved for %s plants', plant_id)

    recording_df = pd.DataFrame(recording_data_list).dropna()
    watering_df = pd.DataFrame(watering_data_list).dropna()
    return recording_df, watering_df


if __name__ == "__main__":
    extract()
