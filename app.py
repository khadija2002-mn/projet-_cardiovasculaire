import streamlit as st
import numpy as np
import tensorflow as tf

# تحميل الموديل
model = tf.keras.models.load_model("mlp_model_heart_attack.keras")

# إعدادات الصفحة
st.set_page_config(page_title="Heart Attack Risk Predictor", layout="wide")

# 🔧 تعيين خلفية عبر رابط صورة
def set_background_url(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://img.freepik.com/free-photo/view-graphic-3d-heart_23-2150849187.jpg?semt=ais_hybrid&w=740");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🌄 خلفية عامة للموقع
set_background_url("https://images.unsplash.com/photo-1588776814546-bb4f3a601b86")  # خلفية طبية مثلاً

# 🔶 العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: white;'>💓 Heart Attack Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #f0f0f0;'>Enter patient data below to assess risk</h4>", unsafe_allow_html=True)

# 📋 فورم الإدخال
with st.form(key="predict_form"):
    st.subheader("🔢 Patient Data")
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 20, 100, 50)
        cholesterol = st.number_input("Cholesterol Level", value=200)
        trtbps = st.number_input("Resting Blood Pressure", value=130)

    with col2:
        thalachh = st.number_input("Max Heart Rate Achieved", value=150)
        oldpeak = st.number_input("Oldpeak (ST depression)", value=1.0, format="%.1f")
        cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
    
    submit = st.form_submit_button("🧠 Predict Risk")

# ⚙️ الحساب والتوقع
if submit:
    input_data = np.array([[age, trtbps, cholesterol, thalachh, oldpeak, cp]])
    prediction = model.predict(input_data)
    risk_score = prediction[0][0]

    st.markdown("---")
    st.markdown(
        f"<h2 style='color: #00ffcc;'>🩺 Predicted Heart Attack Risk: <strong>{risk_score:.2f}</strong></h2>",
        unsafe_allow_html=True
    )

    if risk_score > 0.5:
        st.error("⚠️ High Risk — Please consult a doctor.")
    else:
        st.success("✅ Low Risk — Keep up the healthy lifestyle!")

# 🔻 التذييل
st.markdown("---")
st.markdown("<p style='text-align: center; color: white;'>© 2025 HeartCare AI | All rights reserved.</p>", unsafe_allow_html=True)
