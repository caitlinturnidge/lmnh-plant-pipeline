# Plant Pipeline Group Project Folders

## db_setup

This folder contains the files required to set up the initial database and files to seed this database with static data. This allows for soil moisture and temperature plant recordings to be added when the pipeline runs.

## pipeline

This folder contains the files required to run the pipeline that gets the plant data from the api, loads it into the database and takes old data from the database and adds it to S3 to be stored in long term storage.

## s3_data_management

This folder contains the file that manages the S3 long term storage. It puts data from the previous day into the correct year and month files in S3.

## dashboard

This folder contains the files that create the plant analytics dashboard. It shows the plant soil moisture and temperature over time for specific plants.

## terraform

This folder contains the files that create cloud resources for the pipeline, dashboard and S3 management files to be ran on the cloud.