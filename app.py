import streamlit as st
import random

st.set_page_config(page_title="Prédiction Crise Cardiaque", page_icon="🫀", layout="centered")

st.title("🫀 Prédiction du Risque de Crise Cardiaque")
st.markdown("**Veuillez remplir les données du patient pour lancer la prédiction.**")

# --- Formulaire données patient ---
with st.form("patient_form"):
    age = st.number_input("Âge", min_value=0, max_value=120, value=50)
    gender = st.selectbox("Genre", ["Homme", "Femme"])
    heart_rate = st.number_input("Fréquence cardiaque (bpm)", min_value=30, max_value=200, value=75)
    systolic_bp = st.number_input("Tension artérielle systolique (mmHg)", min_value=50, max_value=250, value=120)
    diastolic_bp = st.number_input("Tension diastolique (mmHg)", min_value=30, max_value=150, value=80)
    blood_sugar = st.number_input("Taux de sucre (mg/dL)", min_value=50, max_value=500, value=100)
    ckmb = st.number_input("CK-MB (U/L)", min_value=0.0, max_value=100.0, value=20.0)
    troponin = st.number_input("Troponine (ng/mL)", min_value=0.0, max_value=100.0, value=0.5)
    
    submit = st.form_submit_button("🔍 Prédire")

# --- Simuler une prédiction ---
if submit:
    # ⚠️ Remplace cette partie par ton vrai modèle plus tard
    prediction = random.choice(["Positif", "Négatif"])
    confidence = random.randint(70, 99)

    st.subheader("🧪 Résultat de la prédiction")
    if prediction == "Positif":
        st.error(f"Risque de crise cardiaque : **{prediction}**")
    else:
        st.success(f"Risque de crise cardiaque : **{prediction}**")
    
    st.write(f"**Confiance du modèle :** {confidence}%")
    st.progress(confidence / 100)

    if prediction == "Positif" and confidence < 90:
        st.warning("⚠️ Résultat à confirmer par examens complémentaires.")

    # Actions recommandées
    st.markdown("---")
    st.subheader("🩺 Actions du médecin")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Valider le diagnostic"):
            st.success("Diagnostic validé.")
        if st.button("🧪 Demander examens complémentaires"):
            st.info("Demande d'examens enregistrée.")

    with col2:
        if st.button("📅 Programmer un suivi"):
            st.success("Suivi médical programmé.")
        if st.button("❌ Marquer comme faux positif"):
            st.warning("Cas marqué pour vérification.")

    # Historique fictif
    st.markdown("---")
    st.subheader("📋 Historique médical du patient")
    st.write("""
    - 01/07/2025 : Prédiction négative  
    - 15/06/2025 : ECG anormal  
    - 20/05/2025 : Hospitalisation courte  
    """)

