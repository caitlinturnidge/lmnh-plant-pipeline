## Daily Pipeline

This pipeline runs at 00:15 each day. It runs the S3 data management followed by the update duties script.


### Add these values to a .env file

- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME
- DB_SCHEMA
- AWS_ACCESS_KEY_ID_
- AWS_SECRET_ACCESS_KEY_A
- BUCKET_NAME

### Running daily_pipeline.py

- Run `pip install -r requirements`
- Run `daily_pipeline.py`

## What does each script do?

### s3_data_management.py

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

### update_duties.py

Each day, this script checks to see if the duties (the carer of each plant) have changed. If they have, then this updates the plant-duties table to make sure the duties are up do date. If the duties get updated more frequently than we are assuming, then note that this script can be ran more often to keep them even more up to date.