"""
Contains code to retrieve watering/recording data older than 24hrs from the database, append it to
the relevant files in s3 (automatically creates if none exist), and delete from the db.
"""

from datetime import datetime, timedelta
from os import environ
import pandas as pd

from boto3 import client
from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.engine.base import Connection


load_dotenv()



def get_database_engine():
    """Returns the database engine."""
    try:
        engine = db.create_engine(
            f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}:{environ['DB_PORT']}/{environ['DB_NAME']}?charset=utf8"
        )
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise e


def get_old_records(table_name: str, db_engine: db.Engine, connection: Connection, metadata,
                    datetime_cutoff: str):
    """
    Retrieves records older than 24 hours (by attribute 'datetime') from db table with given name
    (watering/recording).
    """
    try:
        table = db.Table(table_name, metadata, autoload_with=db_engine)
        query = db.select(table).where(table.columns.datetime < datetime_cutoff)
        response = connection.execute(query)
        results = response.fetchall()
        return pd.DataFrame(results)

    except Exception as e:
        raise e


def get_day_bucket_keys(s3_client: client, folder_path: str, day: int,
                    bucket_name: str = environ['BUCKET_NAME']) -> list:
    """
    Returns list of keys within a given s3 bucket ending in '_{yesterday}.csv, with a prefix matching
    the given folder_path.
    """
    objects = s3_client.list_objects(Bucket=bucket_name, Prefix=folder_path).get('Contents')
    if objects:
        return [obj['Key'] for obj in objects if f'{day}.csv' in obj['Key']]
    return []


def get_current_csv_data(data_type: str, s3_client: client, date: str, bucket_name:
                         str = environ['BUCKET_NAME']) -> pd.DataFrame:
    """
    Downloads relevant files of specified data_type (watering/recording) from S3 to local, and
    then returns it as a pandas dataframe.
    """

    folder_path = f'{date.year}/{date.month}'
    keys = get_day_bucket_keys(s3_client, folder_path)
    type_keys = [key for key in keys if data_type in key]
    if type_keys:
        type_key = type_keys[0]
        response = s3_client.get_object(Bucket=bucket_name, Key = type_key)
        try:
            return pd.read_csv(response.get("Body"))
        except pd.errors.EmptyDataError:
            # Prevents code crashing if a csv exists in s3 but is empty
            pass

    return pd.DataFrame()


def upload_to_s3(data_type: str, df: pd.DataFrame, s3_client,
                 date: str, bucket_name: str = environ['BUCKET_NAME']):
    """Uploads pandas dataframe of data_type to appropriate csv in s3 bucket."""
    s3_client.put_object(Body = df.to_csv(index=False), Bucket = bucket_name,
                         Key = f'{date.year}/{date.month}/{data_type}_{date.day}.csv')



def delete_oldest_records(table_name: str, db_engine: db.Engine, connection: Connection, metadata,
                          datetime_cutoff: str):
    """
    Deletes records older than 24 hours (by attribute 'datetime') from db table with given name
    (watering/recording).
    """
    try:
        table = db.Table(table_name, metadata, autoload=True,
                         autoload_with=db_engine)
        query = db.delete(table).where(table.columns.datetime < datetime_cutoff)
        connection.execute(query)
        connection.commit()
    except Exception as e:
        raise e


def update_rds_and_s3():
    """
    Gets any records from watering and recording tables in df older than 24hours, combines with
    the csv files in s3 bucket for current day (if any exist), and saves the result as csvs in the
    bucket with a name ending in _{yesterday}.csv.
    """
    literal_day_ago = (datetime.now() - timedelta(hours = 24))

    db_engine = get_database_engine()
    db_connection = db_engine.connect()
    db_metadata = db.MetaData(schema=environ['DB_SCHEMA'])

    s3_client = client("s3",
                       aws_access_key_id=environ['AWS_ACCESS_KEY_ID_'],
                       aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY_'])

    for data_type in ['recording', 'watering']:
        df = get_old_records(data_type, db_engine, db_connection, db_metadata, literal_day_ago)
        df = pd.concat([get_current_csv_data(data_type, s3_client, literal_day_ago), df])
        upload_to_s3(data_type, df, s3_client, literal_day_ago)
        delete_oldest_records(data_type, db_engine, db_connection, db_metadata, literal_day_ago)

    db_connection.close()


if __name__ == "__main__":
    update_rds_and_s3()
