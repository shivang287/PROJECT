# ❤️ CardioPredict — Heart Disease Risk Prediction

An end-to-end machine learning project that analyzes patient health information and predicts the likelihood of heart disease using a trained **K-Nearest Neighbors (KNN)** classification model.

The project includes exploratory data analysis (EDA), data cleaning, categorical encoding, feature scaling, comparison of multiple machine learning algorithms, model evaluation, model serialization, and a Streamlit web application.

> ⚕️ **Disclaimer:** This project is intended for educational and demonstration purposes only. It is not a medical diagnostic system and should not be used for clinical decision-making.

---

## 🚀 Project Highlights

- Exploratory Data Analysis on a heart disease dataset
- Data cleaning and handling of zero values in `RestingBP` and `Cholesterol`
- One-hot encoding of categorical features
- Feature scaling using `StandardScaler`
- Comparison of 5 classification algorithms
- KNN selected as the best-performing model based on test accuracy and F1 score
- Model, scaler, and feature columns saved using Joblib
- Interactive prediction interface built with Streamlit

---

## 📊 Dataset

The dataset contains **918 records and 12 columns**.

### Features

| Feature | Description |
|---|---|
| `Age` | Age of the patient |
| `Sex` | Sex of the patient |
| `ChestPainType` | Type of chest pain |
| `RestingBP` | Resting blood pressure |
| `Cholesterol` | Cholesterol level |
| `FastingBS` | Fasting blood sugar indicator |
| `RestingECG` | Resting ECG result |
| `MaxHR` | Maximum heart rate |
| `ExerciseAngina` | Exercise-induced angina |
| `Oldpeak` | ST depression |
| `ST_Slope` | Slope of the ST segment |
| `HeartDisease` | Target variable |

The dataset contained **no null values and no duplicate rows**.

---

## 🔎 Exploratory Data Analysis

The notebook performs several EDA steps, including:

- Dataset shape and information
- Statistical summary
- Missing-value analysis
- Duplicate-value analysis
- Target distribution
- Categorical feature analysis
- Numerical feature distributions
- Box plots
- Violin plots
- Correlation heatmap

Examples of analyzed relationships include:

- Chest pain type vs. heart disease
- Fasting blood sugar vs. heart disease
- Cholesterol vs. heart disease
- Age vs. heart disease
- Numerical feature correlations

---

## 🧹 Data Preprocessing

### 1. Handling zero values

Zero values in `Cholesterol` and `RestingBP` were treated as missing/invalid measurements and replaced using the mean of the non-zero values.

### 2. Categorical Encoding

Categorical variables were converted into numerical features using:

```python
pd.get_dummies(df, drop_first=True)
```

### 3. Train/Test Split

The data was split into training and testing sets using an **80/20 split** with stratification.

```python
train_test_split(
    X,
    y,
    stratify=y,
    test_size=0.2,
    random_state=42
)
```

### 4. Feature Scaling

Because algorithms such as KNN and SVM are sensitive to feature magnitude, `StandardScaler` was used.

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

## 🤖 Machine Learning Models

Five classification algorithms were trained and evaluated:

1. Logistic Regression
2. K-Nearest Neighbors (KNN)
3. Gaussian Naive Bayes
4. Decision Tree
5. Support Vector Machine (SVM with RBF kernel)

---

## 📈 Model Comparison

The models were evaluated using **Accuracy** and **F1 Score** on the test set.

| Model | Accuracy | F1 Score |
|---|---:|---:|
| Logistic Regression | 87.50% | 88.78% |
| **KNN** | **88.59%** | **89.86%** |
| Naive Bayes | 86.96% | 87.88% |
| Decision Tree | 74.46% | 75.13% |
| SVM (RBF Kernel) | 86.41% | 88.04% |

### 🏆 Best Model

**K-Nearest Neighbors (KNN)** achieved the highest performance among the tested models:

- **Accuracy:** 88.59%
- **F1 Score:** 89.86%

