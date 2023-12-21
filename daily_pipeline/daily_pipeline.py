"""Combines the S3 management script and update duties so they run in the same lambda function"""
from dotenv import load_dotenv
import logging

from s3_data_management import management
from update_duties import cross_reference_api_and_db_duties


def set_up_logger():
    """Set up a logger, to log pipeline progress to the console."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('logger')


def run_pipeline():
    """Function to run the whole management script as a Lambda function."""
    logger = set_up_logger()
    load_dotenv()
    management()
    logger.info("S3 management has been complete.")
    cross_reference_api_and_db_duties()
    logger.info("Duties table has been updated.")


def handler(event=None, context=None) -> None:
    """Function to run the whole pipeline script as a Lambda function."""
    run_pipeline()


if __name__ == "__main__":
    handler()
