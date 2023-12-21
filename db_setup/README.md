# RDS Database Setup
This directory contains the files necessary to setup the RDS and seed the tables with information that changes infrequently.

The files in this directory are intended to be ran once in the initial project set up, or when you need to reset the entire database.
- To run all relevant files run `bash setup_db.sh`

The `upload_seed_data.py` & `extract_seed_data.py` scripts can be ran to update information on plants, locations & duties when necessary.

### Requirements

Run `pip install -r requirements.txt`

## schema.sql

This file contains the details for setting up the required tables & dependencies in the database.
It can be run in the terminal with `sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -i schema.sql`

## extract_seed_data.py

### Overview
This script talks to the plant health API & extracts information about the plants, locations & duties.

### Additional Requirements
Environmental variables with database credentials.
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- DB_NAME

### Functions
- `get_plant_data` makes the API request based on the plant id & returns all the information received.
- `parse_location` takes a list of strings in a particular format and labels each string by turning it into a dictionary.
- `generate_location_id` finds the next suitable identity number for a new entry within a list of dictionaries.
- `cross_reference_location` checks if a location is in a list and finds the identity no. of that if it is, otherwise it adds it to the list and generates a new identity no.
- `get_plant_details` filters the API response data into a dictionary with plant_id, name, scientific_name and origin_location. Then origin_location is converted into an id number based on its contents.
- `get_duty_information` retrieves plant_id and botanist information from the API response and creates a dictionary with plant_id and botanist_id based off the botanist's name.
- `extract` combines all previous functions and exports the details of each plant into a csv file for locations, plants & duties.

## upload_seed_data.py

### Overview
This script connects to the RDS database and uploads the data extracted by the previous script into the corresponding table of the database.

### Functions
- `get_database_connection` returns a sqlalchemy engine based on database credentials.
- `upload_locations` inserts each extracted location into the location table in the database using a connection from the sqlalchemy engine.
- `upload_plants`inserts plant details for each id into the plant table in the database using a connection from the sqlalchemy engine.
- `upload_duties` inserts the duties for each botanist into the duty table in the database using a connection from the sqlalchemy engine.
- `upload` combines all previous functions to connected to the database and upload each dataset.
