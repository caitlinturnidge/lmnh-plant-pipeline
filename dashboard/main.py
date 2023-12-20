"""Script for Streamlit dashboard."""

import pandas as pd
import altair as alt
import streamlit as st
from datetime import timedelta, datetime

from os import environ

from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.engine.base import Connection

from db_functions import (
    get_database_engine,
    get_24hr_data
)

from data_utils import (
    get_plant_images,
    get_origin_locations
)

LINE_WIDTH = 2
FIG_WIDTH = 1200
FIG_HEIGHT = int(FIG_WIDTH / 4)
TICK_LABEL_FONT_SIZE = 14
AXIS_LABEL_FONT_SIZE = 16

st.set_page_config(layout="wide")


def get_moisture_data(data: pd.DataFrame, sample_rate: str) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""

    return data.resample(
        sample_rate, on='datetime').mean().reset_index()


def get_soil_moisture_chart(chart_data: pd.DataFrame) -> alt.Chart:

    y_min = chart_data['soil_moisture'].min()
    y_max = chart_data['soil_moisture'].max()

    chart = alt.Chart(chart_data).mark_line(
        interpolate='cardinal',
        tension=0.8,
        strokeWidth=LINE_WIDTH,
    ).encode(
        x=alt.X('datetime:T', axis=alt.Axis(
            title='Time', format='%H:%M')),
        y=alt.Y('soil_moisture:Q', scale=alt.Scale(
            domain=[y_min - 1, y_max + 1]), axis=alt.Axis(title='Soil Moisture (%)'))
    ).properties(
        width=FIG_WIDTH,
        height=FIG_HEIGHT,
    ).configure_axis(
        labelFontSize=TICK_LABEL_FONT_SIZE,
        titleFontSize=AXIS_LABEL_FONT_SIZE,
    ).interactive()

    return chart


def get_temperature_data(data: pd.DataFrame, sample_rate: str) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""

    return data.resample(
        sample_rate, on='datetime').mean().reset_index()


def get_temperature_chart(chart_data: pd.DataFrame) -> alt.Chart:

    y_min = chart_data['temperature'].min()
    y_max = chart_data['temperature'].max()

    chart = alt.Chart(chart_data).mark_line(
        interpolate='cardinal',
        tension=0.8,
        strokeWidth=LINE_WIDTH,
    ).encode(
        x=alt.X('datetime:T', axis=alt.Axis(
            title='Time', format='%H:%M')),
        y=alt.Y('temperature:Q', scale=alt.Scale(
            domain=[y_min - 1, y_max + 1]), axis=alt.Axis(title='Temperature (°C)'))
    ).properties(
        width=FIG_WIDTH,
        height=FIG_HEIGHT,
    ).configure_axis(
        labelFontSize=TICK_LABEL_FONT_SIZE,
        titleFontSize=AXIS_LABEL_FONT_SIZE,
    )

    return chart


def get_selected_plant(chart_data: pd.DataFrame) -> int:
    """Builds sidebar selector and gets chosen plant."""

    return st.sidebar.selectbox('Select Plant', chart_data['plant_id'].unique())


def get_individual_plant_data(chart_data: pd.DataFrame, plant_selected: int) -> pd.DataFrame:
    """Uses selected plant ID to get individual plant data."""

    plant_id = chart_data['plant_id'] == plant_selected

    return chart_data[plant_id]


def build_resample_rate_slider() -> str:
    """Builds sidebar resample rate slider, returns chosen resample rate."""

    resample_rate = st.sidebar.slider(
        'Select sample rate (minutes)',
        min_value=1, max_value=60, value=10, step=1)

    return f'{resample_rate}T'


def build_moisture_header_and_metric(chart_data: pd.DataFrame) -> None:
    """Builds soil moisture header and metric."""

    latest_data = chart_data.iloc[-1]
    st.header('🚿 Soil Moisture')
    st.metric('Current Soil Moisture',
              f"{latest_data['soil_moisture']:.1f}%", delta='4')


def build_temperature_header_and_metric(chart_data: pd.DataFrame) -> None:
    """Builds temperature header and metric."""

    latest_data = chart_data.iloc[-1]
    st.header('🌡️ Temperature')
    st.metric('Current Temperature', f"{latest_data['temperature']:.1f}°C")


def display_sidebar_image(selected_plant: int) -> None:
    """Gets plant images and displays in sidebar if available."""

    image_dict = get_plant_images()

    if selected_plant in image_dict:
        st.sidebar.image(image_dict.get(selected_plant),
                         caption=f'Plant {selected_plant}')
    else:
        st.sidebar.text('No image available')


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

    db_engine = get_database_engine()
    db_connection = db_engine.connect()
    db_metadata = db.MetaData(schema=environ['DB_SCHEMA'])

    db_data = get_24hr_data('recording', db_engine, db_connection, db_metadata)

    db_data = pd.read_csv('mock_data_multi_plants.csv')
    db_data = db_data.rename(columns={'recording_taken': 'datetime'})
    db_data['datetime'] = pd.to_datetime(db_data['datetime'])

    st.sidebar.title('Plant Health Tracker')

    selected_plant = get_selected_plant(db_data)
    data = get_individual_plant_data(db_data, selected_plant)

    resample_rate = build_resample_rate_slider()

    build_moisture_header_and_metric(data)
    moisture_data = get_moisture_data(data, resample_rate)
    st.altair_chart(get_soil_moisture_chart(moisture_data))

    st.divider()

    build_temperature_header_and_metric(data)
    temperature_data = get_temperature_data(data, resample_rate)
    st.altair_chart(get_temperature_chart(temperature_data))

    display_sidebar_image(selected_plant)

    st.divider()

    display_sidebar_map(selected_plant)

    #  Placeholder
    with st.expander('Open to see more'):
        st.write('This is more content.')


if __name__ == "__main__":
    main()
