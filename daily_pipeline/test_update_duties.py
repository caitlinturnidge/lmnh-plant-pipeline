"""Unit tests for update_duties.py"""
import pandas as pd
from unittest.mock import MagicMock, patch
from update_duties import get_api_botanist_name_by_plant_id, check_if_duty_exists_in_duties


@patch('update_duties.get')
def test_get_api_botanist_name_by_plant_id(mock_get):
    """Testing name is selected from the API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {'botanist': {'name': 'John Doe'}}
    mock_get.return_value = mock_response

    result = get_api_botanist_name_by_plant_id('test')

    assert result == ['John', 'Doe']
    assert mock_get.call_count == 1


@patch('update_duties.get')
def test_get_api_botanist_name_by_plant_id_no_name(mock_get):
    """Testing function passes if no name is found."""
    mock_response = MagicMock()
    mock_response.json.return_value = {'botanist': {'nothing': 'John Doe'}}
    mock_get.return_value = mock_response

    result = get_api_botanist_name_by_plant_id('test')

    assert result == []
    assert mock_get.call_count == 1


def test_check_if_duty_exists_in_duties_true():
    """Testing True is returned if plant and botonist are present."""
    duties_data = {'plant_id': [1, 2, 3],
                   'botanist_id': [101, 102, 103]}
    duties_df = pd.DataFrame(duties_data)
    result = check_if_duty_exists_in_duties(2, 102, duties_df)
    assert result is True


def test_check_if_duty_exists_in_duties_false():
    """Testing False is returned if plant id is not present."""
    duties_data = {'plant_id': [1, 2, 3],
                   'botanist_id': [101, 102, 103]}
    duties_df = pd.DataFrame(duties_data)
    result = check_if_duty_exists_in_duties(4, 102, duties_df)
    assert result is False
