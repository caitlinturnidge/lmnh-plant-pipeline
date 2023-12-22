"""Script for Streamlit dashboard."""

import pandas as pd
import altair as alt
import streamlit as st
from datetime import timedelta, datetime

from os import environ

from dotenv import load_dotenv

from db_functions import (
    MSSQL_Database,
    get_24hr_data
)

from data_utils import (
    get_plant_images,
    get_origin_locations
)

LINE_WIDTH = 2
FIG_WIDTH = 750
FIG_HEIGHT = 400  # int(FIG_WIDTH / 4)
TICK_LABEL_FONT_SIZE = 14
AXIS_LABEL_FONT_SIZE = 16

st.set_page_config(
    layout="wide", page_title="LMNH Plant Health", page_icon="🌿")


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
    ).interactive()

    return chart


def get_selected_plant(chart_data: pd.DataFrame) -> int:
    """Builds sidebar selector and gets chosen plant."""

    return st.sidebar.selectbox('Plant ID', chart_data['plant_id'].unique())


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

    database = MSSQL_Database()

    db_data = get_24hr_data('recording', database)

    st.sidebar.title(f'Plant Selector')

    selected_plant = get_selected_plant(db_data)
    data = get_individual_plant_data(db_data, selected_plant)
    st.sidebar.write('##')
    resample_rate = build_resample_rate_slider()

    idx = db_data.groupby('plant_id')['datetime'].idxmax()

    new_df = db_data.loc[
        idx, ['plant_id', 'soil_moisture', 'temperature', 'datetime']].reset_index()

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:

        st.title(f'🪴 Plant Health Tracker')

    with col2:
        st.metric('Total Number of Plants 🌿',
                  len(db_data['plant_id'].unique()))

    with col3:

        min_soil_moisture_index = new_df['soil_moisture'].idxmin()
        min_soil_moisture_plant_id = new_df.loc[min_soil_moisture_index, 'plant_id']

        st.metric('Lowest Moisture ⚠️',
                  f'Plant {min_soil_moisture_plant_id}')

    st.write('#')
    st.subheader('💦 Current Moisture Levels')

    with st.expander('Show graph.'):
        chart = alt.Chart(new_df).mark_bar().encode(
            y=alt.Y('plant_id:N', sort='-x', title='Plant ID'),
            x=alt.X('soil_moisture:Q', title='Soil Moisture (%)'),
            color=alt.Color('soil_moisture:Q', scale=alt.Scale(
                scheme='redblue'), legend=None),
            tooltip=['plant_id', 'soil_moisture']
        ).properties(
            width=1000,
            height=600,
            # title='Current Soil Moisture Levels'
        )

        st.altair_chart(chart, use_container_width=True)

    st.write('#')

    st.subheader('🌡️ Current Temperature Levels')

    with st.expander('Show graph.'):
        chart = alt.Chart(new_df).mark_bar().encode(
            y=alt.Y('plant_id:N', sort='-x', title='Plant ID'),
            x=alt.X('temperature:Q', title='Temperature (°C)'),
            color=alt.Color('temperature:Q', scale=alt.Scale(
                scheme='redblue', reverse=True), legend=None),
            tooltip=['plant_id', 'temperature']
        ).properties(
            width=1000,
            height=400,
            # title='Current Soil Moisture Levels'
        )
        st.altair_chart(chart, use_container_width=True)

    st.divider()

    st.title(f'Plant {selected_plant}')

    build_moisture_header_and_metric(data, selected_plant)

    #  Placeholder
    with st.expander(f'Show graph.'):

        col1, col2 = st.columns([3, 1])

        with col1:

            moisture_data = get_moisture_data(data, resample_rate)
            st.altair_chart(get_soil_moisture_chart(moisture_data))

        with col2:

            idx = db_data.groupby('plant_id')['datetime'].idxmax()

            new_df = db_data.loc[
                idx, ['plant_id', 'soil_moisture', 'temperature', 'datetime']].reset_index()

            chart = alt.Chart(new_df).mark_bar().encode(
                y=alt.Y('plant_id:N', sort='-x', title='Plant ID'),
                x=alt.X('soil_moisture:Q', title='Soil Moisture'),
                color=alt.Color('soil_moisture:Q', scale=alt.Scale(
                    scheme='redblue'), legend=None),
                tooltip=['plant_id', 'soil_moisture']
            ).properties(
                width=600,
                height=400,
                # title='Current Soil Moisture Levels'
            )

            st.altair_chart(chart, use_container_width=True)

    st.divider()

    build_temperature_header_and_metric(data, selected_plant)
    with st.expander('Show graph.'):

        temperature_data = get_temperature_data(data, resample_rate)
        st.altair_chart(get_temperature_chart(temperature_data))

    display_sidebar_image(selected_plant)

    st.divider()

    display_sidebar_map(selected_plant)

    if st.sidebar.button('🌀 Get latest readings', help='Gets latest data from the database'):
        get_24hr_data.clear()


if __name__ == "__main__":
    main()
