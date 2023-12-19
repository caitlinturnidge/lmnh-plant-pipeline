"""Script to create mock 24-hr data for 1 plant."""


import pandas as pd
import numpy as np
from datetime import datetime, timedelta


if __name__ == "__main__":

    # Given readings for multiple plants
    initial_readings = [
        {'plant_id': 0, 'soil_moisture': 25.730933575024196,
            'temperature': 13.157893007926564, 'recording_taken': '2023-12-19 11:21:43'},
        {'plant_id': 1, 'soil_moisture': 23.98298531988189,
            'temperature': 12.026341992360456, 'recording_taken': '2023-12-19 11:21:45'},
        {'plant_id': 2, 'soil_moisture': 30.616930942675168,
            'temperature': 9.116185308436853, 'recording_taken': '2023-12-19 11:21:45'},
        {'plant_id': 3, 'soil_moisture': 29.019263723342945,
            'temperature': 26.039994462840696, 'recording_taken': '2023-12-19 11:21:46'},
        {'plant_id': 4, 'soil_moisture': 20.951649013916494,
            'temperature': 11.321636304659222, 'recording_taken': '2023-12-19 11:21:47'},
        {'plant_id': 5, 'soil_moisture': 30.434974296121098,
            'temperature': 11.178615799217587, 'recording_taken': '2023-12-19 11:21:48'},
        {'plant_id': 6, 'soil_moisture': 27.364642121408707,
            'temperature': 10.96016882103583, 'recording_taken': '2023-12-19 11:21:48'}
    ]

    # Convert the recording_taken string to a datetime object for each plant
    for reading in initial_readings:
        reading['recording_taken'] = datetime.strptime(
            reading['recording_taken'], '%Y-%m-%d %H:%M:%S')

    # Generate a time series for 24 hours at 1-minute intervals
    time_series = [initial_readings[0]['recording_taken'] +
                   timedelta(minutes=i) for i in range(24 * 60)]

    # Create a DataFrame with the mock data for each plant
    mock_data_list = []
    for reading in initial_readings:
        plant_id = reading['plant_id']
        moisture_variation = np.random.normal(0, 1, len(time_series))
        temperature_variation = np.random.normal(0, 0.5, len(time_series))

        plant_mock_data = pd.DataFrame({
            'plant_id': [plant_id] * len(time_series),
            'soil_moisture': reading['soil_moisture'] + moisture_variation,
            'temperature': reading['temperature'] + temperature_variation,
            'recording_taken': time_series
        })

        mock_data_list.append(plant_mock_data)

    # Concatenate the mock data for each plant into a single DataFrame
    mock_data = pd.concat(mock_data_list, ignore_index=True)

    # Print or visualize the mock data
    print(mock_data.head())

    # Save the mock data to a CSV file if needed
    mock_data.to_csv('mock_data_multi_plants.csv', index=False)

    # initial_reading = {
    #     'plant_id': 0,
    #     'soil_moisture': 25.730933575024196,
    #     'temperature': 13.157893007926564,
    #     'recording_taken': '2023-12-19 11:21:43'
    # }

    # initial_time = datetime.strptime(
    #     initial_reading['recording_taken'], '%Y-%m-%d %H:%M:%S')

    # time_series = [initial_time + timedelta(minutes=i) for i in range(24 * 60)]

    # # Introduce random fluctuations
    # moisture_variation = np.random.normal(
    #     0, 1, len(time_series))
    # temperature_variation = np.random.normal(
    #     0, 0.5, len(time_series))

    # mock_data = pd.DataFrame({
    #     'plant_id': [initial_reading['plant_id']] * len(time_series),
    #     'soil_moisture': initial_reading['soil_moisture'] + moisture_variation,
    #     'temperature': initial_reading['temperature'] + temperature_variation,
    #     'recording_taken': time_series
    # })

    # print(mock_data.head())

    # mock_data.to_csv('mock_data.csv', index=False)
