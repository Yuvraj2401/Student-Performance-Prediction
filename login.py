# ==========================================
# Student Performance Prediction
# login.py
# ==========================================

import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Performance Prediction - Login",
    page_icon="🔐",
    layout="centered"
)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# Admin Credentials
# -----------------------------
USERNAME = "admin"
PASSWORD = "admin123"

# -----------------------------
# Login Function
# -----------------------------
def login(username, password):
    return username == USERNAME and password == PASSWORD

# -----------------------------
# Login Page
# -----------------------------
if not st.session_state.logged_in:

    st.title("🎓 Student Performance Prediction")
    st.subheader("Admin Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if login(username, password):

            st.session_state.logged_in = True

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Username or Password")

# -----------------------------
# Dashboard
# -----------------------------
else:

    st.title("🎓 Welcome Admin")

    st.success("You are logged in successfully.")

    st.write("Use the sidebar to navigate through the project modules.")

    st.markdown("---")

    st.subheader("Project Modules")

    st.write("✅ Student Performance Prediction")
    st.write("✅ Dashboard")
    st.write("✅ Prediction History")
    st.write("✅ Export Reports")
    st.write("✅ Database")

    st.markdown("---")

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.success("Logged out successfully.")

        st.rerun()