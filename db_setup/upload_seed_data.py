
import csv
from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql


load_dotenv()


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


def upload_locations(conn, locations: list) -> None:
    """Seeds database with location data."""
    try:
        conn.execute(sql.text("BEGIN TRANSACTION;"))
        conn.execute(sql.text(f"USE {environ['DB_NAME']};"))

        for row in locations:
            query = sql.text(
                f"""INSERT INTO {environ['DB_SCHEMA']}.location (latitude, longitude, town, country_code, city, continent) 
                    VALUES (:latitude, :longitude, :town, :country_code, :city, :continent)""")
            conn.execute(query, row)

        conn.execute(sql.text("COMMIT;"))
    except Exception as e:
        conn.execute(sql.text("ROLLBACK;"))
        raise e


if __name__ == "__main__":

    
    with open('seed_locations.csv', 'r', encoding="utf-8") as csv_file:
        locations = list(csv.DictReader(csv_file))

    with open('seed_plants.csv', 'r', encoding="utf-8") as csv_file:
        plants = list(csv.DictReader(csv_file))

    engine = create_engine("mssql+pymssql://beta:beta1@c9-plants-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com:1433/plants")

    conn = engine.connect()

    upload_locations(conn, locations)