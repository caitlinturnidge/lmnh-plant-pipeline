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

RESAMPLE_RATE = '10T'
LINE_WIDTH = 2
FIG_WIDTH = 1200
FIG_HEIGHT = int(FIG_WIDTH / 4)

st.set_page_config(layout="wide")


def get_moisture_data(data: pd.DataFrame) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""

    return data.resample(
        RESAMPLE_RATE, on='datetime').mean().reset_index()


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
        # labelFontSize=TICK_LABEL_FONT_SIZE,
        # titleFontSize=AXIS_LABEL_FONT_SIZE,
    ).configure_title(
        # fontSize=TITLE_FONT_SIZE,
    )

    return chart


def get_temperature_data(data: pd.DataFrame) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""

    return data.resample(
        RESAMPLE_RATE, on='datetime').mean().reset_index()


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
        # labelFontSize=TICK_LABEL_FONT_SIZE,
        # titleFontSize=AXIS_LABEL_FONT_SIZE,
    ).configure_title(
        # fontSize=TITLE_FONT_SIZE,
    )

    return chart


if __name__ == "__main__":

    load_dotenv()

    db_engine = get_database_engine()
    db_connection = db_engine.connect()
    db_metadata = db.MetaData(schema=environ['DB_SCHEMA'])

    db_data = get_24hr_data('recording', db_engine, db_connection, db_metadata)

    st.sidebar.title('Plant Health Tracker')

    selected_plant = st.sidebar.selectbox(
        'Select Plant', db_data['plant_id'].unique())

    plant_id = db_data['plant_id'] == selected_plant
    data = db_data[plant_id]

    resample_rate = st.sidebar.slider(
        'Select sample rate (minutes)',
        min_value=1, max_value=60, value=10, step=1)

    RESAMPLE_RATE = f'{resample_rate}T'

    latest_data = data.iloc[-1]

    moisture_data = get_moisture_data(data)

    st.header('🚿 Soil Moisture')
    st.metric('Current Soil Moisture', f"{latest_data['soil_moisture']:.2f}%")
    st.altair_chart(get_soil_moisture_chart(moisture_data))

    st.divider()

    temperature_data = get_temperature_data(data)

    st.header('🌡️ Temperature')
    st.metric('Current Temperature', f"{latest_data['temperature']:.1f}°C")
    st.altair_chart(get_temperature_chart(temperature_data))

    image_dict = get_plant_images()

    if selected_plant in image_dict:
        st.sidebar.image(image_dict.get(selected_plant),
                         caption=f'Plant {selected_plant}')
    else:
        st.sidebar.text('No image available')

    locs = get_origin_locations()

    st.divider()

    st.sidebar.header('🌍 Location of Origin')
    st.sidebar.map(locs.iloc[selected_plant:selected_plant+1],
                   latitude='lat',
                   longitude='lon',
                   size=1000,
                   zoom=4)
