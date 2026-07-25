import requests
import os 
import pandas as pd 
from dotenv import load_dotenv 
load_dotenv()
def lire_secret(nom):
    valeur = os.getenv(nom)

    if not valeur:
        try:
            valeur = st.secrets[nom]
        except KeyError:
            valeur = None

    if not valeur:
        raise ValueError(f"Le secret {nom} est absent.")

    return str(valeur).strip()


CLIENT_ID = lire_secret("CLIENT_ID")
CLIENT_SECRET = lire_secret("CLIENT_SECRET")


def get_token():
    token_url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
    payload ={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    
    response= requests.post(token_url, data=payload, timeout=30)
    if response.status_code != 200 :
        raise Exception(f"Erreur token : {response.text}")
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token

def get_offre(access_token):
    url= "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers= { "Authorization": f"Bearer {access_token}"}
    params = {"motsCles": "data analyst","range": "0-149"}
    response= requests.get(url, headers= headers, params= params, timeout=30)
    if response.status_code not in [200, 206]:
        raise Exception(f"Erreur API {response.status_code}: {response.text}")
    data= response.json()
    offre = data.get("resultats",[])
    df= pd.json_normalize(offre)
    return df 




