import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ICU Login", layout="centered")

st.title("🔐 ICU Dashboard Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "admin123":
        st.success("Login successful! Welcome, admin.")
        st.switch_page("Data entry")  # ✅ Corrected page name
    else:
        st.error("Invalid credentials")