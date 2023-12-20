
from datetime import datetime
from dotenv import load_dotenv
from os import environ
import pandas as pd

import sqlalchemy as db
from sqlalchemy.engine.base import Connection


class MSSQL_Database():

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



def add_duty(database: MSSQL_Database, plant_id: int, botanist_id: int):
    """
    Updates any duties in duty table with plant id and NULL end column to current datetime, and add a new duty for plant and botanist id.
    """
    
    try:
        duty_table = db.Table('duty', database.metadata, autoload_with=database.engine)
        # Update old duty:
        query = db.update(duty_table).values(end=datetime.now()).where((duty_table.c.plant_id == plant_id) & (duty_table.c.end == None))
        database.connection.execute(query)

        # Add new duty
        query = db.insert(duty_table).values(plant_id=plant_id, botanist_id=botanist_id)
        database.connection.execute(query)

        database.commit()

    except Exception as e:
        raise e


def get_db_plant_ids(database: MSSQL_Database) -> list:
    """Retrieves all plant ids from the plant table in the db."""
    try:
        plant_table = db.Table('plant', database.metadata, autoload_with=database.engine)
        query = db.select(plant_table)
        response = database.connection.execute(query)
        results = response.fetchall()
        return [row.id for row in results]

    except Exception as e:
        raise e
    

def get_active_duties(database: MSSQL_Database) -> pd.DataFrame:
    """Retrieves pandas df of all records in db duty table without an end date."""
    try:
        duty_table = db.Table('duty', database.metadata, autoload_with=database.engine)
        query = db.select(duty_table).where(duty_table.columns.end == None)
        response = database.connection.execute(query)
        results = response.fetchall()
        return pd.DataFrame(results)

    except Exception as e:
        raise e
    

def get_botanist_by_name(forename: str, surname: str, database: MSSQL_Database) -> pd.DataFrame:
    """Retrieves pandas df of first record in db botanist table with specified fore- and surname."""
    try:
        botanist_table = db.Table('botanist', database.metadata, autoload_with=database.engine)
        query = db.select(botanist_table).where(botanist_table.columns.firstname == forename and botanist_table.columns.lastname == surname)
        response = database.connection.execute(query)
        result = response.first()
        return list(result)

    except Exception as e:
        raise e


def get_table_records(table_name: str, database: MSSQL_Database) -> pd.DataFrame:
    """Retrieves all records as pandas df from specified table in db."""
    try:
        table = db.Table(table_name, database.metadata, autoload_with=database.engine)
        query = db.select(table)
        response = database.connection.execute(query)
        results = response.fetchall()
        return pd.DataFrame(results)

    except Exception as e:
        raise e
    

if __name__ == "__main__":
    load_dotenv()

    database = MSSQL_Database()

    add_duty(database, 5, 10)