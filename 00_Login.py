import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# -------------- User Credentials --------------
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "kah": {"password": "kah123", "role": "kah_user"},
    "tathleeth": {"password": "tath123", "role": "tathleeth_user"},
    "alayah": {"password": "ala123", "role": "alalaya_user"}
}

# -------------- Page Config --------------
st.set_page_config(page_title="Bisha ICU Dashboard Login", layout="centered")

# -------------- Dark Theme --------------
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    h1, h2, h3, h4, .stTextInput > label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# -------------- Title --------------
st.title("🔐 Bisha ICU Dashboard Login")

# -------------- Already Logged In --------------
if "username" in st.session_state and "role" in st.session_state:
    st.success(f"✅ Already logged in as `{st.session_state.username}`")
    if st.session_state["role"] == "admin":
        if st.button("🔁 Proceed to Comparison View"):
            switch_page("comparison_view")
    else:
        if st.button("✍️ Proceed to Editing Page"):
            switch_page("editing")
    st.stop()

# -------------- Login Form --------------
username = st.selectbox("👤 Select User", list(users.keys()))
password = st.text_input("🔒 Password", type="password")

if st.button("🔓 Login"):
    if username in users and users[username]["password"] == password:
        st.session_state["username"] = username
        st.session_state["role"] = users[username]["role"]
        st.success("✅ Login successful!")

        # Redirect based on role
        if users[username]["role"] == "admin":
            switch_page("comparison_view")
        else:
            switch_page("edit_view")
    else:
        st.error("❌ Invalid username or password")
