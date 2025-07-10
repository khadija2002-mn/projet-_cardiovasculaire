import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

# ===== 🎨 STYLING & BACKGROUND =====
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://anatomy.app/Media/videos/heartturntableml1080x1080_20240110114947_preview_medium.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .block-container {{
        background-color: rgba(255,255,255,0.9);
        padding: 2rem 4rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .stButton>button {{
        background-color: #0077b6;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
    }}
    .stButton>button:hover {{
        background-color: #023e8a;
        color: #fff;
    }}
    .main-title {{
        font-size: 40px;
        color: #023e8a;
        font-weight: bold;
    }}
    .sub-title {{
        font-size: 24px;
        color: #0077b6;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ===== 🩺 TITRE =====
st.markdown('<div class="main-title">🩺 Application Médicale : Analyse & Prédiction</div>', unsafe_allow_html=True)
st.markdown("---")

# ===== TABS =====
tab1, tab2 = st.tabs(["📊 Visualisation du Dataset", "🔍 Prédiction Patient"])

# ========================
# === 1. VISUALISATION ===
# ========================
with tab1:
    st.markdown('<div class="sub-title">📁 Charger votre dataset médical (CSV)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Uploader un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.success("✅ Fichier chargé avec succès.")
            
            # Aperçu
            st.markdown('<div class="sub-title">🧾 Aperçu des données</div>', unsafe_allow_html=True)
            st.dataframe(data.head())

            # Graphique
            st.markdown('<div class="sub-title">📈 Distribution d\'une variable</div>', unsafe_allow_html=True)
            numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                col_to_plot = st.selectbox("Choisir une variable :", numeric_cols)
                fig1, ax1 = plt.subplots()
                sns.histplot(data[col_to_plot], kde=True, ax=ax1)
                st.pyplot(fig1)

            # Corrélation
            st.markdown('<div class="sub-title">🔍 Matrice de corrélation</div>', unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.heatmap(data.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax2)
            st.pyplot(fig2)

        except Exception as e:
            st.error(f"Erreur : {e}")
    else:
        st.info("Veuillez uploader un fichier CSV pour visualiser les données.")

# ========================
# === 2. PREDICTION ======
# ========================
with tab2:
    st.markdown('<div class="sub-title">🧾 Remplir les données du patient</div>', unsafe_allow_html=True)

    with st.form("formulaire"):
        age = st.number_input("Âge", 0, 120, 55)
        gender = st.selectbox("Genre", ["Homme", "Femme"])
        heart_rate = st.number_input("Fréquence cardiaque (bpm)", 30, 200, 75)
        systolic = st.number_input("Tension systolique", 50, 250, 120)
        diastolic = st.number_input("Tension diastolique", 30, 150, 80)
        blood_sugar = st.number_input("Taux de sucre (mg/dL)", 50, 500, 110)
        ckmb = st.number_input("CK-MB (U/L)", 0.0, 100.0, 18.0)
        troponin = st.number_input("Troponine (ng/mL)", 0.0, 100.0, 0.4)

        submitted = st.form_submit_button("🔍 Lancer la prédiction")

    if submitted:
        # Simulation de prédiction (à remplacer par modèle réel)
        prediction = random.choice(["Positif", "Négatif"])
        confidence = random.randint(70, 99)

        st.markdown('<div class="sub-title">🧪 Résultat</div>', unsafe_allow_html=True)
        if prediction == "Positif":
            st.error(f"🚨 Résultat : **{prediction}**")
        else:
            st.success(f"✅ Résultat : **{prediction}**")

        st.markdown(f"🎯 Score de confiance : **{confidence}%**")
        st.progress(confidence / 100)

        if prediction == "Positif" and confidence < 90:
            st.warning("⚠️ Ce résultat nécessite une validation médicale.")

        st.markdown('<div class="sub-title">🩺 Actions médicales possibles</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Valider le diagnostic"):
                st.success("✅ Diagnostic validé")
            if st.button("📅 Programmer un suivi"):
                st.info("📅 Suivi médical programmé")

        with col2:
            if st.button("🧪 Ajouter examens complémentaires"):
                st.info("🧪 Examen complémentaire recommandé")
            if st.button("❌ Marquer comme faux positif"):
                st.warning("🔁 Signalé pour vérification")
