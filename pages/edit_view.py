import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page


# ---- Role Guard ----
if "role" not in st.session_state or st.session_state["role"] == "admin":
    st.error("🚫 Access denied. Not allowed for admin.")
    st.stop()

# ---- Page Setup ----
st.set_page_config(layout="wide")
st.title("📝 ICU Data Entry (Hospital Staff Only)")

st.write("Welcome hospital team! You can enter and manage your ICU data here.")

# ---------- Load Existing Data ----------
try:
    data = pd.read_csv("data.csv")
except FileNotFoundError:
    data = pd.DataFrame(columns=[
        "Date", "Hospital", "Total Beds", "Occupied Beds", "ICU Patients",
        "Discharges", "Deaths", "Re-admissions 48h", "Infected Patients",
        "Unplanned_Ext", "Intubated Patients", "VAP Cases", "Ventilator Days",
        "CLABSI Cases", "Central Line Days", "CAUTI Cases", "Catheter Days",
        "Pressure Ulcer Cases"
    ])

# ---------- Detect Hospital Name ----------
hospital = st.session_state.get("username", "").replace("_user", "").replace("_", " ").title() + " Hospital"

# ---------- KPI Form ----------
with st.form("icu_data_entry"):
    date = st.date_input("📅 Date")

    st.markdown("### 🛏 Bed Information")
    total_beds = st.number_input("Total ICU Beds", min_value=0)
    occupied_beds = st.number_input("Occupied ICU Beds", min_value=0)

    st.markdown("### 👥 Patient Flow")
    icu_patients = st.number_input("ICU Patients", min_value=0)
    discharges = st.number_input("Discharges", min_value=0)
    deaths = st.number_input("Deaths", min_value=0)
    readm_48h = st.number_input("Re-admissions within 48h", min_value=0)

    st.markdown("### 🦠 Infections & Complications")
    infected = st.number_input("Infected Patients", min_value=0)
    unplanned_ext = st.number_input("Unplanned Extubations", min_value=0)
    intubated = st.number_input("Intubated Patients", min_value=0)

    st.markdown("### 🩺 Device Use & Safety Events")
    vap = st.number_input("VAP Cases", min_value=0)
    vent_days = st.number_input("Ventilator Days", min_value=0)
    clabsi = st.number_input("CLABSI Cases", min_value=0)
    central_days = st.number_input("Central Line Days", min_value=0)
    cauti = st.number_input("CAUTI Cases", min_value=0)
    cath_days = st.number_input("Catheter Days", min_value=0)
    ulcer = st.number_input("Pressure Ulcer Cases", min_value=0)

    submitted = st.form_submit_button("💾 Submit Data")

if submitted:
    new_row = {
        "Date": date,
        "Hospital": hospital,
        "Total Beds": total_beds,
        "Occupied Beds": occupied_beds,
        "ICU Patients": icu_patients,
        "Discharges": discharges,
        "Deaths": deaths,
        "Re-admissions 48h": readm_48h,
        "Infected Patients": infected,
        "Unplanned_Ext": unplanned_ext,
        "Intubated Patients": intubated,
        "VAP Cases": vap,
        "Ventilator Days": vent_days,
        "CLABSI Cases": clabsi,
        "Central Line Days": central_days,
        "CAUTI Cases": cauti,
        "Catheter Days": cath_days,
        "Pressure Ulcer Cases": ulcer
    }

    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    data.to_csv("data.csv", index=False)
    st.success("✅ Data submitted successfully!")