"""Unit tests for extract.py"""
from extract import get_recording_data, get_watering_data


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


def test_get_watering_data_no_data():
    """Test the function has None for each value if no no data is given."""
    data = {}
    assert get_watering_data(data) == {
        'plant_id': None, 'last_watered': None}

