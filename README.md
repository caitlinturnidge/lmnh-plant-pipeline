## Plant Data Extraction and Cleaning Script
### Overview
This script is designed to extract and clean data from the Liverpool Natural History Museum's plant API. The extracted data includes information about plant recordings, watering details, botanists, and plant names. The script then processes and organizes this data into separate DataFrames, and saves them as CSV files for further analysis.

### Dependencies
requests
pandas


Usage
To use the script, ensure you have the required dependencies installed:



Run the script:

```python3 extract.py
```

Functions
get_plant_data(plant_id: int) -> list[dict]
Retrieves plant data from the API based on the provided plant ID.

get_recording_data(data: dict) -> dict
Returns recording data as a dictionary, including soil moisture, temperature, and recording timestamp.

get_watering_data(data: dict) -> dict
Returns watering data as a dictionary, including the plant ID and last watering timestamp.

get_botanist_data(data: dict) -> dict
Returns botanist data as a dictionary.

get_unique_botanists(botanist_list: list[dict]) -> list[dict]
Filters unique botanists from the full botanist list.

get_plant_names(data: dict) -> dict
Returns plant data as a dictionary, including the plant ID, name, and scientific name.

DataFrames
The script creates the following DataFrames:

recording_df: DataFrame containing recording data.
watering_df: DataFrame containing watering data.
botanist_df: DataFrame containing unique botanist data.
plant_df: DataFrame containing plant data.
CSV Files
The resulting DataFrames are saved as CSV files:

recording_data_SAMPLE.csv
watering_data_SAMPLE.csv
botanist_data_SAMPLE.csv
Notes
The script iterates over 50 plant IDs and fetches data for each plant.
Duplicate and None values are appropriately handled.

## s3_data_management
Contains files for management of data in s3 bucket; to be run daily *after* midnight, to combine the csv from the day before into the monthly csv. Assumes an s3 file structure as follows:
- `{year}`
    - `{month}`
        - `watering.csv`
        - `recording.csv`
        - `watering_{yesterday}.csv`
        - `recording_{yesterday}.csv`
        - `watering_{today}.csv`
        - `recording_{today}.csv`

Purpose of the script is to append the data from `watering_{yesterday}.csv` and `recording_{yesterday}.csv` to `watering.csv` and `recording.csv`, respectively.

For example, the structure before the script is run today (18/12/23) might look like (leaving irrelevant folders unexpanded):
- `2021`
- `2022`
- `2023`
    - `1`
    - `2`
    - ...
    - `11`
    - `12`
        - `watering.csv`
        - `recording.csv`
        - `watering_17.csv`
        - `recording_17.csv`
        - `watering_18.csv`
        - `recording_18.csv`

And, after the script is run, would look like:
- `2021`
- `2022`
- `2023`
    - `1`
    - `2`
    - ...
    - `11`
    - `12`
        - `watering.csv`
        - `recording.csv`
        - `watering_18.csv`
        - `recording_18.csv`

At the end of each month, the month folder will contain only two csv files, `watering.csv` and `recording.csv`.

### Requirements to run
- Written to use a .env file with AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, BUCKET_NAME.
- Library requirements in file `requirements.txt`
