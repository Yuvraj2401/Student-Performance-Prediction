
import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# Load Saved Model Bundle
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
BUNDLE_PATH = BASE_DIR / "model_files" / "student_model_bundle.pkl"

@st.cache_resource
def load_bundle():
    return joblib.load(BUNDLE_PATH)

st.title("🎓 Student Performance Prediction System")
st.write(
    "Predict whether a student will Pass or Fail "
    "using Machine Learning."
)

if not BUNDLE_PATH.exists():
    st.error(
        "Model bundle not found. Please run train_model.py "
        "first to generate the model_files folder."
    )
    st.stop()

try:
    bundle = load_bundle()
    model = bundle["model"]
    scaler = bundle["scaler"]
    feature_names = bundle["feature_names"]
    feature_encoders = bundle["feature_encoders"]
    target_encoder = bundle["target_encoder"]
except Exception as e:
    st.error(f"Unable to load model files: {e}")
    st.stop()

st.caption(
    f"Model: {bundle['model_name']} | "
    f"Test accuracy: {bundle['accuracy'] * 100:.2f}%"
)

st.markdown("---")

# ==========================================
# Sidebar: Student Information
# ==========================================

st.sidebar.title("📝 Student Details")

with st.sidebar.form("student_prediction_form"):

    # Use the exact categories learned during training.
    gender_encoder = feature_encoders["Gender"]
    department_encoder = feature_encoders["Department"]
    internet_encoder = feature_encoders["Internet_Access"]
    extra_encoder = feature_encoders["Extra_Classes"]
    income_encoder = feature_encoders["Family_Income"]

    gender = st.selectbox(
        "Gender",
        options=gender_encoder.classes_.tolist()
    )

    age = st.slider(
        "Age",
        min_value=15,
        max_value=30,
        value=20
    )

    department = st.selectbox(
        "Department",
        options=department_encoder.classes_.tolist()
    )

    study_hours = st.slider(
        "Study Hours per Day",
        min_value=0,
        max_value=10,
        value=5
    )

    attendance = st.slider(
        "Attendance (%)",
        min_value=0,
        max_value=100,
        value=80
    )

    assignment = st.slider(
        "Assignment Score",
        min_value=0,
        max_value=100,
        value=70
    )

    quiz = st.slider(
        "Quiz Score",
        min_value=0,
        max_value=100,
        value=70
    )

    midterm = st.slider(
        "Midterm Marks",
        min_value=0,
        max_value=100,
        value=70
    )

    previous = st.slider(
        "Previous Marks",
        min_value=0,
        max_value=100,
        value=70
    )

    internet = st.selectbox(
        "Internet Access",
        options=internet_encoder.classes_.tolist()
    )

    extra_classes = st.selectbox(
        "Extra Classes",
        options=extra_encoder.classes_.tolist()
    )

    sleep = st.slider(
        "Sleep Hours",
        min_value=4,
        max_value=12,
        value=7
    )

    family_income = st.selectbox(
        "Family Income",
        options=income_encoder.classes_.tolist()
    )

    submitted = st.form_submit_button(
        "🔍 Predict Result",
        use_container_width=True
    )

# ==========================================
# Create Raw Student Data
# ==========================================

student_raw = pd.DataFrame([{
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
    "Extra_Classes": extra_classes,
    "Sleep_Hours": sleep,
    "Family_Income": family_income
}])

# ==========================================
# Prediction
# ==========================================

if submitted:
    try:
        # Verify exact feature names and ordering.
        missing_features = [
            col for col in feature_names
            if col not in student_raw.columns
        ]

        extra_features = [
            col for col in student_raw.columns
            if col not in feature_names
        ]

        if missing_features or extra_features:
            st.error(
                f"Feature mismatch. Missing: {missing_features}; "
                f"Unexpected: {extra_features}"
            )
            st.stop()

        # Match the training feature order.
        student = student_raw[feature_names].copy()

        # Apply the SAME fitted encoders used during training.
        for col, encoder in feature_encoders.items():
            student[col] = encoder.transform(
                student[col].astype(str)
            )

        # Apply the SAME fitted scaler.
        student_scaled = scaler.transform(student)

        # Predict encoded result.
        prediction = model.predict(student_scaled)

        # Decode the prediction into its original label.
        predicted_label = target_encoder.inverse_transform(
            prediction.astype(int)
        )[0]

        # Find probabilities using the model's actual class order.
        probabilities = model.predict_proba(student_scaled)[0]

        probability_by_label = {}

        for class_value, probability in zip(
            model.classes_, probabilities
        ):
            label = target_encoder.inverse_transform(
                [int(class_value)]
            )[0]

            probability_by_label[label] = probability * 100

        # Display prediction.
        st.markdown("---")
        st.subheader("📊 Prediction Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Predicted Result", predicted_label)

        with col2:
            st.metric(
                "Pass Probability",
                f"{probability_by_label.get('Pass', 0):.2f}%"
            )

        with col3:
            st.metric(
                "Fail Probability",
                f"{probability_by_label.get('Fail', 0):.2f}%"
            )

        if predicted_label == "Pass":
            st.success("The model predicts that the student will PASS.")
        else:
            st.error("The model predicts that the student may FAIL.")

        st.caption(
            "Probabilities are model estimates, not guarantees "
            "of the student's actual result."
        )

        # Display student information.
        st.subheader("👨‍🎓 Student Details")
        st.dataframe(
            student_raw,
            use_container_width=True,
            hide_index=True
        )

        # Download entered student details.
        csv_data = student_raw.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Student Details (CSV)",
            data=csv_data,
            file_name="student_prediction_details.csv",
            mime="text/csv"
        )

    except ValueError as e:
        st.error(
            f"Input encoding or feature error: {e}. "
            "Check your dataset categories and retrain the model "
            "if the training files are inconsistent."
        )

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# ==========================================
# Input Summary Dashboard
# ==========================================

st.markdown("---")
st.subheader("📈 Input Summary Dashboard")

numeric_summary = student_raw.select_dtypes(
    include="number"
).T

numeric_summary.columns = ["Value"]

st.bar_chart(numeric_summary)

with st.expander("View all input features"):
    st.dataframe(
        student_raw,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")
st.info(
    "Developed using Python, Pandas, Scikit-learn, "
    "Joblib and Streamlit."
)
