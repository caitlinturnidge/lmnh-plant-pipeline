"""Unit tests for transform.py"""
import pandas as pd
from transform import transform


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
