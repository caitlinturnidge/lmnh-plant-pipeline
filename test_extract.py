"""Unit tests for extract.py"""
from extract import get_origin_data, get_plant_names, get_unique_botanists, get_botanist_data, get_recording_data


def test_get_origin_data_invalid():
    """Test no origin data found."""
    data = {'test': 'nothing'}
    assert get_origin_data(data) is None


def test_get_origin_data_valid():
    """Test function handles valid data correctly."""
    data = {'test': 'nothing', 'origin_location': [
        "1", "2", "Test", "BR", "Country/City"]}
    assert get_origin_data(data) == {
        'lat': '1', 'lon': '2',
        'town': 'Test', 'country_code': 'BR',
        'country': 'Country', 'capital': 'City'}


def test_get_plant_names_none():
    """Test None is given to keys if keys aren't present in the data."""
    data = {'nothing': 'test'}
    assert get_plant_names(data) == {
        'name': None, 'plant_id': None, 'scientific_name': None}


def test_get_plant_names_valid_plant_id():
    """Test the function picks up the plant_id value in the data and None for the other keys."""
    data = {'nothing': 'test', 'plant_id': 5}
    assert get_plant_names(data) == {
        'name': None, 'plant_id': 5, 'scientific_name': None}


def test_get_unique_botanists():
    """Test the function filters the unique botanists from full botanist list."""
    botanists = [{'botanist1': 'mary'}, {
        'botanist1': 'mary'}, {'botanist1': 'mary'}, {'botanist2': 'john'}]
    assert len(get_unique_botanists(botanists)) == 2


def test_get_unique_botanists_with_empty_full_list():
    """Test the function can handle an empty list."""
    botanists = []
    assert get_unique_botanists(botanists) == []


def test_get_botanist_data():
    """Test the function can find the botanist key and return its value."""
    data = {'botanist': 'jane', 'key': 'value'}
    assert get_botanist_data(data) == 'jane'


def test_get_recording_data_no_valid_keys():
    """Test the function changes the temperature key present and returns None for the rest."""
    data = {'botanist': 'jane', 'key': 'value', 'temperature': 12}
    assert get_recording_data(data) == {
        'plant_id': None, 'soil_moisture': None, 'temperature': 12, 'recording_taken': None}
