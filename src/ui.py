import streamlit as st
def uploader_cv():

    uploaded_cv = st.file_uploader(
        "📄 Déposez votre CV",
        type=["pdf"]
    )

    if uploaded_cv is not None:
        st.success("CV importé avec succès")
        st.write(f"📄 {uploaded_cv.name}")

    return uploaded_cv

def afficher_offre(offre):
   with st.container():
    st.subheader(offre["intitule"])
    col1, col2 = st.columns([3,1])

    with col1:
        
        st.write(offre["entreprise.nom"])
        st.write(f"📍 {offre['lieuTravail.libelle']}")
        st.write(f"🚗 {offre['distance_km']} km de chez vous")

    with col2:
        st.metric( "Score", f"{offre['score']}%")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    with col_btn1:    
            st.link_button("🔗 Voir l'offre",f"https://candidat.francetravail.fr/offres/recherche/detail/{offre['id']}")
    with col_btn2:
    
            analyser = st.button("🧠 Analyser", key=f"analyse_{offre['id']}")

    with col_btn3:
            generer_cv = st.button( "📄 Générer CV ATS", key=f"cv_ats_{offre['id']}")
    with col_btn4:
              generer_lm = st.button( "✉️ Lettre", key=f"lm_{offre['id']}")
    
    return analyser, generer_cv, generer_lm

    

       
