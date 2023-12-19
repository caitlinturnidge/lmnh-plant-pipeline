"""Unit tests for s3_data_management.py"""
from os import environ
from unittest.mock import MagicMock, patch

from s3_data_management import get_bucket_keys, combine_csv_files_for_month

environ['BUCKET_NAME'] = 'test'


def test_get_bucket_keys_correct_keys():
    """Test the bucket keys returned are just csv files."""
    s3_client_mock = MagicMock()
    folder_path = 'testing'
    bucket_name = 'test'
    sample_objects = [
        {'Key': 'folder/file1.csv'},
        {'Key': 'folder/file2.json'},
        {'Key': 'other_folder/file3.txt'},
        {'Key': 'folder/file4.csv'},
    ]

    s3_client_mock.list_objects.return_value = {'Contents': sample_objects}
    result = get_bucket_keys(
        s3_client_mock, folder_path, environ['BUCKET_NAME'])

    s3_client_mock.list_objects.assert_called_once_with(
        Bucket=bucket_name, Prefix=folder_path)
    assert result == ['folder/file1.csv', 'folder/file4.csv']
