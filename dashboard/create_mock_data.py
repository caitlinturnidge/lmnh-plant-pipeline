"""Script to create mock 24-hr data for 1 plant."""


import pandas as pd
import numpy as np
from datetime import datetime, timedelta


if __name__ == "__main__":

    initial_reading = {
        'plant_id': 0,
        'soil_moisture': 25.730933575024196,
        'temperature': 13.157893007926564,
        'recording_taken': '2023-12-19 11:21:43'
    }

    initial_time = datetime.strptime(
        initial_reading['recording_taken'], '%Y-%m-%d %H:%M:%S')

    time_series = [initial_time + timedelta(minutes=i) for i in range(24 * 60)]

    # Introduce random fluctuations
    moisture_variation = np.random.normal(
        0, 1, len(time_series))
    temperature_variation = np.random.normal(
        0, 0.5, len(time_series))

    mock_data = pd.DataFrame({
        'plant_id': [initial_reading['plant_id']] * len(time_series),
        'soil_moisture': initial_reading['soil_moisture'] + moisture_variation,
        'temperature': initial_reading['temperature'] + temperature_variation,
        'recording_taken': time_series
    })

    print(mock_data.head())

    mock_data.to_csv('mock_data.csv', index=False)
