"""Database functions for dashboard."""

import pandas as pd
from datetime import timedelta, datetime
from os import environ

from dotenv import load_dotenv
import pandas as pd
import sqlalchemy as db


load_dotenv()
LITERAL_DAY_AGO = (datetime.now() - timedelta(hours=24))
TODAY = datetime.today()


class MSSQL_Database():
    """
    Class containing key objects used in database interactions; aims to encapsulate and abstract
    db connection details from other classes.
    """

    def __init__(self) -> None:
        """
        Connects to engine, creates connection, and stores resulting objects along with the
        database metadata as attributes of the image of the class.
        """
        load_dotenv()
        try:
            self.engine = db.create_engine(
                f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}:{environ['DB_PORT']}/{environ['DB_NAME']}?charset=utf8"
            )
            self.connection = self.engine.connect()
            self.metadata = db.MetaData(schema=environ['DB_SCHEMA'])
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise e

    def commit(self):
        """Commits db connection for changes made to persist externally."""
        self.connection.commit()

    def close(self):
        """Closes db connection."""
        self.connection.close()



def get_24hr_data(table_name: str, database: MSSQL_Database,
                  datetime_cutoff: str = LITERAL_DAY_AGO):
    """
    Retrieves records from the last 24 hours (by attribute 'datetime') from db table with given
    name.
    """
    try:
        table = db.Table(table_name, database.metadata, autoload_with=database.engine)
        query = db.select(table).where(
            table.columns.datetime > datetime_cutoff)
        response = database.connection.execute(query)
        results = response.fetchall()
        return pd.DataFrame(results)

    except Exception as e:
        raise e
