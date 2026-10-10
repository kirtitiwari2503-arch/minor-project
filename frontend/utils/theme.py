import streamlit as st


def apply_theme():
    theme = st.sidebar.selectbox(
        "Choose Theme",
        ["Green Theme", "White Theme"],
        key="nabha_theme"
    )

    if theme == "Green Theme":
        background = "#166534"
        text_color = "#FFFFFF"
        card_background = "#15803D"
    else:
        background = "#FFFFFF"
        text_color = "#166534"
        card_background = "#F0FDF4"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background};
            color: {text_color};
        }}

        [data-testid="stSidebar"] {{
            background-color: {card_background};
        }}

        [data-testid="stMarkdownContainer"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {{
            color: {text_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )