"""
Contains code to retrieve watering/recording data older than 24hrs from the database, append it to
the relevant files in s3 (automatically creates if none exist), and delete from the db.
"""

from os import environ
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.engine.base import Connection
from boto3 import client


STR_DAY_AGO = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
TODAY = datetime.today()


def get_database_engine():
    """Returns the database engine."""
    try:
        engine = db.create_engine(
            f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8"
        )
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise e


def get_old_records(table_name: str, db_engine: db.Engine, connection: Connection, metadata,
                    date_cutoff: str = STR_DAY_AGO):
    """
    Retrieves records older than 24 hours (by attribute 'datetime') from db table with given name
    (watering/recording).
    """
    try:
        table = db.Table(f"{environ['DB_SCHEMA']}.{table_name}", metadata, autoload=True,
                         autoload_with=db_engine)
        query = db.select([table]).where(table.columns.datetime < date_cutoff)
        response = connection.execute(query)
        return pd.DataFrame(response.fetchall())

    except Exception as e:
        raise e


def get_day_bucket_keys(s3_client: client, folder_path: str, day: int = TODAY.day,
                    bucket_name: str = environ['BUCKET_NAME']) -> list:
    """
    Returns list of keys within a given s3 bucket ending in '_{day}.csv, with a prefix matching
    the given folder_path.
    """
    objects = s3_client.list_objects(Bucket=bucket_name, Prefix=folder_path).get('Contents')
    if objects:
        return [obj['Key'] for obj in objects if obj['Key'].split('_')[-1] == f'{day}.csv']
    return []


def get_current_csv_data(data_type: str, s3_client: client, bucket_name:
                         str = environ['BUCKET_NAME'], date: str = TODAY) -> pd.DataFrame:
    """
    Downloads relevant files of specified data_type (watering/recording) from S3 to local, and
    then returns it as a pandas dataframe
    """

    folder_path = f'{date.year}/{date.month}'
    keys = get_day_bucket_keys(s3_client, folder_path)
    type_keys = [key for key in keys if data_type in key]
    if type_keys:
        type_key = type_keys[0]
        response = s3_client.get_object(Bucket=bucket_name, Key = type_key)
        return pd.read_csv(response.get("Body"))
    return pd.DataFrame


def upload_to_s3(data_type: str, df: pd.DataFrame, s3_client,
                 bucket_name: str = environ['BUCKET_NAME'], date: str = TODAY):
    """Uploads pandas dataframe of data_type to appropriate csv in s3 bucket."""
    s3_client.put_object(Body = df.to_csv(), Bucket = bucket_name,
                         Key = f'{date.year}/{date.month}/{data_type}_{date.day}.csv')



def delete_oldest_records(table_name: str, db_engine: db.Engine, connection: Connection, metadata):
    """
    Deletes records older than 24 hours (by attribute 'datetime') from db table with given name
    (watering/recording).
    """
    try:
        table = db.Table(f"{environ['DB_SCHEMA']}.{table_name}", metadata, autoload=True,
                         autoload_with=db_engine)
        query = db.delete([table]).where(table.columns.datetime < STR_DAY_AGO)
        connection.execute(query)
        connection.commit()
    except Exception as e:
        raise e


def update_rds_and_s3():
    """
    Gets any records from watering and recording tables in df older than 24hours, combines with
    the csv files in s3 bucket for current day (if any exist), and saves the result as csvs in the
    bucket with a name ending in _{day}.csv.
    """
    db_engine = get_database_engine()
    db_connection = db_engine.connect()
    db_metadata = db.MetaData()

    s3_client = client("s3",
                       aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])

    for data_type in ['recording', 'watering']:
        df = get_old_records(data_type, db_engine, db_connection, db_metadata)
        df = pd.concat(df, get_current_csv_data(data_type, s3_client))
        upload_to_s3(data_type, df, s3_client)
        delete_oldest_records(data_type, db_engine, db_engine, db_metadata)


if __name__ == "__main__":
    load_dotenv()
    update_rds_and_s3()
