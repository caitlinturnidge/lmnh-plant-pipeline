"""Upload image URLs to the database so they can be used in the dashboard."""

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
    

def upload_images(images: list, engine: db.Engine, conn: Connection, metadata) -> None:
    """Seeds database with image data."""
    plant_table = db.Table('image', metadata, autoload_with=engine)

    try:
        conn.execute(plant_table.insert(), images)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    

def main() -> None:
    """Reads in the image data csv and uploads it."""
    images_df = pd.read_csv('image_data_STATIC.csv')
    images_df = images_df[['plant_id','image_url','license','license_name','license_url']]
    images = images_df.to_dict('records')
    
    engine = get_database_engine()
    conn = engine.connect()
    metadata = db.MetaData(schema=environ['DB_SCHEMA'])

    upload_images(images, engine, conn, metadata)


if __name__ == "__main__":

    main()