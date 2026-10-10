import streamlit as st
from utils.theme import apply_theme

st.set_page_config(
    page_title="NABHA",
    page_icon="🌿",
    layout="wide"
)

apply_theme()

st.title("🌿 NABHA")
st.subheader("Air Quality Prediction and Health Advisory System")

st.write(
    "NABHA provides air quality information, "
    "AQI predictions, and health recommendations "
    "based on pollution levels."
)

st.divider()

st.header("👤 User Profile")

name = st.text_input("Enter Your Name")

city = st.selectbox(
    "Choose Your Preferred City",
    ["Mumbai", "Pune", "Nagpur", "Delhi", "Nashik"]
)

if st.button("Save Profile"):
    st.session_state["user_name"] = name
    st.session_state["preferred_city"] = city

    st.success("Profile saved for this session!")

if "user_name" in st.session_state:
    st.write("Name:", st.session_state["user_name"])
    st.write("Preferred City:", st.session_state["preferred_city"])

st.caption(
    "Profile preferences are currently saved only "
    "for the active session."
)