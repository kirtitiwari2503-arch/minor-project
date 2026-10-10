import streamlit as st
from utils.theme import apply_theme
from utils.advisory import get_health_advisory

st.set_page_config(
    page_title="NABHA - Health Advisory",
    page_icon="🌿",
    layout="wide"
)

apply_theme()

st.title("🌿 NABHA - Health Advisory")

st.write(
    "Get general health precautions based on "
    "air quality and your selected profile."
)

profile = st.selectbox(
    "Select Your Profile",
    [
        "General Adult",
        "Child",
        "Older Adult",
        "Sensitive to Air Pollution"
    ]
)

aqi_category = st.selectbox(
    "Select AQI Category",
    ["Good", "Moderate", "Poor", "Very Poor"]
)

if st.button("Get Health Advisory"):
    category_message, profile_message = get_health_advisory(
        aqi_category,
        profile
    )

    st.subheader("Your Health Advisory")

    st.write("Selected Profile:", profile)
    st.write("Air Quality:", aqi_category)

    st.info(category_message)
    st.warning(profile_message)

st.caption(
    "General health guidance only. This is not a medical diagnosis."
)