import streamlit as st
from utils.theme import apply_theme

st.set_page_config(
    page_title="NABHA Dashboard",
    page_icon="🌿",
    layout="wide"
)

apply_theme()

st.title("🌿 NABHA - Air Quality Dashboard")

st.write(
    "Monitor air quality and weather information "
    "for your selected city."
)

city = st.selectbox(
    "Select Your City",
    ["Mumbai", "Pune", "Nagpur", "Delhi", "Nashik"]
)

st.subheader(f"Air Quality Information - {city}")

col1, col2, col3 = st.columns(3)

col1.metric("AQI", "78")
col2.metric("PM2.5", "24.6 µg/m³")
col3.metric("PM10", "42 µg/m³")

st.subheader("Air Quality Category")
st.info("Moderate")

st.subheader("Weather Information")

col4, col5 = st.columns(2)

col4.metric("Temperature", "29°C")
col5.metric("Humidity", "65%")

st.caption(
    "Sample values only. These are not live readings."
)