"""Data utility functions for dashboard."""

import csv
import pandas as pd
import streamlit as st

IMAGES_FILE_PATH = 'image_data_STATIC.csv'
LOCS_FILE_PATH = 'origin_data_STATIC.csv'


def get_plant_images():
    """Returns available plant images as dict."""

    plant_dict = {}
    with open(IMAGES_FILE_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'upgrade' not in row['regular_url']:
                plant_id = int(row['plant_id'])
                regular_url = row['regular_url']
                plant_dict[plant_id] = regular_url

    return plant_dict


def get_origin_locations() -> pd.DataFrame:
    """Returns dataframe of origin locations."""

    return pd.read_csv(LOCS_FILE_PATH)
