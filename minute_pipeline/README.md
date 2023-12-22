## Minute pipeline Script
This script is designed to extract and clean data from the Liverpool Natural History Museum's plant API. The soil moisture and temperature recordings are put into the short term database and any data older than 24 hours is put into an S3 bucket for storage. 

This script will run every minute of the day.

It combines extract.py, transform.py, load.py and rds_to_S3.py.

### Requirements

Run `pip install -r requirements.txt`

Add these variables to a .env file

- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME
- DB_SCHEMA
- AWS_ACCESS_KEY_ID_
- AWS_SECRET_ACCESS_KEY_A
- BUCKET_NAME


### Running pipeline.py

Run `pipeline.py`

To run scripts individually, more details are below:

## Extract Script
### Overview
This script is designed to extract data from the Liverpool Natural History Museum's plant API. The extracted data includes information about plant recordings and watering details. The script then processes and organizes this data into separate DataFrames, and saves them as CSV files for cleaning.

### Running the script

`python3 extract.py`

Functions
get_plant_data(plant_id: int) -> list[dict]
Retrieves plant data from the API based on the provided plant ID.

get_recording_data(data: dict) -> dict
Returns recording data as a dictionary, including soil moisture, temperature, and recording timestamp.

get_watering_data(data: dict) -> dict
Returns watering data as a dictionary, including the plant ID and last watering timestamp.

DataFrames
The script creates the following DataFrames:

recording_df: DataFrame containing recording data.
watering_df: DataFrame containing watering data.

The script iterates over 50 plant IDs and fetches data for each plant.
Duplicate and None values are appropriately handled.


## Transform Script
### Overview
This script is designed to clean the extracted data that includes information about plant recordings and watering details. 

### Running the script

`python3 transform.py`

Functions
Transform(recordings, waterings):
Cleans the two dataframes it takes in and returns the two transformed dataframes, ready to be loaded into the database

## Load Script

### Overview
This script gets the cleaned data in the dataframes, created from the transform script and adds them to the short term database.

Run the script:

`python3 load.py`

Functions:
- get_database_connection - Gets the connection to the database
- upload_recordings - uploads the recordings data to the database
- upload_waterings - uploads the waterings data to the database`


## RDS to S3 Script
Contains code to retrieve watering/recording data older than 24hrs from the database, append it to
the relevant files in s3 (automatically creates if none exist), and delete from the db.

Entire functionality is run by calling function `update_rds_and_s3()`, with no arguments, which is called automatically when the function is run from the command line.

### Requirements to run
- Assumes same s3 file structure as detailed in notes for `daily_pipeline/README.md`
