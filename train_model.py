
# ===========================================
# Student Performance Prediction
# train_model.py
# ===========================================

import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# ===========================================
# Configuration
# ===========================================

DATASET_PATH = "Student_Performance_1000_Records_With_Names.xlsx"
MODEL_DIR = Path("model_files")
MODEL_DIR.mkdir(exist_ok=True)

# ===========================================
# Load Dataset
# ===========================================

df = pd.read_excel(DATASET_PATH)

print("Dataset shape:", df.shape)
print("\nDataset columns:")
print(df.columns.tolist())

# ===========================================
# Remove personal identification columns
# ===========================================

df.drop(
    columns=["Student_ID", "Student_Name"],
    errors="ignore",
    inplace=True
)

# ===========================================
# Handle missing values
# ===========================================

# Forward fill first, then use column-wise fallback values.
df = df.ffill()

for col in df.columns:
    if df[col].isna().any():
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode = df[col].mode()
            df[col] = df[col].fillna(
                mode.iloc[0] if not mode.empty else "Unknown"
            )

# ===========================================
# Encode categorical columns
# ===========================================

target_column = "Final_Result"

if target_column not in df.columns:
    raise ValueError(
        f"Target column '{target_column}' was not found. "
        f"Available columns: {df.columns.tolist()}"
    )

# Encode each categorical feature independently.
feature_encoders = {}
target_encoder = LabelEncoder()

for col in df.columns:
    if col == target_column:
        continue

    if (
        pd.api.types.is_object_dtype(df[col])
        or isinstance(df[col].dtype, pd.CategoricalDtype)
        or pd.api.types.is_string_dtype(df[col])
    ):
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col].astype(str))
        feature_encoders[col] = encoder

df[target_column] = target_encoder.fit_transform(
    df[target_column].astype(str)
)

# ===========================================
# Features and Target
# ===========================================

X = df.drop(columns=[target_column])
y = df[target_column]

# Preserve the exact feature order for the Streamlit app.
feature_names = X.columns.tolist()

print("\nFeatures used by the model:")
for index, feature in enumerate(feature_names, start=1):
    print(f"{index}. {feature}")

# ===========================================
# Train-Test Split
# ===========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ===========================================
# Feature Scaling
# ===========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===========================================
# Compare Models
# ===========================================

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),
    "Support Vector Machine": SVC(probability=True)
}

best_accuracy = -1
best_model = None
best_model_name = None

print("\n========== MODEL ACCURACY ==========")

for name, model in models.items():
    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)

    print(f"{name}: {accuracy * 100:.2f}%")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# ===========================================
# Save Model, Scaler and Encoders
# ===========================================

joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
joblib.dump(best_model, MODEL_DIR / "student_prediction_model.pkl")

# Save everything needed to interpret inputs and predictions.
bundle = {
    "model": best_model,
    "scaler": scaler,
    "feature_names": feature_names,
    "feature_encoders": feature_encoders,
    "target_encoder": target_encoder,
    "model_name": best_model_name,
    "accuracy": best_accuracy,
    "categorical_columns": list(feature_encoders.keys())
}

joblib.dump(bundle, MODEL_DIR / "student_model_bundle.pkl")

print("\n=================================")
print("Best model:", best_model_name)
print(f"Test accuracy: {best_accuracy * 100:.2f}%")
print("Model files saved in:", MODEL_DIR.resolve())
print("=================================")

# ===========================================
# Demonstration Prediction
# ===========================================

# Use an existing dataset row as a demonstration input.
# Replace these values with actual student details in your app.
sample = X.iloc[[0]].copy()

sample_scaled = scaler.transform(sample)
prediction = best_model.predict(sample_scaled)

predicted_label = target_encoder.inverse_transform(
    prediction.astype(int)
)[0]

print("\nDemonstration prediction:", predicted_label)
