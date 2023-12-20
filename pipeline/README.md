## Pipeline Script
This script is designed to extract and clean data from the Liverpool Natural History Museum's plant API. The soil moisture and temperature recordings are put into the short term database and any data older than 24 hours is put into an S3 bucket for storage. 

This script will run every minute of the day.

It combines extract.py, load.py and rds_to_S3.py.

### Requirements

Run `pip install -r requirements.txt`

### Running pipeline.py

Run `pipeline.py`

To run scripts individually, more details are below:

## Extract Script
### Overview
This script is designed to extract and clean data from the Liverpool Natural History Museum's plant API. The extracted data includes information about plant recordings, watering details, botanists, and plant names. The script then processes and organizes this data into separate DataFrames, and saves them as CSV files for further analysis.

Usage
To use the script, ensure you have the required dependencies installed:

### Dependencies
requests
pandas

Run the script:

`python3 extract.py`

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


## Load Script

### Overview
This script gets the cleaned data in the csvs, created from the extract script and adds them to the short term database.

Usage
To use the script, ensure you have the required dependencies installed:

### Dependencies
sqlalchemy
python-dotenv
pytest

### Add environment variables to .env
- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME
- DB_SCHEMA

Run the script:

`python3 load.py`

Functions:
- get_database_connection - Gets the connection to the database
- get_recordings_csv - Gets the recordings data from the csv and returns it
- get_waterings_csv - Gets the waterings data from the csv and returns it
- upload_recordings - uploads the recordings data to the database
- upload_waterings - uploads the waterings data to the database`


## RDS to S3 Script
Contains code to retrieve watering/recording data older than 24hrs from the database, append it to
the relevant files in s3 (automatically creates if none exist), and delete from the db.

Entire functionality is run by calling function `update_rds_and_s3()`, with no arguments, which is called automatically when the function is run from the commandline.

### Requirements to run
- Assumes same s3 file structure as detailed in notes for `s3_data_management/`
- Written to use a .env file with AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, BUCKET_NAME, DB_HOST, BB_PORT, DB_NAME, DB_SCHEMA, DB_USER, DB_PASSWORD
- Library requirements in file `requirements.txt` in parent directory