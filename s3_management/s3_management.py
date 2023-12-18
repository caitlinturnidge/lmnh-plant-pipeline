from boto3 import client
from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)


def get_bucket_keys(s3_client: client, folder_path: str, bucket_name: str = environ['BUCKET_NAME']):
    """
    Returns list of keys of csv files within a given s3 bucket, with a prefix matching the given folder_path.
    """
    objects = s3_client.list_objects(Bucket=bucket_name, Prefix=folder_path).get('Contents')
    if objects:
        return [obj['Key'] for obj in objects if obj['Key'].split(-1)[-1] == '.csv']
    return []


def save_df_to_s3_bucket(s3_client: client, df: pd.DataFrame,
                         key: str, bucket: str = environ['BUCKET_NAME']):
    """Function to save a pandas dataframe to the given s3 bucket."""
    file_body = df.to_csv()

    s3_client.put_object(Body = file_body, Bucket = bucket, Key = key)


def combine_csv_files_for_month(s3_client: client, bucket_name: str = environ['BUCKET_NAME']):
    """
    Downloads relevant files from S3 to local, and then converts into two pandas dataframes, one
    containing all recording info, and one all watering info.
    """

    folder_path = f'{YESTERDAY.year}/{YESTERDAY.month}'
    keys = get_bucket_keys(s3_client, bucket_name, folder_path)

    s3_dfs = {}
    for type in ['watering', 'recording']:
        type_keys = [key for key in keys if type in key and key.split('_')[-1] != str(TODAY.day)]
        # ^^^ Don't want data from live files
        responses = [s3_client.get_object(Bucket=bucket_name, Key = key) for key in type_keys]
        df = \
            pd.concat([pd.read_csv(response.get("Body")) for response in responses])
        save_df_to_s3_bucket(s3_client, df, f"{folder_path}/{type}.csv")


if __name__ == "__main__":
    s3_client = client("s3",
                       aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'])