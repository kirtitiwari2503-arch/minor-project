import streamlit as st

st.set_page_config(
    page_title="NABHA",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 NABHA")
st.subheader("Air Quality Monitoring and Health Advisory")

st.write(
    "Welcome to NABHA, an air quality awareness project."
)

section = st.sidebar.selectbox(
    "Select Section",
    [
        "Home",
        "Health Advisory",
        "Air Quality Information"
    ]
)

if section == "Home":
    st.header("Welcome to NABHA")
    st.write("Learn about air quality and its effects on health.")

elif section == "Health Advisory":
    st.header("🌿 Health Advisory")

    aqi = st.slider("Select AQI", 0, 300, 78)

    profile = st.selectbox(
        "Select Your Profile",
        [
            "General Adult",
            "Child",
            "Older Adult",
            "Sensitive to Air Pollution"
        ]
    )

    if aqi <= 50:
        category = "Good"
        advice = "Continue normal activities and monitor air quality."
    elif aqi <= 100:
        category = "Moderate"
        advice = "Monitor air quality before prolonged outdoor activity."
    elif aqi <= 150:
        category = "Poor"
        advice = "Reduce prolonged or strenuous outdoor activity."
    elif aqi <= 200:
        category = "Very Poor"
        advice = "Limit outdoor exposure and follow local guidance."
    else:
        category = "Severe"
        advice = "Minimize outdoor exposure and follow official guidance."

    st.metric("Example AQI", aqi)
    st.subheader("Air Quality: " + category)
    st.info(advice)
    st.write("Selected Profile:", profile)
    st.caption("Example values only, not live AQI readings.")

elif section == "Air Quality Information":
    st.header("Air Quality Information")
    st.write(
        "AQI helps describe the level of air pollution."
    )
    st.info(
        "Air quality readings are not connected yet. "
        "This is a project demonstration."
    )
 