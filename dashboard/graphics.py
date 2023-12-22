"""Modules containing functions to make altair chart graphics used in dashboard (main.py)."""

import altair as alt
import pandas as pd


LINE_WIDTH = 2
FIG_WIDTH = 750
FIG_HEIGHT = 400  # int(FIG_WIDTH / 4)
TICK_LABEL_FONT_SIZE = 14
AXIS_LABEL_FONT_SIZE = 16


def get_soil_moisture_chart(chart_data: pd.DataFrame) -> alt.Chart:
    """
    Creates altair line chart of moisture against time for given df (of a singular plant's info).
    """
    y_min = chart_data['soil_moisture'].min()
    y_max = chart_data['soil_moisture'].max()

    chart = alt.Chart(chart_data).mark_line(
        interpolate='cardinal',
        tension=0.8,
        strokeWidth=LINE_WIDTH,
    ).encode(
        x=alt.X('datetime:T', axis=alt.Axis(title='Time')),
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


def get_temperature_chart(chart_data: pd.DataFrame) -> alt.Chart:
    """
    Creates altair line chart of temperature against time for a given df (of a singular plant's
    info).
    """
    y_min = chart_data['temperature'].min()
    y_max = chart_data['temperature'].max()

    chart = alt.Chart(chart_data).mark_line(
        interpolate='cardinal',
        tension=0.8,
        strokeWidth=LINE_WIDTH,
    ).encode(
        x=alt.X('datetime:T', axis=alt.Axis(
            title='Time')),
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


def get_current_moisture_levels_chart(latest_recording_data: pd.DataFrame) -> alt.Chart:
    """
    Creates an altair bar chart of current moisture levels from df of current plant recording data.
    """
    return alt.Chart(latest_recording_data).mark_bar().encode(
        y=alt.Y('plant_id:N', sort='-x', title='Plant ID'),
        x=alt.X('soil_moisture:Q', title='Soil Moisture (%)'),
        color=alt.Color('soil_moisture:Q', scale=alt.Scale(
            scheme='redblue'), legend=None),
        tooltip=['plant_id', 'soil_moisture']
    ).properties(
        width=1000,
        height=600
    )


def get_current_temperatures_chart(latest_recording_data: pd.DataFrame) -> alt.Chart:
    """
    Creates an altair bar chart of current temperature levels from df of current plant recording
    data.
    """
    return alt.Chart(latest_recording_data).mark_bar().encode(
        y=alt.Y('plant_id:N', sort='-x', title='Plant ID'),
        x=alt.X('temperature:Q', title='Temperature (°C)'),
        color=alt.Color('temperature:Q', scale=alt.Scale(
            scheme='redblue', reverse=True), legend=None),
        tooltip=['plant_id', 'temperature']
    ).properties(
        width=1000,
        height=400
    )


def adjust_chart_dimensions(chart: alt.Chart, width: int = None, height: int = None) -> alt.Chart:
    """Returns a copy of the input chart with dimensions adjusted to values given."""
    if not width:
        width = chart.width

    if not height:
        height = chart.height

    return chart.properties(width=width, height=height)
