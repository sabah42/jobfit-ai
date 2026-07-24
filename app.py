
from src import api
from src import matching
from src import cv_parser
from src import ui
from src import llm

import streamlit as st
import pandas as pd
# =========================
# Récupération des offres
# =========================
st.set_page_config( page_title="JobFit AI", page_icon="🎯",layout="wide")
st.title("🎯 JobFit AI")
st.caption( "Assistant IA de matching CV ↔ offres d'emploi")
token = api.get_token()
df = api.get_offre(token)

# =========================
# Colonnes utiles
# =========================

colonnes_utiles = [
    "id",
    "intitule",
    "description",
    "dateCreation",
    "dateActualisation",
    "romeCode",
    "romeLibelle",
    "typeContratLibelle",
    "experienceLibelle",
    "lieuTravail.libelle",
    "lieuTravail.commune",
    "lieuTravail.codePostal",
    "lieuTravail.latitude",
    "lieuTravail.longitude",
    "salaire.libelle",
    "salaire.commentaire",
    "entreprise.nom",
    "secteurActiviteLibelle",
    "langues",
    "competences"
]

df = df[colonnes_utiles].copy()


# =========================
# Profil utilisateur
# =========================
col_profil, col_offres = st.columns([1.3, 4])
with st.sidebar:
    uploader_cv= ui.uploader_cv()
    type_contrat= st.selectbox("contrat souhaité",["CDI", "CDD", "Alternance"])
    distance_max_km= st.slider( "Distance maximale (km)",0,400,50)
    if uploader_cv is not None:

     cv_text_original = cv_parser.extract_text_from_pdf(uploader_cv)
     cv_text= cv_parser.normaliser(cv_text_original)
     
     profil = {"titre": cv_parser.extract_titre(cv_text),"commune": cv_parser.extract_commune(cv_text), "distance_max_km": distance_max_km,"type_contrat":type_contrat,   "competences": cv_parser.extract_competences(cv_text), "langues": cv_parser.extract_langues(cv_text), "experience": cv_parser.extract_experience(cv_text)}
     with col_profil:
      st.subheader("👤 Profil détecté")
      st.write(f"🎯 Métier : {profil['titre'][0]}")
      st.write(f"📍 Ville : {profil['commune']}")
      st.write(f"💼 Contrat : {profil['type_contrat']}")
      st.write(f"🚗 Distance max : {profil['distance_max_km']} km")
      st.write(f"📅 Expérience : {profil['experience']} ans")
      with st.expander("Voir le profil complet"):
        st.json(profil)
    # ====================================================================================================================================

# =====================================================
# Ajout coordonnées utilisateur
# =========================

     profil = matching.ajouter_coordonnees_profil(profil)

     diagnostic = llm.diagnostiquer_cv(cv_text_original )
     st.subheader("🧠 Diagnostic IA")

     st.write(diagnostic)

# Filtre distance

     df = df[df.apply( lambda offre: matching.filtrer_offres_par_distance(
            profil["lat"],
            profil["lon"],
            offre["lieuTravail.latitude"],
            offre["lieuTravail.longitude"],
            offre["lieuTravail.libelle"],
            profil["distance_max_km"] ),axis=1)]
     df["distance_km"] = df.apply(lambda row: matching.calculate_distance(
        profil["lat"],
        profil["lon"],
        row["lieuTravail.latitude"],
        row["lieuTravail.longitude"]),axis=1)
     df["score_competence"] = df.apply( lambda offre: matching.calculate_competence_score(profil["competences"], offre["competences"]),axis=1)

     df["score_experience"] = df.apply(
     lambda offre: matching.calculate_experience_score(profil["experience"], offre["experienceLibelle"]),axis=1)

     df["score_langue"] = df.apply(
     lambda offre: matching.calculate_langue_score(profil["langues"], offre["langues"]), axis=1)
# Filtre contrat

     df = df[df.apply(lambda offre: matching.filtrer_offres_par_contrat(
            profil["type_contrat"],
            offre["typeContratLibelle"]), axis=1)]
     if df.empty:
        print('Aucune offre trouvée avec ces filtres.')
        print(" Essaie d'augmenter la distance ou de retirer temporairement le filtre contrat ")
     else:
       df["score"] = df.apply(lambda offre: matching.calculate_global_score(profil, offre), axis=1)
       df_sorted = df.sort_values("score", ascending=False)
       print(df_sorted[[ "intitule", "entreprise.nom", "typeContratLibelle","competences","lieuTravail.libelle","distance_km","score_competence","score_experience","score_langue","score"]].head(10))
       print(f"Offres après filtre distance : {len(df)}")

       with col_offres:
           st.subheader("🎯 Offres recommandées")
           for _, offre in df_sorted.iterrows():
               analyser, generer_cv, generer_lm = ui.afficher_offre(offre)
               
               if analyser:

                  analyse = llm.analyser_compatibilite( cv_text,offre)

                  st.write(analyse)
               
               if generer_cv:

                 cv_optimise = llm.generer_cv_optimise(cv_text,offre)

                 with st.expander("👀 Voir le CV optimisé"):
                   st.markdown(cv_optimise)

                 st.download_button("📥 Télécharger le CV optimisé",cv_optimise, file_name="cv_optimise_ats.txt", mime="text/plain", key=f"download_cv_{offre['id']}")
                 
               if generer_lm:

                  with st.spinner("Génération de la lettre de motivation..."):

                   lettre = llm.generer_lettre_motivation( cv_text, offre)

                  with st.expander("✉️ Voir la lettre"):
                    st.markdown(lettre)

                  st.download_button("📥 Télécharger la lettre", lettre, file_name="lettre_motivation.txt", mime="text/plain", key=f"download_lm_{offre['id']}")
               st.divider()