import streamlit as st
from datetime import date

# --- Données de prédiction (à remplacer par ta vraie logique) ---
risk = "Positif"  # "Positif" ou "Négatif"
confidence = 85
confidence_threshold = 90

# --- Fonction pour afficher le résultat ---
def show_result():
    st.title("Résultat de la prédiction")

    # Couleur selon risque
    color = "#c53030" if risk == "Positif" else "#2f855a"
    st.markdown(f"<h2 style='color:{color};'>Risque de crise cardiaque : {risk}</h2>", unsafe_allow_html=True)

    # Barre de confiance
    st.write(f"Confiance du modèle : {confidence}%")
    st.progress(confidence / 100)

    # Alerte si besoin
    if risk == "Positif" and confidence < confidence_threshold:
        st.warning("⚠️ Attention : ce résultat nécessite une validation supplémentaire avant décision clinique.")

# --- Popup En savoir plus ---
def show_more_info():
    st.info("""
    **Qu’est-ce qu’un faux positif ?**

    Un faux positif est un résultat indiquant un risque élevé alors qu'en réalité le patient n’a pas eu de crise cardiaque.

    Cela peut arriver pour plusieurs raisons : limites du modèle, données insuffisantes ou atypiques, variations biologiques.

    En cas de doute, il est recommandé de demander des examens complémentaires avant toute décision médicale.

    Consultez les protocoles internes et guides cliniques pour plus d’informations.
    """)

# --- Formulaire examens complémentaires ---
def examens_complementaires():
    st.subheader("Demande d'examens complémentaires")
    ecg = st.checkbox("ECG")
    prise_sang = st.checkbox("Prise de sang")
    scanner = st.checkbox("Scanner")
    autre = st.text_input("Autre examen (précisez)")
    if st.button("Envoyer la demande"):
        examens = []
        if ecg: examens.append("ECG")
        if prise_sang: examens.append("Prise de sang")
        if scanner: examens.append("Scanner")
        if autre.strip() != "": examens.append(autre.strip())
        if examens:
            st.success(f"Demande envoyée pour les examens : {', '.join(examens)}")
        else:
            st.error("Veuillez sélectionner au moins un examen.")

# --- Formulaire suivi rapproché ---
def suivi_rapproche():
    st.subheader("Programmer un suivi rapproché")
    rdv_date = st.date_input("Date du suivi", min_value=date.today())
    if st.button("Programmer"):
        st.success(f"Suivi rapproché programmé pour le {rdv_date.strftime('%d/%m/%Y')}.")

# --- Formulaire notification patient ---
def notifier_patient():
    st.subheader("Envoyer notification au patient")
    message = st.text_area("Message personnalisé", "Bonjour, suite à votre examen, veuillez suivre les recommandations de votre médecin.")
    if st.button("Envoyer"):
        st.success("Notification envoyée au patient.")
        st.write(f"Message envoyé : {message}")

# --- Historique patient ---
def afficher_historique():
    st.subheader("Historique du patient")
    historique = """
    - 01/07/2025 : Prédiction négative  
    - 15/06/2025 : Prédiction positive (confiance 90%)  
    - 01/06/2025 : ECG normal  
    - 20/05/2025 : Consultation cardiologue  
    """
    st.markdown(historique)

# --- Main interface ---
def main():
    st.set_page_config(page_title="Prédiction Crise Cardiaque", page_icon="❤️", layout="centered")

    show_result()

    # Bouton en savoir plus
    if st.button("En savoir plus"):
        show_more_info()

    st.markdown("---")
    st.subheader("Actions recommandées")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Valider le diagnostic"):
            st.success("Diagnostic validé par le médecin.")
        if st.button("Marquer comme faux positif"):
            st.error("Cas marqué comme faux positif pour rétroaction.")

    with col2:
        if st.button("Demander examens complémentaires"):
            examens_complementaires()
        if st.button("Programmer un suivi rapproché"):
            suivi_rapproche()
        if st.button("Envoyer notification au patient"):
            notifier_patient()

    st.markdown("---")
    afficher_historique()

if __name__ == "__main__":
    main()
