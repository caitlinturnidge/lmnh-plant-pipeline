"""Script for Streamlit dashboard."""

import pandas as pd
import altair as alt
import streamlit as st
from datetime import timedelta


RESAMPLE_RATE = '10T'
LINE_WIDTH = 2
FIG_WIDTH = 1200
FIG_HEIGHT = int(FIG_WIDTH / 4)

st.set_page_config(layout="wide")

if __name__ == "__main__":

    data = pd.read_csv('mock_data.csv')
    data['recording_taken'] = pd.to_datetime(data['recording_taken'])
    data.head()

    # Sidebar content
    st.sidebar.header('Plant Health Tracker')

    resample_rate = st.sidebar.slider(
        'Select sample rate (minutes)',
        min_value=1, max_value=60, value=10, step=1)

    RESAMPLE_RATE = f'{resample_rate}T'

    # Time range sliders
    total_hours = data['recording_taken'].max() - data['recording_taken'].min()
    total_hours = total_hours.total_seconds() / 3600

    selected_hours = st.sidebar.slider(
        'Select number of hours to display',
        min_value=1, max_value=int(total_hours), value=int(total_hours / 2), step=1
    )

    start_datetime = st.sidebar.slider(
        'Select starting point',
        min_value=0, max_value=int(total_hours - selected_hours), value=0, step=1
    )

    end_datetime = start_datetime + selected_hours

    # Filter data based on selected time range
    filtered_data = data[
        (data['recording_taken'] >= data['recording_taken'].min() + timedelta(hours=start_datetime)) &
        (data['recording_taken'] <= data['recording_taken'].min() +
         timedelta(hours=end_datetime))
    ]

    latest_data = data.iloc[-1]

    moisture_data = filtered_data.resample(
        RESAMPLE_RATE, on='recording_taken').mean().reset_index()
    y_min = moisture_data['soil_moisture'].min()
    y_max = moisture_data['soil_moisture'].max()

    chart = alt.Chart(moisture_data).mark_line(
        interpolate='cardinal',
        tension=0.8,
        strokeWidth=LINE_WIDTH,
    ).encode(
        x=alt.X('recording_taken:T', axis=alt.Axis(
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

    st.header('Soil Moisture')
    st.subheader(f"Latest Soil Moisture: {latest_data['soil_moisture']:.2f}%")
    st.altair_chart(chart)

    st.divider()

    temperature_data = data.resample(
        RESAMPLE_RATE, on='recording_taken').mean().reset_index()
    y_min = temperature_data['temperature'].min()
    y_max = temperature_data['temperature'].max()

    chart = alt.Chart(temperature_data).mark_line(
        interpolate='cardinal',
        tension=0.8,
        strokeWidth=LINE_WIDTH,
    ).encode(
        x=alt.X('recording_taken:T', axis=alt.Axis(
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

    st.header('Temperature')
    st.subheader(f"Latest Temperature: {latest_data['temperature']:.2f}°C")
    st.altair_chart(chart)

    st.sidebar.image('https://perenual.com/storage/species_image/2961_ficus_elastica/small/533092219_8da73ba0d2_b.jpg',
                     caption='Plant 34')
