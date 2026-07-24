from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd 
import re

def ajouter_coordonnees_profil(profil):
    geolocator = Nominatim(user_agent="jobfit-ai")
    location = geolocator.geocode(f'{profil["commune"]}, France')
    
    if location:
        profil["lat"] = location.latitude
        profil["lon"] = location.longitude
    else:
        profil["lat"] = None
        profil["lon"] = None

    return profil
def calculate_distance(lat_user, lon_user, lat_offre, lon_offre):

    if pd.isna(lat_user) or pd.isna(lon_user):
        return None

    if pd.isna(lat_offre) or pd.isna(lon_offre):
        return None

    return round(
        geodesic(
            (lat_user, lon_user),
            (lat_offre, lon_offre)
        ).km,
        1
    )

def filtrer_offres_par_distance( lat_user, lon_user, lat_offre, lon_offre, lieu_libelle, distance_max_km):
   if pd.isna(lieu_libelle):
      lieu_libelle = ""
   lieu_libelle = str(lieu_libelle).lower()
   if "remote" in lieu_libelle or "télétravail" in lieu_libelle:
       return True
   if pd.isna(lat_user) or pd.isna(lon_user) :
       return False
   if pd.isna(lon_offre) or pd.isna(lat_offre):
       return False
   lat_offre = float(lat_offre)
   lon_offre = float(lon_offre)
                      
   distance = geodesic((lat_user, lon_user),(lat_offre, lon_offre)).km

   return distance <= distance_max_km
   


def filtrer_offres_par_contrat(contrat_user, contrat_offre):
    if pd.isna(contrat_offre):
        return True

    contrat_user = str(contrat_user).upper()
    contrat_offre = str(contrat_offre).upper()

    return contrat_user == contrat_offre
   
def calculate_langue_score( langue_user, langue_offre):
   if not isinstance(langue_offre, list):
      return 100
   else:
      libelles_user = [l.upper() for l in langue_user]
      libelles_offre = [l.get("libelle", "").upper() for l in langue_offre
                        if isinstance(l, dict) and l.get("libelle")]
      langues_demandees = set(libelles_offre)
      langues_utilisateur = set(libelles_user)

   if not langues_demandees:
        return 100

   langues_communes = langues_demandees.intersection(langues_utilisateur)

   return round(len(langues_communes) / len(langues_demandees) * 100)
   
def calculate_competence_score(competence_user, competence_offre):
   if not isinstance(competence_offre, list):
        return 100
   if not competence_offre:  # si la liste est vide ou None
    return 50
   libelles_user = [l.upper() for l in competence_user]
   libelles_offre = [l.get("libelle", "").upper() for l in competence_offre if l.get("libelle")]
   competences_demandes= set(libelles_offre)
   competences_utilisateur = set(libelles_user)

   if not competences_demandes:
      return 100
   competences_communs = competences_demandes.intersection(competences_utilisateur)
   
   return round(len(competences_communs) / len(competences_demandes)*100) 
      
def calculate_experience_score(experience_user, experience_offre):
   if pd.isna(experience_offre):
      return 100
   experience_offre= experience_offre.lower()
   if "débutant" in experience_offre or "debutant" in experience_offre:
      return 100
   numbers= re.findall(r"\d+", experience_offre)
   if not numbers:
      return 70
   experience_demandee= int(numbers[0])
   if experience_user >= experience_demandee:
        return 100

   elif experience_user >= experience_demandee - 1:
        return 70

   else:
        return 30

def calculate_global_score(profil, offre):
    score_competence= calculate_competence_score(profil["competences"], offre["competences"]) 
    score_experience= calculate_experience_score(profil["experience"], offre["experienceLibelle"])
    score_langue= calculate_langue_score(profil["langues"], offre["langues"])
    score_global = (0.70 * score_competence+ 0.2 * score_experience+ 0.1 * score_langue )

    return round(score_global, 2)
