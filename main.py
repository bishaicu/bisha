import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
from streamlit_extras.switch_page_button import switch_page

if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    switch_page("Login")
if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    from streamlit_extras.switch_page_button import switch_page
    switch_page("Login")

st.set_page_config(page_title="ICU KPI Dashboard", layout="wide")

col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown("<h1 style='color:white; font-size:40px;'>Asir Cluster Health Sector – Bisha Region</h1>", unsafe_allow_html=True)

riyadh_time = datetime.now(pytz.timezone("Asia/Riyadh")).strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<h4 style='color:white;'>📅 {riyadh_time}</h4>", unsafe_allow_html=True)

if st.button("🔁 Refresh Data"):
    st.experimental_rerun()

try:
    data = pd.read_csv("data.csv")
except FileNotFoundError:
    st.warning("⚠️ Data file not found.")
    st.stop()

data["Bed Occupancy Rate"] = (data["Occupied Beds"] / data["Total Beds"]) * 100
data["Bed Turnover Rate"] = ((data["Discharges"] + data["Deaths"]) / data["Total Beds"]) * 100

if st.session_state.role == "admin":
    st.subheader("📊 KPI Comparison for All Hospitals")
    for hospital in data["Hospital"].unique():
        st.markdown(f"### 🏥 {hospital}")
        hospital_data = data[data["Hospital"] == hospital].iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Bed Occupancy Rate", f"{hospital_data['Bed Occupancy Rate']:.1f}%")
        with col2:
            st.metric("Bed Turnover Rate", f"{hospital_data['Bed Turnover Rate']:.1f}%")
    st.plotly_chart(px.bar(data, x="Hospital", y="Bed Occupancy Rate", color="Hospital"))
    st.plotly_chart(px.bar(data, x="Hospital", y="Bed Turnover Rate", color="Hospital"))
else:
    st.subheader("📝 Enter ICU Data")
    with st.form("entry_form"):
        date = st.date_input("Date")
        hospital = st.session_state["username"].replace("_user", "").replace("_", " ").title() + " Hospital"
        total_beds = st.number_input("Total ICU Beds", min_value=0)
        occupied_beds = st.number_input("Occupied ICU Beds", min_value=0)
        icu_patients = st.number_input("ICU Patients", min_value=0)
        discharges = st.number_input("Discharges", min_value=0)
        deaths = st.number_input("Deaths", min_value=0)
        readm_48h = st.number_input("Re-admissions 48h", min_value=0)
        infected = st.number_input("Infected Patients", min_value=0)
        unplanned_ext = st.number_input("Unplanned Extubations", min_value=0)
        intubated = st.number_input("Intubated Patients", min_value=0)
        vap = st.number_input("VAP Cases", min_value=0)
        vent_days = st.number_input("Ventilator Days", min_value=0)
        clabsi = st.number_input("CLABSI Cases", min_value=0)
        central_days = st.number_input("Central Line Days", min_value=0)
        cauti = st.number_input("CAUTI Cases", min_value=0)
        cath_days = st.number_input("Catheter Days", min_value=0)
        ulcer = st.number_input("Pressure Ulcer Cases", min_value=0)
        submitted = st.form_submit_button("Submit")
    if submitted:
        new_row = {
            "Date": date, "Hospital": hospital, "Total Beds": total_beds, "Occupied Beds": occupied_beds,
            "ICU Patients": icu_patients, "Discharges": discharges, "Deaths": deaths,
            "Re-admissions 48h": readm_48h, "Infected Patients": infected, "Unplanned_Ext": unplanned_ext,
            "Intubated Patients": intubated, "VAP Cases": vap, "Ventilator Days": vent_days,
            "CLABSI Cases": clabsi, "Central Line Days": central_days, "CAUTI Cases": cauti,
            "Catheter Days": cath_days, "Pressure Ulcer Cases": ulcer
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv("data.csv", index=False)
        st.success("✅ Data submitted successfully.")

if st.button("🚪 Logout"):
    st.session_state.clear()
    st.success("Logged out. Please refresh the page.")
