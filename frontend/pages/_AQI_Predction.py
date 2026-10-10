import streamlit as st
from utils.theme import apply_theme

st.set_page_config(
    page_title="NABHA - AQI Prediction",
    page_icon="🌿",
    layout="wide"
)

apply_theme()

st.title("🌿 NABHA - AQI Prediction")

st.write(
    "Enter air quality and weather parameters "
    "to predict the Air Quality Index."
)

with st.form("prediction_form"):
    city = st.selectbox(
        "Select Your City",
        ["Mumbai", "Pune", "Nagpur", "Delhi", "Nashik"]
    )

    pm25 = st.number_input(
        "PM2.5 Level",
        min_value=0.0,
        value=24.6
    )

    pm10 = st.number_input(
        "PM10 Level",
        min_value=0.0,
        value=42.0
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=29.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0,
        max_value=100,
        value=65
    )

    submitted = st.form_submit_button("Predict AQI")

if submitted:
    st.warning(
        "The trained machine learning model is not "
        "connected yet. No actual prediction has been generated."
    )

st.caption(
    "Actual predictions will be available after "
    "connecting the trained ML model."
)