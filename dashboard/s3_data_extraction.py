"""
Module containing code to extract and combine cumulative csv files for the month with csv files
from the previous day in the folder in the s3 bucket corresponding to yesterday's month.
"""

from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv

import pandas as pd
import re
from boto3 import client


load_dotenv()
TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)
VALID_S3_FILE_PATTERN = r'20[0-9][0-9]\/(([0-9])|(1[0-2]))\/(watering|recording)(_(([1-9]|[1-2][0-9]|3[01])))?.csv'


def create_s3_client():
    """Creates a client that connects to s3 on AWS."""
    return client("s3",
                  aws_access_key_id=environ['AWS_ACCESS_KEY_ID_'],
                  aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY_'])


def get_bucket_keys(s3_client: client, bucket_name: str = environ['BUCKET_NAME']) -> list:
    """
    Returns a list of keys of csv files, format matching {year}/{month}/recording_20, for example
    (recording could be watering, and underscore day is optional).
    """
    objects = s3_client.list_objects(
        Bucket=bucket_name).get('Contents')
    if objects:
        return [obj['Key'] for obj in objects if re.search(VALID_S3_FILE_PATTERN, obj['Key'])]
    return []


def get_earliest_data_date(s3_client: client, bucket_name: str = environ['BUCKET_NAME']):
    """Function to return the earliest month there is data for in the s3 bucket."""
    keys = get_bucket_keys(s3_client, bucket_name)
    keys.sort(key = lambda file_name: int(''.join(file_name.split('/')[:-1])))
    return datetime(year = int(keys[0].split('/')[0]), month = int(keys[0].split('/')[1]), day = 1)



def get_s3_data_for_type_and_date_ranges(s3_client, data_type: str, range_start: datetime,
                                         range_end: datetime = TODAY,
                                         bucket_name: str = environ['BUCKET_NAME']):
    """
    Downloads relevant s3 files for every month between the two dates (including the months in
    which they themselves fall).
    """
    if range_start > (datetime.now() - timedelta(days = 1)).date():
        return pd.DataFrame()

    keys = get_bucket_keys(s3_client, bucket_name)

    int_start = int(str(range_start.year) + str(range_start.month))
    int_end = int(str(range_end.year) + str(range_end.month))

    keys = [key for key in keys if int_start <= int(''.join(key.split('/')[:-1])) <= int_end]
    # Filters keys by date_range
    keys = [key for key in keys if data_type in key]
    # Filters keys by datatype

    responses = [s3_client.get_object(Bucket=bucket_name, Key=key) for key in keys]
    # ^^ List comprehension handles start / end of month

    df = pd.DataFrame()

    for response in responses:
        try:
            # This way would allow us to monitor df size and decrease resolution as needed
            df_csv = pd.read_csv(response.get("Body"))
            df = pd.concat([df, df_csv])
        except pd.errors.EmptyDataError as e:
            pass

    if not df.empty:
        df['datetime'] = pd.to_datetime(df['datetime'])

    return df


if __name__ == "__main__":

    s3_client = create_s3_client()

    print(get_s3_data_for_type_and_date_ranges(s3_client, 'recording', range_start=datetime.today()-timedelta(days=1)))

