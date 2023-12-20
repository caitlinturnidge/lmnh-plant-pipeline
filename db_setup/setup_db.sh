# Run this script to create the database and seed the static data with details from the API.

source ../.env

sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -i schema.sql

python3 extract_seed_data.py

python3 upload_seed_data.py