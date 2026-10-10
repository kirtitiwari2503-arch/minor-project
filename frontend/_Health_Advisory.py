import streamlit as st

st.title("🌿 NABHA - Health Advisory")

aqi = st.slider("Select AQI", 0, 300, 78)

profile = st.selectbox(
    "Select Your Profile",
    ["General Adult", "Child", "Older Adult",
     "Sensitive to Air Pollution"]
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