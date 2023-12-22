"""Unit tests for rds_to_s3.py"""
from unittest.mock import MagicMock

from rds_to_s3 import get_day_bucket_keys


def test_get_day_bucket_keys_valid():
    """Testing the correct keys are returned."""
    s3_client_mock = MagicMock()

    day = 10

    s3_client_mock.list_objects.return_value = {
        'Contents': [
            {'Key': 'test/file.csv'},
            {'Key': 'test/file_10.csv'},
            {'Key': 'test/file_9.csv'},
        ]
    }

    result = get_day_bucket_keys(s3_client_mock, 'test', day, 'test')

    assert result == ['test/file_10.csv']
    assert s3_client_mock.list_objects.call_count == 1
