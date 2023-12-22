"""Script for Streamlit dashboard."""

from datetime import timedelta, datetime

from dotenv import load_dotenv
import pandas as pd
import streamlit as st

import db_functions
import graphics
import s3_data_extraction as s3_functions

from data_utils import (
    get_origin_locations
)

LINE_WIDTH = 2
FIG_WIDTH = 750
FIG_HEIGHT = 400  # int(FIG_WIDTH / 4)
TICK_LABEL_FONT_SIZE = 14
AXIS_LABEL_FONT_SIZE = 16

ERROR_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/a/ac/RGTR_bw_%28404%29.svg"

st.set_page_config(
    layout="wide", page_title="LMNH Plant Health", page_icon="🌿")


# Cached resources and data:

@st.cache_resource
def fetch_database_object() -> db_functions.MSSQL_Database:
    """Cacheable function to return a database (connection) object."""
    return db_functions.MSSQL_Database()


@st.cache_resource
def fetch_s3_client_object():
    """Cacheable function to return boto3 client to access s3 bucket."""
    return s3_functions.create_s3_client()


@st.cache_data(show_spinner='Plants be loading... 🌱')
def get_24hr_data(table_name: str, _database: db_functions.MSSQL_Database) -> pd.DataFrame:
    """Cacheable function to return last 24hrs of data from database."""
    return db_functions.get_24hr_data(table_name, _database)


@st.cache_data()
def get_min_s3_date(_s3_client) -> datetime:
    """Cacheable function to return minimum date (to the month) of data in s3 bucket."""
    return s3_functions.get_earliest_data_date(_s3_client).date()


@st.cache_data()
def get_s3_data_for_type_and_date_ranges(_s3_client, data_type: str, range_start: datetime,
                                         range_end: datetime) -> pd.DataFrame:
    """
    Cacheable function to return s3 data of given type between the months of the date range given
    (range_start and range_end MUST be date objects).
    """
    return s3_functions.get_s3_data_for_type_and_date_ranges(
        _s3_client, data_type, range_start, range_end)


@st.cache_data(show_spinner="Retrieving image...")
def get_plant_image_url(plant_id: int, _database: db_functions.MSSQL_Database) -> str:
    """Function to retrieve url of plant with given id from db."""
    return db_functions.get_plant_image_url(plant_id, _database)


# Data manipulation:

def get_moisture_data(data: pd.DataFrame, sample_rate: str) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""
    return data.resample(
        sample_rate, on='datetime').mean().reset_index()


def get_temperature_data(data: pd.DataFrame, sample_rate: str) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""
    return data.resample(
        sample_rate, on='datetime').mean().reset_index()


def get_individual_plant_data(chart_data: pd.DataFrame, plant_selected: int) -> pd.DataFrame:
    """Uses selected plant ID to get individual plant data."""
    plant_id = (chart_data['plant_id'] == plant_selected)
    return chart_data[plant_id]



# Streamlit dashboard objects:

def get_selected_plant(chart_data: pd.DataFrame) -> int:
    """Builds sidebar selector and gets chosen plant."""
    plant_ids = chart_data['plant_id'].unique()
    plant_ids.sort()
    return st.sidebar.selectbox('Plant ID', plant_ids)


def build_resample_rate_slider() -> str:
    """Builds sidebar resample rate slider, returns chosen resample rate."""
    resample_rate = st.sidebar.slider(
        'Select sample rate (minutes)',
        min_value=1, max_value=60, value=10, step=1)
    return f'{resample_rate}T'


def build_date_range_slider(min_date_possible: datetime) -> list[datetime]:
    """
    Builds slider for user to select data sample range; default selected range is only the current
    day.
    """
    today = datetime.today().date()
    return st.slider('Sample range (selection outside of current day may incur delays): ',
        min_value=min_date_possible,
        max_value=datetime.today().date(),
        value=(today, today))


def build_moisture_header_and_metric(chart_data: pd.DataFrame, selected_plant: int) -> None:
    """Builds soil moisture header and metric."""
    col1, col2 = st.columns([1, 3])
    latest_data = chart_data.iloc[-1]
    with col1:
        st.subheader('🚿 Soil Moisture')
    with col2:
        st.metric(f'Current Level',
                  f"{latest_data['soil_moisture']:.1f}%")


def build_temperature_header_and_metric(chart_data: pd.DataFrame, selected_plant: int) -> None:
    """Builds temperature header and metric."""
    col1, col2 = st.columns([1, 3])
    with col1:
        latest_data = chart_data.iloc[-1]
        st.subheader('🌡️ Temperature')
    with col2:
        st.metric(
            f'Current Temperature (Plant {selected_plant})', f"{latest_data['temperature']:.1f}°C")


