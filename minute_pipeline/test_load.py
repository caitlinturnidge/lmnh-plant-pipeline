"""Unit tests for load.py"""
from os import environ
from unittest.mock import MagicMock
import pandas as pd
from sqlalchemy import Table, MetaData

from load import upload_recordings, upload_waterings

environ['DB_NAME'] = 'test'
environ['DB_SCHEMA'] = 'test'


def test_upload_recordings_correct_calls():
    """Test the correct number of calls occur with two lines of data."""
    data = pd.DataFrame([
        {'plant_id': 1, 'soil_moisture': 30, 'temperature': 25,
            'recording_taken': 'test'},
        {'plant_id': 1, 'soil_moisture': 30, 'temperature': 25,
         'recording_taken': 'test0'}
    ])
    db_metadata = MetaData()
    table = Table("test", db_metadata)
    conn = MagicMock()
    mock_execute = conn.execute
    mock_commit = conn.commit
    upload_recordings(data, conn, table)
    assert mock_execute.call_count == 1
    assert mock_commit.call_count == 1


def test_upload_waterings_correct_calls_empty_data():
    """Test the correct number of calls occur with empty data."""
    data = pd.DataFrame([])
    conn = MagicMock()
    mock_execute = conn.execute
    mock_commit = conn.commit
    db_metadata = MetaData()
    table = Table("test", db_metadata)
    upload_waterings(data, conn, table)
    assert mock_execute.call_count == 1
    assert mock_commit.call_count == 1
