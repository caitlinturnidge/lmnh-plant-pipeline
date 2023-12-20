"""File to load the clean recording and watering data into the short term database."""
import csv
from os import environ

from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.engine.base import Connection


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


def get_recordings_csv() -> list:
    """Gets the cleaned recordings csv and returns it."""
    with open('/tmp/recording_data_SAMPLE.csv', 'r', encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def get_waterings_csv() -> list:
    """Gets the cleaned waterings csv and returns it."""
    with open('/tmp/watering_data_SAMPLE.csv', 'r', encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def upload_recordings(conn: Connection, table: db.Table) -> None:
    """Uploads recording data to the database."""
    data = get_recordings_csv()

    try:
        conn.execute(table.insert(), data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def upload_waterings(conn: Connection, table: db.Table) -> None:
    """Uploads watering data to the database."""
    data = get_waterings_csv()

    try:
        conn.execute(table.insert(), data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def load() -> None:
    """Main function to run the whole load script."""
    db_engine = get_database_engine()
    db_connection = db_engine.connect()
    db_metadata = db.MetaData(schema=environ['DB_SCHEMA'])
    recording_table = db.Table("recording", db_metadata, autoload_with=db_engine)
    watering_table = db.Table("watering", db_metadata, autoload_with=db_engine)
    upload_recordings(db_connection, recording_table)
    upload_waterings(db_connection, watering_table)
    db_connection.close()


if __name__ == "__main__":
    load_dotenv()
    load()
