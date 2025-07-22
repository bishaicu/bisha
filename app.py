import os
os.environ["STREAMLIT_DISABLE_USAGE_STATS"] = "1"
os.environ["STREAMLIT_HOME"] = "/tmp"

import streamlit as st
from streamlit_extras.switch_page_button 
import switch_page

switch_page("00_Login")
