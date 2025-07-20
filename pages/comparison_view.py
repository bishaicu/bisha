import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz



# ---- Role Guard ----
if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("🚫 Access denied. Admin only.")
    st.stop()

# ---- Page Setup ----
st.set_page_config(layout="wide")
st.title("📊 Comparison View (Admin Only)")

st.write("Welcome, Admin! This page is restricted to you.")


# ---------- Header and Time ----------
st.markdown("<h1 style='color:white; font-size:40px;'>ICU KPI Comparison View – Bisha Region</h1>", unsafe_allow_html=True)
riyadh_time = datetime.now(pytz.timezone("Asia/Riyadh")).strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<h5 style='color:white;'>📅 Current Riyadh Time: {riyadh_time}</h5>", unsafe_allow_html=True)

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
st.subheader("🍩 Donut Charts: ICU Patient Outcomes")
for hospital in data["Hospital"].unique():
    row = data[data["Hospital"] == hospital].iloc[0]
    discharged = row["Discharges"]
    deaths = row["Deaths"]
    remaining = row["ICU Patients"] - discharged - deaths
    values = [discharged, deaths, max(0, remaining)]
    labels = ["Discharges", "Deaths", "Still in ICU"]

    fig = px.pie(
        names=labels,
        values=values,
        hole=0.5,
        title=f"{hospital} - ICU Patient Status"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- KPI Metrics ----------
st.subheader("📋 ICU KPI Metric Cards")
for hospital in data["Hospital"].unique():
    st.markdown(f"### 🏥 {hospital}")
    row = data[data["Hospital"] == hospital].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bed Occupancy Rate", f"{row['Bed Occupancy Rate']:.1f}%")
    col2.metric("Bed Turnover Rate", f"{row['Bed Turnover Rate']:.1f}%")
    col3.metric("ICU Patients", int(row["ICU Patients"]))
    col4.metric("Discharges", int(row["Discharges"]))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Deaths", int(row["Deaths"]))
    col2.metric("Infection Rate", f"{row['Infection Rate']:.1f}%")
    col3.metric("VAP Rate", f"{row['VAP Rate']:.1f} / 1000d")
    col4.metric("CLABSI Rate", f"{row['CLABSI Rate']:.1f} / 1000d")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CAUTI Rate", f"{row['CAUTI Rate']:.1f} / 1000d")
    col2.metric("Re-admissions 48h", int(row["Re-admissions 48h"]))
    col3.metric("Intubated Patients", int(row["Intubated Patients"]))
    col4.metric("Pressure Ulcer Cases", int(row["Pressure Ulcer Cases"]))

    st.markdown("---")