Therefore, the KNN model was selected for deployment in the Streamlit application.

---

## 🧠 ML Workflow

```text
                    Heart Disease Dataset
                             │
                             ▼
                     Exploratory Analysis
                             │
                             ▼
                    Data Cleaning
                (Zero-value treatment)
                             │
                             ▼
                    Categorical Encoding
                             │
                             ▼
                     Train/Test Split
                          80 / 20
                             │
                             ▼
                      Feature Scaling
                     StandardScaler
                             │
                             ▼
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         Logistic          KNN          Naive Bayes
         Regression
              │              │              │
              └──────────────┼──────────────┘
                             │
                    Decision Tree + SVM
                             │
                             ▼
                    Model Comparison
                             │
                             ▼
                    🏆 Best Model: KNN
                             │
                             ▼
                    Joblib Serialization
                             │
                             ▼
                    Streamlit Web App
```

---

## 🖥️ Streamlit Application

The project includes an interactive web application where users can enter patient information and receive a model prediction.

### Input Parameters

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak
- ST Slope

The application:

```text
User Input
    ↓
Feature Formatting
    ↓
Match Training Columns
    ↓
StandardScaler
    ↓
Trained KNN Model
    ↓
Prediction
```

### Application Screenshot

Add your Streamlit screenshot here:

```markdown
![Streamlit Application](screenshots/streamlit_app.png)
```

---

## 📊 Model Evaluation

### Model Comparison

If you save the model-comparison graph from the notebook, place it inside:

```text
screenshots/model_comparison.png
```

Then add:

```markdown
![Model Comparison](screenshots/model_comparison.png)
```

### Confusion Matrix

If you have a confusion-matrix image, place it inside:

```text
screenshots/confusion_matrix.png
```

Then add:

```markdown
![Confusion Matrix](screenshots/confusion_matrix.png)
```

---

## 📁 Project Structure

```text
CardioPredict/
│
├── app.py
├── HeartdiseaseFinal.ipynb
│
├── knn_heart_model.pkl
├── heart_scaler.pkl
├── heart_columns.pkl
│
├── requirements.txt
├── README.md
│
└── screenshots/
    ├── streamlit_app.png
    ├── model_comparison.png
    └── confusion_matrix.png
```

### File Description

| File | Purpose |
|---|---|
| `app.py` | Streamlit web application |
| `HeartdiseaseFinal.ipynb` | EDA, preprocessing, model training and evaluation |
| `knn_heart_model.pkl` | Saved trained KNN model |
| `heart_scaler.pkl` | Saved feature scaler |
| `heart_columns.pkl` | Saved feature/column order |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |

---

## ⚙️ Installation & Usage

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CardioPredict
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your default web browser.

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Matplotlib**
- **Seaborn**
- **Streamlit**
- **Joblib**
- **Jupyter Notebook**

---

## 📚 Key Concepts Demonstrated

This project demonstrates practical understanding of:

- Exploratory Data Analysis
- Data preprocessing
- One-hot encoding
- Feature scaling
- Train/test splitting
- Classification algorithms
- KNN
- Model comparison
- Accuracy and F1-score
- Model serialization
- Streamlit deployment
- Real-time ML prediction

---

## 🔮 Future Improvements

- Add cross-validation for more robust model evaluation
- Perform hyperparameter tuning for KNN
- Add ROC-AUC and ROC curve analysis
- Add an interactive model-performance dashboard
- Deploy the Streamlit application online
- Add automated input validation
- Experiment with additional classification algorithms
- Improve explainability using feature importance/SHAP where appropriate

---

## 👨‍💻 Author

**Akarsh**

Machine Learning / Python Project

---

## ⚕️ Medical Disclaimer

This application is an academic machine learning project. Predictions are generated by a statistical model and do not constitute medical advice, diagnosis, or treatment recommendations. Always consult a qualified healthcare professional for medical concerns.
