"""Unit tests for extract.py"""
import pandas as pd
from extract import get_recording_data, get_watering_data, transform


def test_get_recording_data_one_valid_keys():
    """Test the function changes the temperature key present and returns None for the rest."""
    data = {'botanist': 'jane', 'key': 'value', 'temperature': 12}
    assert get_recording_data(data) == {
        'plant_id': None, 'soil_moisture': None, 'temperature': 12, 'recording_taken': None}


def test_get_watering_data_no_valid_keys():
    """Test the function has None for each value if no relevant keys."""
    data = {'botanist': 'jane', 'key': 'value', 'temperature': 12}
    assert get_watering_data(data) == {
        'plant_id': None, 'last_watered': None}


def test_transform_function():
    """Test that column names are changed correctly."""
    data = {'recording_taken': 'Wed, 20 Dec 2023 14:03:04 GMT'}
    recording_df = pd.DataFrame(data, index=[0, 1])
    data = {'last_watered': 'Wed, 20 Dec 2023 14:03:04 GMT',
            'another_column': 'testing'}
    watering_df = pd.DataFrame(data, index=[0, 1])

    recordings, waterings = transform(recording_df, watering_df)

    expected_recording_columns = ['datetime']
    assert list(recordings.columns) == expected_recording_columns

    expected_watering_columns = ['datetime', 'another_column']
    assert list(waterings.columns) == expected_watering_columns
