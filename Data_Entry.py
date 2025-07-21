import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Entry", layout="wide")
st.title("📋 ICU Data Entry")

csv_file = "data.csv"

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Patient Name", "Age", "ICU Ward", "Notes"])
    df.to_csv(csv_file, index=False)

with st.form("entry_form"):
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=130)
    ward = st.selectbox("ICU Ward", ["ICU", "CCU", "NICU", "PICU"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Submit")

    if submitted:
        new_entry = pd.DataFrame([[name, age, ward, notes]], columns=["Patient Name", "Age", "ICU Ward", "Notes"])
        new_entry.to_csv(csv_file, mode="a", header=False, index=False)
        st.success("✅ Entry added successfully!")

st.subheader("📊 Current Records")
df = pd.read_csv(csv_file)
st.dataframe(df, use_container_width=True)
