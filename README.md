# Plant Pipeline Group Project Folders

## db_setup

This folder contains the files required to set up the initial database and files to seed this database with static data. This allows for soil moisture and temperature plant recordings to be added when the pipeline runs.

## minute_pipeline

This folder contains the files required to run the minute pipeline that gets the plant data from the api, loads it into the short term database and takes old data (from over 24 hours ago) from this database and adds it to S3 to be stored in long term storage.

## daily_pipeline

This folder contains the files to run the daily pipeline at 00:15. Firstly, it organizes the S3 long term storage by adding data from the previous day into the correct year and month files in S3. It also updates the duties table in the database, to check the duties of each plant have not changed.

## dashboard

This folder contains the files that create the plant analytics dashboard. It shows the plant soil moisture and temperature over time for specific plants.

## terraform

This folder contains the files to create all the cloud resources for both the pipelines and dashboard.  