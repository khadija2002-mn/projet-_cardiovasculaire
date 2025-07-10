import streamlit as st
import tensorflow as tf
import numpy as np
import tempfile
import os
from pathlib import Path

# إعداد صفحة Streamlit
st.set_page_config(page_title="Heart Risk Predictor", layout="wide")
st.title("💓 Heart Attack Risk Predictor")

# رفع الموديل من طرف المستخدم
uploaded_model = st.file_uploader("🔼 Upload your model (.keras, .h5, .pb)", type=["keras", "h5", "pb"])

model = None
loaded_model_type = None

# تحميل الموديل
if uploaded_model is not None:
    try:
        suffix = Path(uploaded_model.name).suffix
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, uploaded_model.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_model.read())

            if suffix in [".keras", ".h5"]:
                model = tf.keras.models.load_model(file_path)
                loaded_model_type = "keras"

            elif suffix == ".pb":
                model_dir = os.path.join(tmpdir, "saved_model")
                os.makedirs(model_dir, exist_ok=True)
                new_path = os.path.join(model_dir, "saved_model.pb")
                os.rename(file_path, new_path)
                model = tf.saved_model.load(model_dir)
                loaded_model_type = "savedmodel"

        st.success(f"✅ Model loaded successfully as type: {loaded_model_type}")

    except Exception as e:
        st.error(f"❌ Error loading model: {e}")

# إذا تم تحميل الموديل
if model is not None and loaded_model_type:
    with st.form("prediction_form"):
        st.subheader("🔢 Patient Data Input")
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("Age", 20, 100, 50)
            sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
            cp = st.selectbox("Chest Pain Type (cp)", [0, 1, 2, 3])
            trtbps = st.number_input("Resting Blood Pressure (trtbps)", value=130)

        with col2:
            cholesterol = st.number_input("Cholesterol", value=200)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", [0, 1])
            thalachh = st.number_input("Max Heart Rate (thalachh)", value=150)
            oldpeak = st.number_input("Oldpeak (ST depression)", value=1.0)

        submit = st.form_submit_button("🧠 Predict")

    if submit:
        # إدخال البيانات بالترتيب الصحيح (8 خصائص)
        input_data = np.array([[age, sex, cp, trtbps, cholesterol, fbs, thalachh, oldpeak]], dtype=np.float32)

        try:
            if loaded_model_type == "keras":
                prediction = model.predict(input_data)
            elif loaded_model_type == "savedmodel":
                infer = model.signatures["serving_default"]
                tensor_input = tf.convert_to_tensor(input_data)
                prediction = infer(tensor_input)
                prediction = list(prediction.values())[0].numpy()

            risk_score = prediction[0][0]
            st.markdown(f"### 🩺 Predicted Risk: **{risk_score:.2f}**")

            if risk_score > 0.5:
                st.error("⚠️ High Risk — Please consult a doctor.")
            else:
                st.success("✅ Low Risk — Great job!")

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")

else:
    st.info("📂 Please upload a model file to get started.")
