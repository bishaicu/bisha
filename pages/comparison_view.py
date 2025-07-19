import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page

# ---------- Login Guard ----------
if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    switch_page("00_Login")

# ---------- Page Setup ----------
st.set_page_config(layout="wide")
st.title("📊 ICU KPI Comparison View (with Donut Charts)")

# ---------- Load Data ----------
data = pd.read_csv("data.csv")

# ---------- Auto Calculations ----------
data["Bed Occupancy Rate"] = (data["Occupied Beds"] / data["Total Beds"]) * 100
data["Bed Turnover Rate"] = ((data["Discharges"] + data["Deaths"]) / data["Total Beds"]) * 100
data["VAP Rate"] = data.apply(lambda row: (row["VAP Cases"] / row["Ventilator Days"]) * 1000 if row["Ventilator Days"] > 0 else 0, axis=1)
data["CLABSI Rate"] = data.apply(lambda row: (row["CLABSI Cases"] / row["Central Line Days"]) * 1000 if row["Central Line Days"] > 0 else 0, axis=1)
data["CAUTI Rate"] = data.apply(lambda row: (row["CAUTI Cases"] / row["Catheter Days"]) * 1000 if row["Catheter Days"] > 0 else 0, axis=1)
data["Infection Rate"] = data.apply(lambda row: (row["Infected Patients"] / row["ICU Patients"]) * 100 if row["ICU Patients"] > 0 else 0, axis=1)

# ---------- Donut Chart: Bed Occupancy ----------
st.subheader("🍩 Donut Charts: Bed Occupancy Breakdown")
for hospital in data["Hospital"].unique():
    row = data[data["Hospital"] == hospital].iloc[0]
    fig = px.pie(
        names=["Occupied Beds", "Available Beds"],
        values=[row["Occupied Beds"], row["Total Beds"] - row["Occupied Beds"]],
        hole=0.5,
        title=f"{hospital} - Bed Occupancy"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Donut Chart: ICU Outcomes ----------
st.subheader