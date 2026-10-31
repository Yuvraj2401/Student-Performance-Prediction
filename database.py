# ==========================================
# Student Performance Prediction
# database.py
# ==========================================

import sqlite3
import pandas as pd

# ==========================================
# Connect Database
# ==========================================

conn = sqlite3.connect("students.db", check_same_thread=False)

cursor = conn.cursor()

# ==========================================
# Create Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(

id INTEGER PRIMARY KEY AUTOINCREMENT,

student_name TEXT,

gender TEXT,

age INTEGER,

department TEXT,

study_hours REAL,

attendance REAL,

assignment_score REAL,

quiz_score REAL,

midterm_marks REAL,

previous_marks REAL,

internet_access TEXT,

extra_classes TEXT,

sleep_hours REAL,

family_income TEXT,

prediction TEXT,

prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

# ==========================================
# Insert Data
# ==========================================

def save_prediction(
        student_name,
        gender,
        age,
        department,
        study_hours,
        attendance,
        assignment_score,
        quiz_score,
        midterm_marks,
        previous_marks,
        internet_access,
        extra_classes,
        sleep_hours,
        family_income,
        prediction):

    cursor.execute("""

    INSERT INTO predictions(

    student_name,
    gender,
    age,
    department,
    study_hours,
    attendance,
    assignment_score,
    quiz_score,
    midterm_marks,
    previous_marks,
    internet_access,
    extra_classes,
    sleep_hours,
    family_income,
    prediction

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """,(

    student_name,
    gender,
    age,
    department,
    study_hours,
    attendance,
    assignment_score,
    quiz_score,
    midterm_marks,
    previous_marks,
    internet_access,
    extra_classes,
    sleep_hours,
    family_income,
    prediction

    ))

    conn.commit()

# ==========================================
# Display All Records
# ==========================================

def show_predictions():

    df = pd.read_sql(
        "SELECT * FROM predictions",
        conn
    )

    return df

# ==========================================
# Search Student
# ==========================================

def search_student(name):

    query = """

    SELECT *

    FROM predictions

    WHERE student_name LIKE ?

    """

    df = pd.read_sql(
        query,
        conn,
        params=(f"%{name}%",)
    )

    return df

# ==========================================
# Delete Record
# ==========================================

def delete_record(record_id):

    cursor.execute(

        "DELETE FROM predictions WHERE id=?",

        (record_id,)

    )

    conn.commit()

# ==========================================
# Export Excel
# ==========================================

def export_excel():

    df = show_predictions()

    df.to_excel(

        "Prediction_History.xlsx",

        index=False

    )

    print("Excel Exported Successfully")

# ==========================================
# Total Predictions
# ==========================================

def total_predictions():

    cursor.execute(

        "SELECT COUNT(*) FROM predictions"

    )

    total = cursor.fetchone()[0]

    return total

# ==========================================
# Pass Count
# ==========================================

def total_pass():

    cursor.execute(

        "SELECT COUNT(*) FROM predictions WHERE prediction='PASS'"

    )

    return cursor.fetchone()[0]

# ==========================================
# Fail Count
# ==========================================

def total_fail():

    cursor.execute(

        "SELECT COUNT(*) FROM predictions WHERE prediction='FAIL'"

    )

    return cursor.fetchone()[0]

# ==========================================
# Close Database
# ==========================================

def close():

    conn.close()