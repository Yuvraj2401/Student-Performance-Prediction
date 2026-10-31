# ==========================================
# Student Performance Prediction
# export_report.py
# ==========================================

import sqlite3
import pandas as pd
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ==========================================
# Create Reports Folder
# ==========================================

if not os.path.exists("reports"):
    os.makedirs("reports")

# ==========================================
# Database Connection
# ==========================================

conn = sqlite3.connect("students.db")

# ==========================================
# Read Prediction Data
# ==========================================

df = pd.read_sql(
    "SELECT * FROM predictions",
    conn
)

# ==========================================
# Export Excel
# ==========================================

def export_excel():

    file = "reports/Prediction_Report.xlsx"

    df.to_excel(
        file,
        index=False
    )

    print("Excel Report Saved Successfully")

# ==========================================
# Export PDF
# ==========================================

def export_pdf():

    file = "reports/Prediction_Report.pdf"

    pdf = SimpleDocTemplate(file)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b><font size=16>"
        "Student Performance Prediction Report"
        "</font></b>",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Paragraph("<br/><br/>", styles["Normal"]))

    data = [list(df.columns)]

    for row in df.values.tolist():
        data.append(row)

    table = Table(data)

    table.setStyle(

        TableStyle([

            ('BACKGROUND',(0,0),(-1,0),colors.darkblue),

            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('BACKGROUND',(0,1),(-1,-1),colors.beige),

            ('ALIGN',(0,0),(-1,-1),'CENTER'),

            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

            ('BOTTOMPADDING',(0,0),(-1,0),10),

        ])

    )

    elements.append(table)

    pdf.build(elements)

    print("PDF Report Saved Successfully")

# ==========================================
# Summary
# ==========================================

def report_summary():

    total = len(df)

    passed = len(df[df["prediction"]=="PASS"])

    failed = len(df[df["prediction"]=="FAIL"])

    print("\n========== Report Summary ==========")

    print("Total Predictions :", total)

    print("PASS :", passed)

    print("FAIL :", failed)

    print("====================================")

# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    report_summary()

    export_excel()

    export_pdf()

    print("\nReports Generated Successfully")

    conn.close()