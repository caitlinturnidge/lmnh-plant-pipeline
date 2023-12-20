"""This script seeds the database plant, location and duty tables with .csv files."""


import csv
from os import environ

from dotenv import load_dotenv

import numpy as np
import pandas as pd

import sqlalchemy as db
from sqlalchemy.engine.base import Connection


load_dotenv()


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


def upload_locations(locations: list, engine: db.Engine, conn: Connection, metadata) -> None:
    """Seeds database with location data."""
    location_table = db.Table('location', metadata, autoload_with=engine)

    try:
        conn.execute(location_table.insert(), locations)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def upload_plants(plants: list, engine: db.Engine, conn: Connection, metadata) -> None:
    """Seeds database with plant data."""
    plant_table = db.Table('plant', metadata, autoload_with=engine)

    try:
        conn.execute(plant_table.insert(), plants)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def upload_duties(duties: list, engine: db.Engine, conn: Connection, metadata) -> None:
    """Seeds database with information about each botanists responsibility."""
    duty_table = db.Table('duty', metadata, autoload_with=engine)

    try:
        conn.execute(duty_table.insert(), duties)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def upload() -> None:
    """Combines each function to seed the database."""

    locations = pd.read_csv('seed_locations.csv').replace(np.nan, None).to_dict('records')

    plants_df = pd.read_csv('seed_plants.csv')
    plants_df['origin_location'] = plants_df['origin_location'].fillna(-1).astype(int)
    plants_df = plants_df.replace({np.nan: None, -1: None})
    plants = plants_df.to_dict('records')
    
    duties = pd.read_csv('seed_duties.csv').replace(np.nan, None).to_dict('records')

    engine = get_database_engine()
    conn = engine.connect()
    metadata = db.MetaData(schema=environ['DB_SCHEMA'])

    upload_locations(locations, engine, conn, metadata)

    upload_plants(plants, engine, conn, metadata)

    upload_duties(duties, engine, conn, metadata)


if __name__ == "__main__":

    upload()
