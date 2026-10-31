# ============================================
# Student Performance Prediction
# prediction.py
# ============================================

import joblib
import pandas as pd

# --------------------------------------------
# Load Model and Scaler
# --------------------------------------------

model = joblib.load("student_prediction_model.pkl")
scaler = joblib.load("scaler.pkl")

# --------------------------------------------
# Student Details
# --------------------------------------------

print("\n===== Student Performance Prediction =====\n")

gender = int(input("Gender (Male=1, Female=0): "))
age = int(input("Age: "))
department = int(input("Department (BCA=0, B.Tech=1, B.Sc=2, B.Com=3, BBA=4): "))
study_hours = float(input("Study Hours Per Day: "))
attendance = float(input("Attendance (%): "))
assignment = float(input("Assignment Score: "))
quiz = float(input("Quiz Score: "))
midterm = float(input("Midterm Marks: "))
previous = float(input("Previous Marks: "))
internet = int(input("Internet Access (Yes=1, No=0): "))
extra = int(input("Extra Classes (Yes=1, No=0): "))
sleep = float(input("Sleep Hours: "))
income = int(input("Family Income (Low=0, Medium=1, High=2): "))

# --------------------------------------------
# Create DataFrame
# --------------------------------------------

student = pd.DataFrame([{
    "Gender": gender,
    "Age": age,
    "Department": department,
    "Study_Hours": study_hours,
    "Attendance": attendance,
    "Assignment_Score": assignment,
    "Quiz_Score": quiz,
    "Midterm_Marks": midterm,
    "Previous_Marks": previous,
    "Internet_Access": internet,
    "Extra_Classes": extra,
    "Sleep_Hours": sleep,
    "Family_Income": income
}])

# --------------------------------------------
# Scale Data
# --------------------------------------------

student_scaled = scaler.transform(student)

# --------------------------------------------
# Prediction
# --------------------------------------------

prediction = model.predict(student_scaled)

# Probability (if supported by model)
try:
    probability = model.predict_proba(student_scaled)
except AttributeError:
    probability = None

# --------------------------------------------
# Result
# --------------------------------------------

print("\n========== Prediction Result ==========")

if prediction[0] == 1:
    print("Student Result : PASS")
else:
    print("Student Result : FAIL")

if probability is not None:
    print(f"Pass Probability : {probability[0][1]*100:.2f}%")
    print(f"Fail Probability : {probability[0][0]*100:.2f}%")

print("=======================================")