from os import environ
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql
from sqlalchemy.engine.base import Connection

from load import get_database_connection

NOW = datetime.now() - timedelta(hours=24)

def get_oldest_records(db_conn: Connection):
    try:
        db_conn.execute(sql.text("BEGIN TRANSACTION;"))
        db_conn.execute(sql.text(f"USE {environ['DB_NAME']};"))

        query = sql.text(
            f"""SELECT * FROM {environ['DB_SCHEMA']}.watering
                WHERE (:plant_id, :last_watered)""")
        db_conn.execute(query, row)

        db_conn.execute(sql.text("COMMIT;"))
    except Exception as e:
        db_conn.execute(sql.text("ROLLBACK;"))
        raise e
    

if __name__ == "__main__":

    load_dotenv()