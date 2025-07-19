import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page

if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    switch_page("Login")
if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    from streamlit_extras.switch_page_button import switch_page
    switch_page("Login")

st.title("📈 Comparison View")

data = pd.read_csv("data.csv")
data["Bed Occupancy Rate"] = (data["Occupied Beds"] / data["Total Beds"]) * 100
data["Bed Turnover Rate"] = ((data["Discharges"] + data["Deaths"]) / data["Total Beds"]) * 100

st.plotly_chart(px.bar(data, x="Hospital", y="Bed Occupancy Rate", color="Hospital"))
st.plotly_chart(px.bar(data, x="Hospital", y="Bed Turnover Rate", color="Hospital"))
