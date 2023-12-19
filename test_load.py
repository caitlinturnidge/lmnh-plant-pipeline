"""Unit tests for load.py"""
from os import environ
from unittest.mock import MagicMock, patch

from load import upload_recordings, upload_waterings

environ['DB_NAME'] = 'test'
environ['DB_SCHEMA'] = 'test'


@patch("load.get_recordings_csv")
def test_upload_recordings_correct_calls(mock_get_recordings_csv):
    """Test the correct number of calls occur with two lines of data."""
    mock_get_recordings_csv.return_value = mock_get_recordings_csv.return_value = [
        {'plant_id': 1, 'soil_moisture': 30, 'temperature': 25,
            'recording_taken': 'test'},
        {'plant_id': 1, 'soil_moisture': 30, 'temperature': 25,
         'recording_taken': 'test0'}
    ]
    conn = MagicMock()
    mock_execute = conn.execute
    upload_recordings(conn)
    assert mock_execute.call_count == 5


@patch("load.get_waterings_csv")
def test_upload_waterings_correct_calls_empty_data(mock_get_waterings_csv):
    """Test the correct number of calls occur with empty data."""
    mock_get_waterings_csv.return_value = []
    conn = MagicMock()
    mock_execute = conn.execute
    mock_commit = conn.commit
    upload_waterings(conn)
    assert mock_execute.call_count == 3
    assert mock_commit.call_count == 0
