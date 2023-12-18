"""File to load the clean recording and watering data into the short term database."""
from os import environ
import csv

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql


def get_database_connection():
    """Returns the connection to the database."""
    try:
        engine = create_engine(
            f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8"
        )
        connection = engine.connect()
        return connection
    except Exception as e:
        print(f"Error creating database connection: {e}")
        raise e


def get_recordings_csv() -> list:
    """Gets the cleaned recordings csv and returns it."""
    with open('sample.csv', 'r', encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def get_waterings_csv() -> list:
    """Gets the cleaned waterings csv and returns it."""
    with open('sample.csv', 'r', encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def upload_recordings(conn) -> None:
    """Uploads recording data to the database."""
    data = get_recordings_csv()

    try:
        conn.execute(sql.text("BEGIN TRANSACTION;"))
        conn.execute(sql.text(f"USE {environ['DB_NAME']};"))

        for row in data:
            query = sql.text(
                f"""INSERT INTO {environ['DB_SCHEMA']}.recording (plant_id, soil_moisture, temperature, datetime) 
                    VALUES (:plant_id, :soil_moisture, :temperature, :recording_taken)""")
            conn.execute(query, row)

        conn.execute(sql.text("COMMIT;"))
    except Exception as e:
        conn.execute(sql.text("ROLLBACK;"))
        raise e


def upload_waterings(conn) -> None:
    """Uploads watering data to the database."""
    data = get_waterings_csv()

    try:
        conn.execute(sql.text("BEGIN TRANSACTION;"))
        conn.execute(sql.text(f"USE {environ['DB_NAME']};"))

        for row in data:
            query = sql.text(
                f"""INSERT INTO {environ['DB_SCHEMA']}.watering (plant_id, datetime) 
                    VALUES (:plant_id, :last_watered)""")
            conn.execute(query, row)

        conn.execute(sql.text("COMMIT;"))
    except Exception as e:
        conn.execute(sql.text("ROLLBACK;"))
        raise e


def load() -> None:
    """Main function to run the whole load script."""
    connection = get_database_connection()
    upload_recordings(connection)
    upload_waterings(connection)
    connection.close()


if __name__ == "__main__":
    load_dotenv()
    load()
