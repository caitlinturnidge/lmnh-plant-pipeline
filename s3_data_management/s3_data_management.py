"""
Module containing code to extract and combine cumulative csv files for the month with csv files
from the previous day in the folder in the s3 bucket corresponding to yesterday's month.
"""

from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd

from boto3 import client

TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)


def create_s3_client():
    """Creates a client that connects to s3 on AWS."""
    return client("s3",
                  aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])


def get_bucket_keys(s3_client: client, folder_path: str, bucket_name: str) -> list:
    """Returns a list of keys of csv files, with a prefix matching the folder_path."""
    objects = s3_client.list_objects(
        Bucket=bucket_name, Prefix=folder_path).get('Contents')
    if objects:
        return [obj['Key'] for obj in objects if '.csv' in obj['Key']]
    return []


def save_df_to_s3_bucket(s3_client: client, df: pd.DataFrame, key: str, bucket: str):
    """Function to save a pandas dataframe to the given s3 bucket."""
    file_body = df.to_csv()
    s3_client.put_object(Body=file_body, Bucket=bucket, Key=key)


def combine_csv_files_for_month(s3_client: client, bucket_name: str):
    """Downloads relevant files from S3 to local, converts into two pandas data frames and saves them, 
           old csv files that have been combined are deleted."""
    folder_path = f'{YESTERDAY.year}/{YESTERDAY.month}'
    keys = get_bucket_keys(s3_client, folder_path, bucket_name)
    for data_type in ['watering', 'recording']:
        type_keys = [key for key in keys if data_type in key and
                     key.split('_')[-1] != str(TODAY.day)]
        # ^^ Don't want data from live files
        responses = [s3_client.get_object(
            Bucket=bucket_name, Key=key) for key in type_keys]
        # ^^ List comprehension handles start / end of month
        df = pd.concat([pd.read_csv(response.get("Body"))
                       for response in responses])
        save_df_to_s3_bucket(
            s3_client, df, f"{folder_path}/{data_type}.csv", bucket_name)
        s3_client.delete_object(
            Bucket=bucket_name, Key=f"{folder_path}/{data_type}_{YESTERDAY.day}.csv")


def handler(event=None, context=None):
    """Function to run the whole management script as a Lambda function."""
    s3_client = create_s3_client()
    combine_csv_files_for_month(s3_client, environ['BUCKET_NAME'])


if __name__ == "__main__":
    load_dotenv()
    print(handler({'key': 'value'}))
