import streamlit as st
import tensorflow as tf
import numpy as np
import tempfile
import os
from pathlib import Path

st.set_page_config(page_title="Heart Risk Predictor", layout="wide")
st.title("💓 Heart Attack Risk Predictor")

# 🆙 رفع النموذج من طرف المستخدم
uploaded_model = st.file_uploader("🔼 Upload your model (.keras, .h5, .pb)", type=["keras", "h5", "pb"])

model = None
loaded_model_type = None

if uploaded_model is not None:
    try:
        # حفظ الملف المؤقت
        suffix = Path(uploaded_model.name).suffix
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, uploaded_model.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_model.read())

            if suffix in [".keras", ".h5"]:
                model = tf.keras.models.load_model(file_path)
                loaded_model_type = "keras"

            elif suffix == ".pb":
                # `.pb` خاص تكون داخلة فـ structure ديال SavedModel
                # ننسخها إلى مجلد خاص
                model_dir = os.path.join(tmpdir, "saved_model")
                os.makedirs(model_dir, exist_ok=True)
                # نعمل نسخة فقط
                new_path = os.path.join(model_dir, "saved_model.pb")
                os.rename(file_path, new_path)
                # نحاول نحمّل الموديل
                model = tf.saved_model.load(model_dir)
                loaded_model_type = "savedmodel"

        st.success(f"✅ Model loaded successfully as type: {loaded_model_type}")

    except Exception as e:
        st.error(f"❌ Error loading model: {e}")

# ✅ إذا تم تحميل الموديل
if model is not None and loaded_model_type:
    with st.form("prediction_form"):
        st.subheader("🔢 Patient Data Input")
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("Age", 20, 100, 50)
            cholesterol = st.number_input("Cholesterol", value=200)
            trtbps = st.number_input("Resting Blood Pressure", value=130)

        with col2:
            thalachh = st.number_input("Max Heart Rate", value=150)
            oldpeak = st.number_input("Oldpeak (ST depression)", value=1.0)
            cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])

        submit = st.form_submit_button("🧠 Predict")

    if submit:
        input_data = np.array([[age, trtbps, cholesterol, thalachh, oldpeak, cp]], dtype=np.float32)

        try:
            if loaded_model_type == "keras":
                prediction = model.predict(input_data)
            elif loaded_model_type == "savedmodel":
                infer = model.signatures["serving_default"]
                tensor_input = tf.convert_to_tensor(input_data)
                prediction = infer(tensor_input)
                # نحاول ناخذ أول output (بعض saved_models عندهم keys)
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