def display_sidebar_image(plant_id: int, image_url: str) -> None:
    """Gets plant images and displays in sidebar if available."""
    if image_url and ('upgrade_access' not in image_url):
        st.sidebar.image(image_url,
                         caption=f'Plant {plant_id}')
    else:
        st.sidebar.image(ERROR_IMAGE_URL,
                         caption='Image not found!')


def display_sidebar_map(selected_plant: int) -> None:
    """Gets locations and displays map if available."""
    locs = get_origin_locations()
    st.sidebar.header('🌍 Location of Origin')
    st.sidebar.map(locs.iloc[selected_plant:selected_plant+1],
                   latitude='lat',
                   longitude='lon',
                   size=1000,
                   zoom=4)

    

def main():
    """Main logic to run dashboard."""

    load_dotenv()

    # Fetching db data:
    database = fetch_database_object()
    db_data = get_24hr_data('recording', database)


    # Sidebar:
    st.sidebar.title('Plant Selector')

    selected_plant_id = get_selected_plant(db_data)
    st.sidebar.write('##')
    resample_rate = build_resample_rate_slider()


    # Current values section:
    idx = db_data.groupby('plant_id')['datetime'].idxmax()

    latest_readings_df = db_data.loc[
        idx, ['plant_id', 'soil_moisture', 'temperature', 'datetime']].reset_index()

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.title('🪴 Plant Health Tracker')

    with col2:
        st.metric('Total Number of Plants 🌿',
                  len(db_data['plant_id'].unique()))

    with col3:
        min_soil_moisture_index = latest_readings_df['soil_moisture'].idxmin()
        min_soil_moisture_plant_id = latest_readings_df.loc[min_soil_moisture_index, 'plant_id']

        st.metric('Lowest Moisture ⚠️',
                  f'Plant {min_soil_moisture_plant_id}')

    st.write('#')
    st.subheader('💦 Current Moisture Levels')

    with st.expander('Show graph.'):
        current_moisture_chart = graphics.get_current_moisture_levels_chart(latest_readings_df)
        st.altair_chart(current_moisture_chart, use_container_width=True)

    st.write('#')
    st.subheader('🌡️ Current Temperature Levels')

    with st.expander('Show graph.'):
        current_temperature_chart = graphics.get_current_temperatures_chart(latest_readings_df)
        st.altair_chart(current_temperature_chart, use_container_width=True)

    st.divider()


    # Plant specific historic section:

    st.title(f'Plant {selected_plant_id}')

    # Datetime slider and selection from user
    s3_client = fetch_s3_client_object()
    min_s3_date = get_min_s3_date(s3_client)
    date_range = build_date_range_slider(min_s3_date)
    datetime_range = (datetime.combine(date_range[0], datetime.min.time()),
                      datetime.combine(date_range[1] + timedelta(days=1), datetime.min.time()))

    # Fetching data from s3, and restricting to current plant
    selected_plant_data = get_individual_plant_data(db_data, selected_plant_id)
    s3_data = get_s3_data_for_type_and_date_ranges(
        s3_client, 'recording', date_range[0], date_range[1])
    
    if not s3_data.empty:
        selected_plant_s3_data = get_individual_plant_data(s3_data, selected_plant_id)
        selected_plant_data = pd.concat([selected_plant_data, selected_plant_s3_data])

    selected_plant_data = selected_plant_data[
        (selected_plant_data['datetime'] >= datetime_range[0]) &
        (selected_plant_data['datetime'] <= datetime_range[1])
        ]


    build_moisture_header_and_metric(selected_plant_data, selected_plant_id)
    with st.expander('Show graph.'):

        col1, col2 = st.columns([3, 1])

        with col1:

            moisture_data = get_moisture_data(selected_plant_data, resample_rate)
            st.altair_chart(graphics.get_soil_moisture_chart(moisture_data))

        with col2:
            current_moisture_chart = graphics.adjust_chart_dimensions(
                                            current_moisture_chart, height = 400)
            st.altair_chart(current_moisture_chart, use_container_width=True)

    st.divider()


    build_temperature_header_and_metric(selected_plant_data, selected_plant_id)
    with st.expander('Show graph.'):

        col1, col2 = st.columns([3, 1])

        with col1:

            temperature_data = get_temperature_data(selected_plant_data, resample_rate)
            st.altair_chart(graphics.get_temperature_chart(temperature_data))

        with col2:
            current_temperature_chart = graphics.adjust_chart_dimensions(current_temperature_chart, height = 400)
            st.altair_chart(current_temperature_chart, use_container_width=True)
            
    plant_image_url = get_plant_image_url(int(selected_plant_id), database)
    display_sidebar_image(selected_plant_id, plant_image_url)

    st.divider()

    display_sidebar_map(selected_plant_id)

    if st.sidebar.button('🌀 Get latest readings', help='Gets latest data from the database'):
        get_24hr_data.clear()


if __name__ == "__main__":
    main()
