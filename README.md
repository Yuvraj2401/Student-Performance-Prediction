# 🎓 Student Performance Prediction System

A Machine Learning project built with Python and Streamlit to predict student academic outcomes based on academic performance and other relevant student-related factors.

## 📌 Project Overview

The Student Performance Prediction System uses machine learning classification algorithms to predict a student's final academic result. It includes data preprocessing, model training, model evaluation, and an interactive web interface built with Streamlit.

The project is designed to demonstrate how machine learning can support the analysis of student performance.

## 🎯 Project Objectives

- Analyze student academic performance data.
- Clean and preprocess the dataset for machine learning.
- Train and compare multiple classification algorithms.
- Predict student outcomes using input features.
- Provide an interactive interface through Streamlit.
- Practice model evaluation and Python application development.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Data Preprocessing:** Label Encoding, Standard Scaling
- **Model Persistence:** Joblib
- **Dataset:** Excel
- **Database:** MySQL, if enabled in the current application
- **Development Tools:** VS Code / Jupyter Notebook

## 🤖 Machine Learning Algorithms

The project compares the following classification algorithms:

1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
4. Support Vector Machine (SVM)

The best-performing model should be selected based on the evaluation results from the training script.

## ✨ Key Features

- Interactive Streamlit web interface
- Student information and academic-feature inputs
- Data preprocessing and feature scaling
- Multiple machine learning model comparison
- Student outcome prediction
- Model saving and loading
- Prediction results displayed in the application
- Optional reporting and dashboard functionality, depending on the enabled modules

## 📂 Project Structure

```text
Student_Performance_Prediction/
│
├── app.py
├── app1.py
├── train_model.py
├── prediction.py
├── predictions.py
├── dashboard.py
├── database.py
├── login.py
├── export_report.py
├── requirements.txt
├── README.md
├── style.css
├── assets/
├── model_files/
├── Student_Performance_1000_Records_With_Names.xlsx
└── prediction_report.xlsx
```

*Note: This is a representative structure based on the project files. Keep only the files that your current application uses. Generated model files should be stored in the location expected by your code.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Student-Performance-Prediction.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the project directory

```bash
cd Student-Performance-Prediction
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Prepare the dataset

Place the Excel dataset in the location expected by `train_model.py`. Ensure the dataset has the columns required by the training script.

### 6. Train the machine learning model

```bash
python train_model.py
```

Run this step if the model files have not already been generated or need to be regenerated.

### 7. Start the Streamlit application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## 📊 Input Features

The model may use the following features, depending on the final training dataset:

- Gender
- Age
- Department
- Study Hours
- Attendance
- Assignment Score
- Quiz Score
- Midterm Marks
- Previous Marks
- Internet Access
- Extra Classes
- Sleep Hours
- Family Income

The input features and their column names must match those used during model training.

## 📈 Model Evaluation

Model performance should be evaluated using suitable classification metrics, such as:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Add the actual evaluation results from your training script here once verified. Do not report an accuracy value unless it has been measured.

## 🗄️ Database Configuration

If the application uses MySQL, configure the database connection using your local database settings. Create the required database and tables before running database-dependent features.

**Security:** Do not commit database passwords, API keys, or other credentials to GitHub. Store them in environment variables or an appropriate secrets configuration.

## 🚀 Future Improvements

- Improve model performance through feature engineering and hyperparameter tuning.
- Add interactive data visualizations.
- Include detailed prediction reports.
- Add a student performance dashboard.
- Improve input validation and error handling.
- Deploy the application online.

## 🎓 Learning Outcomes

Through this project, I practiced:

- Data preprocessing and exploratory data analysis
- Classification algorithms using Scikit-learn
- Encoding categorical variables and scaling numerical features
- Model evaluation and comparison
- Building a machine learning application with Streamlit
- Organizing Python project files and using GitHub

## 👨‍💻 Author

**Yuvraj Pal**

Aspiring Data Analyst | Data Science & Machine Learning Enthusiast

## 📄 License

This project can be shared and reused under a suitable open-source license. Add a `LICENSE` file if you decide to publish it under a specific license.