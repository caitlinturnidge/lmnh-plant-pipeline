"""File to combine the extract and loading into RDS and S3 scripts, to run the pipeline in a lambda function."""
import logging
from dotenv import load_dotenv

from extract import extract_and_transform
from load import load
from rds_to_s3 import update_rds_and_s3


def set_up_logger():
    """Set up a logger, to log pipeline progress to the console."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('logger')


def run_pipeline():
    """Extracts the plant data, loads it into the short term database and moves data over 24hours old into S3 storage."""
    load_dotenv()
    logger = set_up_logger()

    extract_and_transform()
    logger.info("All plant data has been extracted and cleaned.")

    load()
    logger.info("Plant data has been loaded into the short term database.")

    update_rds_and_s3()
    logger.info("Old plant data has been moved to S3 storage.")


def handler(event=None, context=None) -> None:
    """Function to run the whole pipeline script as a Lambda function."""
    run_pipeline()


if __name__ == "__main__":
    handler()
