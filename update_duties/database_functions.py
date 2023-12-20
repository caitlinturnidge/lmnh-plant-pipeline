
from dotenv import load_dotenv
from os import environ

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


def get_db_plant_ids(table_name: str, db_engine: db.Engine, connection: Connection, metadata,
                    datetime_cutoff: str = LITERAL_DAY_AGO):
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