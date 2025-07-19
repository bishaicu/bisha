import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    switch_page("Login")
if "role" not in st.session_state:
    st.error("🚫 You must be logged in. Redirecting to login...")
    from streamlit_extras.switch_page_button import switch_page
    switch_page("Login")

st.title("📝 Edit ICU Data")
data = pd.read_csv("data.csv")

hospital = st.session_state.get("username", "").replace("_user", "").replace("_", " ").title() + " Hospital"

with st.form("edit_form"):
    date = st.date_input("Date")
    total_beds = st.number_input("Total Beds", min_value=0)
    occupied_beds = st.number_input("Occupied Beds", min_value=0)
    discharges = st.number_input("Discharges", min_value=0)
    deaths = st.number_input("Deaths", min_value=0)
    submitted = st.form_submit_button("Submit")

if submitted:
    new_row = {
        "Date": date, "Hospital": hospital, "Total Beds": total_beds,
        "Occupied Beds": occupied_beds, "Discharges": discharges, "Deaths": deaths
    }
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    data.to_csv("data.csv", index=False)
    st.success("Data updated.")
