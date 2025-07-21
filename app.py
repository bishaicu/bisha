import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Disable Streamlit telemetry for Hugging Face compatibility
import os
os.environ["STREAMLIT_DISABLE_USAGE_STATS"] = "1"
os.environ["STREAMLIT_HOME"] = "/tmp"

# Redirect to login page
switch_page("00_Login")