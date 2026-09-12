import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="CardioPredict | Heart Disease Risk",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e3a5f);
        padding: 35px 40px;
        border-radius: 18px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }

    .main-header h1 {
        font-size: 42px;
        margin-bottom: 5px;
        font-weight: 700;
    }

    .main-header p {
        font-size: 17px;
        color: #dbeafe;
        margin-bottom: 0;
    }

    /* Section cards */
    .section-card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }

    .section-title {
        font-size: 21px;
        font-weight: 650;
        color: #1e293b;
        margin-bottom: 15px;
    }

    /* Prediction result */
    .result-low {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-top: 25px;
    }

    .result-high {
        background: #fef2f2;
        border: 1px solid #fecaca;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin-top: 25px;
    }

    .result-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .result-text {
        font-size: 16px;
        color: #475569;
    }

    /* Info box */
    .info-box {
        background: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 15px 18px;
        border-radius: 8px;
        margin-top: 15px;
        color: #1e3a8a;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding: 30px 0 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    model = joblib.load("knn_heart_model.pkl")
    scaler = joblib.load("heart_scaler.pkl")
    expected_columns = joblib.load("heart_columns.pkl")

    return model, scaler, expected_columns


try:
    model, scaler, expected_columns = load_model()

except Exception as e:
    st.error("Unable to load the prediction model.")
    st.info(
        "Make sure knn_heart_model.pkl, heart_scaler.pkl and "
        "heart_columns.pkl are present in the application folder."
    )
    st.stop()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="main-header">

    <h1>❤️ CardioPredict</h1>

    <p>
        Machine Learning powered Heart Disease Risk Assessment
    </p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown("## ❤️ CardioPredict")

    st.markdown("""
    **About the application**

    This application uses a trained **K-Nearest Neighbors (KNN)**
    machine learning model to estimate heart disease risk based
    on the information provided by the user.
    """)

    st.divider()

    st.markdown("### 🧠 Model")

    st.write("**Algorithm:** K-Nearest Neighbors (KNN)")
    st.write("**Preprocessing:** Feature Scaling")
    st.write("**Framework:** Streamlit")
    st.write("**Language:** Python")

    st.divider()

    st.caption(
        "⚠️ This application is for educational and demonstration "
        "purposes only. It is not a medical diagnostic tool."
    )


# --------------------------------------------------
# INTRODUCTION
# --------------------------------------------------
st.markdown("""
<div class="info-box">

<b>How it works:</b>
Enter the patient's basic clinical information below.
The trained machine learning model will process the data
and provide an estimated heart disease risk category.

</div>
""", unsafe_allow_html=True)

st.write("")


# --------------------------------------------------
# PATIENT INFORMATION
# --------------------------------------------------
st.markdown("""
<div class="section-card">

<div class="section-title">
👤 Patient Information
</div>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider(
        "Age",
        min_value=18,
        max_value=100,
        value=40
    )

with col2:
    sex = st.selectbox(
        "Sex",
        ["M", "F"]
    )

with col3:
    fasting_bs = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dL",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )


# --------------------------------------------------
# HEART PARAMETERS
# --------------------------------------------------
st.markdown("""
<div class="section-card">

<div class="section-title">
🫀 Cardiovascular Parameters
</div>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    resting_bp = st.number_input(
        "Resting Blood Pressure (mm Hg)",
        min_value=80,
        max_value=200,
        value=120,
        step=1
    )

with col2:
    cholesterol = st.number_input(
        "Cholesterol (mg/dL)",
        min_value=100,
        max_value=600,
        value=200,
        step=1
    )

with col3:
    max_hr = st.slider(
        "Maximum Heart Rate",
        min_value=60,
        max_value=220,
        value=150
    )


# --------------------------------------------------
# ECG & EXERCISE INFORMATION
# --------------------------------------------------
st.markdown("""
<div class="section-card">

<div class="section-title">
📊 ECG & Exercise Information
</div>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    chest_pain = st.selectbox(
        "Chest Pain Type",
        ["ATA", "NAP", "TA", "ASY"],
        format_func=lambda x: {
            "ATA": "Atypical Angina",
            "NAP": "Non-Anginal Pain",
            "TA": "Typical Angina",
            "ASY": "Asymptomatic"
        }[x]
    )

    resting_ecg = st.selectbox(
        "Resting ECG",
        ["Normal", "ST", "LVH"],
        format_func=lambda x: {
            "Normal": "Normal",
            "ST": "ST-T Wave Abnormality",
            "LVH": "Left Ventricular Hypertrophy"
        }[x]
    )

with col2:

    exercise_angina = st.selectbox(
        "Exercise-Induced Angina",
        ["Y", "N"],
        format_func=lambda x: "Yes" if x == "Y" else "No"
    )

    st_slope = st.selectbox(
        "ST Slope",
        ["Up", "Flat", "Down"]
    )

    oldpeak = st.slider(
        "Oldpeak (ST Depression)",
        min_value=0.0,
        max_value=6.0,
        value=1.0,
        step=0.1
    )


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
st.write("")

predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])

with predict_col2:

    predict_button = st.button(
        "🔍  Assess Heart Disease Risk",
        use_container_width=True,
        type="primary"
    )


if predict_button:

    # --------------------------------------------------
    # CREATE RAW INPUT
    # --------------------------------------------------

    raw_input = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,

        "Sex_" + sex: 1,
        "ChestPainType_" + chest_pain: 1,
        "RestingECG_" + resting_ecg: 1,
        "ExerciseAngina_" + exercise_angina: 1,
        "ST_Slope_" + st_slope: 1
    }

    input_df = pd.DataFrame([raw_input])

    # --------------------------------------------------
    # MATCH TRAINING COLUMNS
    # --------------------------------------------------

    for col in expected_columns:

        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]

    # --------------------------------------------------
    # SCALE INPUT
    # --------------------------------------------------

    scaled_input = scaler.transform(input_df)

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    prediction = model.predict(scaled_input)[0]

    # Probability if supported by model
    probability = None

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(
            scaled_input
        )[0][1]


    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------

    st.divider()

    if prediction == 1:

        st.markdown("""
        <div class="result-high">

            <div class="result-title">
                ⚠️ Elevated Risk Detected
            </div>

            <div class="result-text">
                The machine learning model predicts a higher
                likelihood of heart disease based on the
                information provided.
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="result-low">

            <div class="result-title">
                ✅ Lower Risk Predicted
            </div>

            <div class="result-text">
                The machine learning model predicts a lower
                likelihood of heart disease based on the
                information provided.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # --------------------------------------------------
    # MODEL CONFIDENCE
    # --------------------------------------------------

    if probability is not None:

        st.write("")

        c1, c2, c3 = st.columns(3)

        with c2:

            st.metric(
                "Model Estimated Probability",
                f"{probability * 100:.1f}%"
            )

        st.caption(
            "This probability represents the model's output, "
            "not a clinical probability or diagnosis."
        )


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------
st.write("")

st.markdown("""
<div class="info-box">

<b>⚕️ Important:</b>
This application is an educational machine learning project.
It should not be used to diagnose, treat, or make medical decisions.
If you have health concerns, consult a qualified healthcare professional.

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">

CardioPredict • Machine Learning Project • Built with Python & Streamlit

</div>
""", unsafe_allow_html=True)