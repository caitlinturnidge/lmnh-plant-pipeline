"""File to load the clean recording and watering data into the short term database."""
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


def upload_recordings(data, conn: Connection, table: db.Table) -> None:
    """Uploads recording data to the database."""
    data_dict = data.to_dict(orient='records')
    try:
        conn.execute(table.insert(), data_dict)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def upload_waterings(data, conn: Connection, table: db.Table) -> None:
    """Uploads watering data to the database."""
    data_dict = data.to_dict(orient='records')
    for watering in data_dict:
        try:
            query = db.insert(table).values(plant_id = watering['plant_id'], datetime = watering['datetime'])
            conn.execute(query)
            conn.commit()
        except Exception as e:
            conn.rollback()


def load(recordings, waterings) -> None:
    """Main function to run the whole load script."""
    load_dotenv()
    db_engine = get_database_engine()
    db_connection = db_engine.connect()
    db_metadata = db.MetaData(schema=environ['DB_SCHEMA'])
    recording_table = db.Table(
        "recording", db_metadata, autoload_with=db_engine)
    watering_table = db.Table("watering", db_metadata, autoload_with=db_engine)
    upload_recordings(recordings, db_connection, recording_table)
    upload_waterings(waterings, db_connection, watering_table)
    db_connection.close()
