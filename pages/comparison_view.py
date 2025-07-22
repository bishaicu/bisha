import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import os
import base64
from io import BytesIO

st.set_page_config(page_title="ICU KPI Comparison", layout="wide")
st.title("🏥 ICU KPI Dashboard – Comparison View")

# Load ICU Data
csv_path = "icu_data.csv"
if not os.path.exists(csv_path):
    st.warning("No ICU data submitted yet.")
    st.stop()

try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"❌ Failed to read data: {e}")
    st.stop()

if df.empty:
    st.info("📭 No data available.")
    st.stop()

# KPI Calculations
df["Occupancy Rate (%)"] = (df["Occupied Beds"] / df["Total Beds"] * 100).round(2)
df["Discharge Rate (%)"] = (df["Discharges (Last 24h)"] / df["Occupied Beds"] * 100).round(2)
df["Mortality Rate (%)"] = (df["Deaths (Last 24h)"] / df["Occupied Beds"] * 100).round(2)
df["ICU Bed Turnover Rate"] = (df["Discharges (Last 24h)"] / df["Total Beds"]).round(2)
df["Infection Rate (%)"] = (df["Infected Patients (Last 24h)"] / df["Occupied Beds"] * 100).round(2)
df["Readmission Rate (%)"] = (df["Re-admissions within 48h"] / df["Occupied Beds"] * 100).round(2)

# Riyadh Time
riyadh_time = datetime.now(pytz.timezone("Asia/Riyadh")).strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"**🕒 Riyadh Time:** `{riyadh_time}`")

# Filters
dates = sorted(df["Date"].unique(), reverse=True)
selected_date = st.selectbox("📅 Filter by Date", dates)
hospitals = ["All"] + sorted(df["Hospital"].unique())
selected_hospital = st.selectbox("🏥 Filter by Hospital", hospitals)

filtered_df = df[df["Date"] == selected_date]
if selected_hospital != "All":
    filtered_df = filtered_df[filtered_df["Hospital"] == selected_hospital]

# Show Data
st.subheader("📋 Filtered ICU Data")
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.subheader("📊 KPI Comparison Charts")
kpi_list = [
    "Occupancy Rate (%)", "Discharge Rate (%)", "Mortality Rate (%)",
    "ICU Bed Turnover Rate", "Infection Rate (%)", "Readmission Rate (%)"
]

for kpi in kpi_list:
    if not filtered_df.empty:
        fig = px.bar(filtered_df, x="Hospital", y=kpi, color=kpi,
                     color_continuous_scale=["red", "orange", "green"],
                     text_auto=True, title=kpi)
        st.plotly_chart(fig, use_container_width=True)

# Excel Export
def generate_excel_download_link(df, filename):
    if df.empty:
        return "⚠️ No data to export."
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='ICU KPI')
    writer.close()
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href=\"data:application/octet-stream;base64,{b64}\" download=\"{filename}\">📥 Download KPI Report as Excel</a>'
    return href

st.markdown("---")
st.markdown(generate_excel_download_link(filtered_df, f"icu_kpi_{selected_date}.xlsx"), unsafe_allow_html=True)