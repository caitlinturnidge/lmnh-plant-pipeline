"""Unit tests for extract seed data."""
from unittest.mock import patch
from extract_seed_data import parse_location, generate_location_id, get_plant_details


def test_parse_location():
    """Testing the correct details are added to the dictionary."""
    location_info = ["42.3601", "-71.0589",
                     "Boston", "US", "America/New_York"]
    result = parse_location(location_info)
    assert result == {
        "latitude": "42.3601",
        "longitude": "-71.0589",
        "town": "Boston",
        "country_code": "US",
        "continent": "America",
        "city": "New_York"
    }


def test_parse_no_location():
    """testing no details are added if the length of location info is not 5."""
    location_info = ["test"]
    result = parse_location(location_info)
    assert not result


def test_generate_location_id_empty_list():
    """Testing for an empty list."""
    locations = []
    result = generate_location_id(locations)
    assert result == 1


def test_generate_location_id_non_empty_list():
    """Test with a non-empty list of locations."""
    locations = [{"id": 1}, {"id": 3}, {"id": 2}]
    result = generate_location_id(locations)
    assert result == 4


@patch("extract_seed_data.cross_reference_location")
def test_get_plant_details(mock_cross_reference_location):
    """Testing plant details are transformed corectly."""
    mock_cross_reference_location.return_value = "Mocked Location"

    data = {
        'plant_id': 1,
        'name': 'Rose',
        'scientific_name': ['Rosa'],
        'origin_location': 101
    }
    locations = [{'id': 101, 'name': 'Garden'}]

    result = get_plant_details(data, locations)

    assert result == {
        'plant_id': 1,
        'name': 'Rose',
        'scientific_name': 'Rosa',
        'origin_location': 'Mocked Location'
    }


@patch("extract_seed_data.cross_reference_location")
def test_get_plant_details_no_scientific_name(mock_cross_reference_location):
    """Testing plant details are transformed corectly when there is a key missing."""
    mock_cross_reference_location.return_value = "Mocked Location"

    data = {
        'plant_id': 1,
        'name': 'Rose',
        'origin_location': 101
    }
    locations = [{'id': 101, 'name': 'Garden'}]

    result = get_plant_details(data, locations)

    assert result == {
        'plant_id': 1,
        'name': 'Rose',
        'scientific_name': None,
        'origin_location': 'Mocked Location'
    }
