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


def get_moisture_data(data: pd.DataFrame) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""

    return data.resample(
        RESAMPLE_RATE, on='recording_taken').mean().reset_index()


def get_soil_moisture_chart(chart_data: pd.DataFrame) -> alt.Chart:

    y_min = chart_data['soil_moisture'].min()
    y_max = chart_data['soil_moisture'].max()

    chart = alt.Chart(chart_data).mark_line(
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

    return chart


def get_temperature_data(data: pd.DataFrame) -> pd.DataFrame:
    """Gets moisture data from filtered dataframe."""

    return data.resample(
        RESAMPLE_RATE, on='recording_taken').mean().reset_index()


def get_temperature_chart(chart_data: pd.DataFrame) -> alt.Chart:

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

    return chart


if __name__ == "__main__":

    data_multi = pd.read_csv('mock_data_multi_plants.csv')
    data_multi['recording_taken'] = pd.to_datetime(
        data_multi['recording_taken'])
    data_multi.head()

    st.sidebar.title('Plant Health Tracker')

    selected_plant = st.sidebar.selectbox(
        'Select Plant', data_multi['plant_id'].unique())

    plant_id = data_multi['plant_id'] == selected_plant
    data = data_multi[plant_id]

    resample_rate = st.sidebar.slider(
        'Select sample rate (minutes)',
        min_value=1, max_value=60, value=10, step=1)

    RESAMPLE_RATE = f'{resample_rate}T'

    total_hours = data['recording_taken'].max() - data['recording_taken'].min()
    total_hours = total_hours.total_seconds() / 3600

    selected_hours = st.sidebar.slider(
        'Select number of hours to display',
        min_value=1, max_value=int(total_hours), value=int(total_hours / 2), step=1
    )

    start_datetime = st.sidebar.slider(
        'Select window start',
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

    moisture_data = get_moisture_data(filtered_data)

    st.header('🚿 Soil Moisture')
    st.metric('Current Soil Moisture', f"{latest_data['soil_moisture']:.2f}%")
    st.altair_chart(get_soil_moisture_chart(moisture_data))

    st.divider()

    temperature_data = get_temperature_data(data)

    st.header('🌡️ Temperature')
    st.metric('Current Temperature', f"{latest_data['temperature']:.1f}°C")
    st.altair_chart(get_temperature_chart(temperature_data))

    image_dict = {
        0: 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/medium/2560px-Epipremnum_aureum_31082012.jpg',
        1: 'https://perenual.com/storage/species_image/1007_asclepias_curassavica/small/51757177616_7ca0baaa87_b.jpg',
        2: 'https://perenual.com/storage/species_image/2015_colocasia_esculenta/small/24325097844_14719030a3_b.jpg',
        3: 'https://perenual.com/storage/species_image/2868_euphorbia_cotinifolia/small/51952243235_061102bd05_b.jpg',
        4: 'https://perenual.com/storage/species_image/855_anthurium_andraeanum/small/49388458462_0ef650db39_b.jpg',
        5: 'https://perenual.com/storage/species_image/2045_cordyline_fruticosa/small/2560px-Cordyline_fruticosa_Rubra_1.jpg',
        6: 'https://perenual.com/storage/species_image/2961_ficus_elastica/small/533092219_8da73ba0d2_b.jpg',
    }
    st.sidebar.image(image_dict.get(selected_plant),
                     caption=f'Plant {selected_plant}')

    locs = pd.read_csv('../origin_data_STATIC.csv')

    st.divider()

    st.header('🌍 Origin Location')
    st.map(locs.iloc[selected_plant:selected_plant+1],
           latitude='lat',
           longitude='lon',
           size=1000,
           zoom=4)
