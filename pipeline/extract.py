"""Script to extract and clean API data."""
import logging
import requests
import pandas as pd

BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
NO_OF_PLANTS = 51


def set_up_logger():
    """Set up a logger, to log pipeline progress to the console."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('logger')


def get_plant_data(plant_id: int, session: requests.Session) -> dict:
    """Gets plant data from API using ID."""
    logger = set_up_logger()
    api_data = session.get(BASE_URL + str(plant_id), timeout=100).json()
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


def get_botanist_data(data: dict) -> dict:
    """Returns botanist data as dictionary."""
    return data.get('botanist')


def get_unique_botanists(botanist_list: list[dict]) -> list[dict]:
    """Filters unique botanists from full botanist list."""
    cleaned_data = [dict_item for dict_item in set(map(lambda x: tuple(
        x.items()) if x is not None else None, botanist_list)) if dict_item is not None]
    return [dict(tuple_data) for tuple_data in cleaned_data]


def get_plant_names(data: dict) -> dict:
    """Returns plant data as dictionary."""
    relevant_cols = ['plant_id', 'name', 'scientific_name']
    return {key: data.get(key) for key in relevant_cols}


def get_origin_data(data: dict) -> dict:
    """Returns origin data as dictionary."""
    if 'origin_location' in data:
        origin = data.get('origin_location')

        lat, lon = origin[0], origin[1]
        town, country_code = origin[2], origin[3]
        region = origin[-1].split('/')
        country, capital = region[0], region[1]

        origin_dict = {
            'lat': lat, 'lon': lon,
            'town': town, 'country_code': country_code,
            'country': country, 'capital': capital
        }
        return origin_dict
    return None


def extract():
    """Function to run the whole extract script."""

    logger = set_up_logger()
    recording_data_list, watering_data_list = [], []

    # Static data
    botanist_data_list = []
    plant_data_list = []
    origin_data_list = []
    image_data_list = []

    with requests.Session() as session:
        for plant_id in range(NO_OF_PLANTS):

            data = get_plant_data(plant_id, session)

            recording_data = get_recording_data(data)
            watering_data = get_watering_data(data)
            botanist_data = get_botanist_data(data)
            plant_data = get_plant_names(data)
            origin_data = get_origin_data(data)

            if plant_id % 5 == 0 and plant_id > 0:
                logger.info('Data has been retrieved for %s plants', plant_id)

            recording_data_list.append(recording_data)
            watering_data_list.append(watering_data)
            botanist_data_list.append(botanist_data)
            plant_data_list.append(plant_data)
            origin_data_list.append(origin_data)

    cleaned_botanist_data_list = get_unique_botanists(botanist_data_list)
    cleaned_origin_data_list = [
        origin for origin in origin_data_list if origin]

    recording_df = pd.DataFrame(recording_data_list).dropna()
    watering_df = pd.DataFrame(watering_data_list).dropna()
    botanist_df = pd.DataFrame(cleaned_botanist_data_list)
    plant_df = pd.DataFrame(plant_data_list)
    origin_df = pd.DataFrame(cleaned_origin_data_list)

    recording_df['recording_taken'] = pd.to_datetime(
        recording_df['recording_taken'])
    recording_df = recording_df.rename(columns={'recording_taken': 'datetime'})
    watering_df['last_watered'] = pd.to_datetime(
        watering_df['last_watered']).dt.tz_localize(None)
    watering_df = watering_df.rename(columns={'last_watered': 'datetime'})

    recording_df.to_csv('recording_data_SAMPLE.csv', index=False)
    watering_df.to_csv('watering_data_SAMPLE.csv', index=False)
    botanist_df.to_csv('botanist_data_STATIC.csv', index=False)
    plant_df.to_csv('plant_name_data_STATIC.csv', index=False)
    origin_df.to_csv('origin_data_STATIC.csv', index=False)


if __name__ == "__main__":
    extract()
