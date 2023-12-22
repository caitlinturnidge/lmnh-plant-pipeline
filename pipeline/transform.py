"""File to clean and transform the extracted data from the API, so that its ready to be loaded."""
import pandas as pd

def transform(recording_df, watering_df):
    """Cleans the extracted data frames."""
    recording_df['recording_taken'] = pd.to_datetime(
        recording_df['recording_taken'])
    recording_df = recording_df.rename(columns={'recording_taken': 'datetime'})
    watering_df['last_watered'] = pd.to_datetime(
        watering_df['last_watered']).dt.tz_localize(None)
    watering_df = watering_df.rename(columns={'last_watered': 'datetime'})
    return recording_df, watering_df
