"""Database functions for dashboard."""

import pandas as pd
import altair as alt
import streamlit as st
from datetime import timedelta, datetime

from os import environ

from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.engine.base import Connection


load_dotenv()
LITERAL_DAY_AGO = (datetime.now() - timedelta(hours=24))
TODAY = datetime.today()


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


def get_24hr_data(table_name: str, db_engine: db.Engine, connection: Connection, metadata,
                  datetime_cutoff: str = LITERAL_DAY_AGO):
    """
    Retrieves records from the last 24 hours (by attribute 'datetime') from db table with given name.
    """
    try:
        table = db.Table(table_name, metadata, autoload_with=db_engine)
        query = db.select(table).where(
            table.columns.datetime > datetime_cutoff)
        response = connection.execute(query)
        results = response.fetchall()
        return pd.DataFrame(results)

    except Exception as e:
        raise e
