"""Script to extract and clean API data."""

import requests
import pandas as pd

BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'


def get_plant_data(plant_id: int) -> list[dict]:
    """Gets plant data from API using ID."""

    return requests.get(BASE_URL + str(plant_id), timeout=100).json()


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


if __name__ == "__main__":
    recording_data_list = []
    watering_data_list = []
    botanist_data_list = []
    plant_data_list = []
    location_data_list = []

    for plant_id in range(51):
        data = get_plant_data(plant_id)

        recording_data = get_recording_data(data)
        watering_data = get_watering_data(data)
        botanist_data = get_botanist_data(data)
        plant_data = get_plant_names(data)

        recording_data_list.append(recording_data)
        watering_data_list.append(watering_data)
        botanist_data_list.append(botanist_data)
        plant_data_list.append(plant_data)

        print(f'Retrieving data for plant {plant_id}')

    cleaned_botanist_data_list = get_unique_botanists(botanist_data_list)

    recording_df = pd.DataFrame(recording_data_list)
    watering_df = pd.DataFrame(watering_data_list)
    botanist_df = pd.DataFrame(cleaned_botanist_data_list)
    plant_df = pd.DataFrame(plant_data_list)

    print(botanist_df)
    print()
    print(plant_df)

    recording_df['recording_taken'] = pd.to_datetime(
        recording_df['recording_taken'])
    watering_df['last_watered'] = pd.to_datetime(
        watering_df['last_watered'])

    recording_df.to_csv('recording_data_SAMPLE.csv', index=False)
    watering_df.to_csv('watering_data_SAMPLE.csv', index=False)
    botanist_df.to_csv('botanist_data_SAMPLE.csv', index=False)

    print("DataFrames saved as CSV files.")
