import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

df = pd.read_excel(r"C:\Users\DELL\Downloads\Student_Performance_1000_Records_With_Names.xlsx")

X = df.drop("Final_Result", axis=1)
y = df["Final_Result"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

joblib.dump(scaler, "scaler.pkl")

print("Scaler saved successfully.")

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

joblib.dump(model, "student_prediction_model.pkl")

print("Model saved successfully.")