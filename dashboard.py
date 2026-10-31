# ==========================================
# Student Performance Prediction Dashboard
# dashboard.py
# ==========================================

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Dashboard")

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("students.db")

df = pd.read_sql(
    "SELECT * FROM predictions",
    conn
)

# -----------------------------
# Check Data
# -----------------------------
if df.empty:
    st.warning("No prediction records found.")
    st.stop()

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Project Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Predictions",
        len(df)
    )

with col2:
    st.metric(
        "PASS Students",
        len(df[df["prediction"] == "PASS"])
    )

with col3:
    st.metric(
        "FAIL Students",
        len(df[df["prediction"] == "FAIL"])
    )

st.divider()

# -----------------------------
# Prediction History
# -----------------------------
st.subheader("Prediction History")

st.dataframe(df)

# -----------------------------
# PASS vs FAIL Chart
# -----------------------------
st.subheader("PASS vs FAIL")

result = df["prediction"].value_counts()

fig, ax = plt.subplots()

ax.bar(result.index, result.values)

ax.set_xlabel("Result")

ax.set_ylabel("Students")

ax.set_title("PASS vs FAIL")

st.pyplot(fig)

# -----------------------------
# Department-wise Students
# -----------------------------
st.subheader("Department Wise Students")

dept = df["department"].value_counts()

fig, ax = plt.subplots()

ax.bar(dept.index, dept.values)

ax.set_xlabel("Department")

ax.set_ylabel("Students")

st.pyplot(fig)

# -----------------------------
# Attendance Distribution
# -----------------------------
st.subheader("Attendance Distribution")

fig, ax = plt.subplots()

ax.hist(df["attendance"], bins=10)

ax.set_xlabel("Attendance")

ax.set_ylabel("Students")

st.pyplot(fig)

# -----------------------------
# Study Hours Distribution
# -----------------------------
st.subheader("Study Hours")

fig, ax = plt.subplots()

ax.hist(df["study_hours"], bins=8)

ax.set_xlabel("Study Hours")

ax.set_ylabel("Students")

st.pyplot(fig)

# -----------------------------
# Family Income
# -----------------------------
st.subheader("Family Income")

income = df["family_income"].value_counts()

fig, ax = plt.subplots()

ax.pie(
    income.values,
    labels=income.index,
    autopct="%1.1f%%"
)

st.pyplot(fig)

# -----------------------------
# Average Scores
# -----------------------------
st.subheader("Average Marks")

average = pd.DataFrame({

    "Assignment":[df["assignment_score"].mean()],

    "Quiz":[df["quiz_score"].mean()],

    "Midterm":[df["midterm_marks"].mean()],

    "Previous":[df["previous_marks"].mean()]

})

st.bar_chart(average.T)

# -----------------------------
# Download Data
# -----------------------------
st.subheader("Download Prediction History")

csv = df.to_csv(index=False)

st.download_button(

    "Download CSV",

    csv,

    file_name="Prediction_History.csv",

    mime="text/csv"

)

# -----------------------------
# Footer
# -----------------------------
st.success("Dashboard Loaded Successfully")