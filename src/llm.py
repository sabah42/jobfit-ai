from groq import Groq 
import os 
from dotenv import load_dotenv
load_dotenv()
client= Groq(api_key= os.getenv("GROQ_API_KEY"))
def diagnostiquer_cv(cv_text, poste_cible="Data Analyst", industrie="Data / Analyse marketing", seniorite="Junior"):

    prompt = f"""
Tu es un recruteur Data Analyst senior.

Tu analyses uniquement le contenu textuel du CV.

Tu ne peux pas voir :
- les couleurs
- les polices
- les colonnes
- les tableaux
- les graphiques
- la mise en page

N'invente jamais ces informations.

Si une information n'est pas visible dans le texte, indique :
"Non vérifiable à partir du texte extrait."

Évalue :

1. Score ATS sur 100
2. Score Recruteur sur 100
3. Points forts
4. Points faibles
5. Mots-clés Data Analyst détectés
6. Mots-clés manquants
7. Compatibilité avec un poste Data Analyst Junior
8. Top 5 des améliorations prioritaires

CV : {cv_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
def analyser_compatibilite(cv_text, offre):
    prompt = f"""
Tu es un recruteur Data Analyst senior.

Analyse la compatibilité entre ce CV et cette offre.

Donne :

1. Score de compatibilité sur 100
2. Compétences du CV correspondant à l'offre
3. Compétences manquantes
4. Mots-clés ATS manquants
5. Forces du candidat
6. Faiblesses du candidat
7. Conseils pour adapter le CV à cette offre

CV : {cv_text}

OFFRE :

Titre : {offre["intitule"]}

Description : {offre["description"]}
"""
    
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

    return response.choices[0].message.content

def generer_cv_optimise(cv_text, offre):
    prompt = f"""
Tu es un expert ATS.

Ta mission n'est PAS de créer un nouveau CV.

Ta mission est d'améliorer le CV existant pour cette offre.

Règles obligatoires :

- Conserver les expériences existantes.
- Conserver les diplômes existants.
- Conserver les dates existantes.
- Conserver les projets existants.
- Ne jamais inventer une compétence.
- Ne jamais inventer une expérience.
- Ne jamais inventer un diplôme.
- Ne jamais inventer une responsabilité.
- Ne jamais inventer un nombre d'années d'expérience.

Tu peux uniquement :

- améliorer les formulations
- mettre en avant les mots-clés ATS présents dans l'offre
- réorganiser légèrement les compétences
- améliorer le résumé professionnel

Ne jamais ajouter de commentaires ou d'explications.

Retourne uniquement le CV optimisé.
OFFRE : {offre["description"]}

CV : {cv_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def generer_lettre_motivation(cv_text, offre):

    prompt = f"""
Tu es un recruteur expert.

Rédige une lettre de motivation professionnelle,
personnalisée pour cette offre.

CV du candidat :
{cv_text}

Offre :
Titre : {offre['intitule']}
Entreprise : {offre['entreprise.nom']}
Description :
{offre['description']}

Consignes :
- ton professionnel
- maximum une page
- mettre en avant les compétences du CV qui correspondent à l'offre
- éviter les phrases génériques
- français
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content