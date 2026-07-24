import pdfplumber 
import re
import unicodedata
def extract_text_from_pdf(uploaded_file):
    text= ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text= page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
def normaliser(texte):
    return unicodedata.normalize("NFD", texte).encode("ascii", "ignore").decode("utf-8").upper()
titres_connus = ["DATA ANALYST", "DATA SCIENTIST", "DATA ENGINEER"]

def extract_titre(cv_text):
    texte = cv_text.upper()
    titre = []
    for tit in titres_connus:
        if tit in texte:
             titre.append(tit.title())
    return titre
def extract_commune(cv_text):
    position=cv_text.upper().find("CONTACT")
    if position == -1:
        return None 
    contact= cv_text[position:]
    ville= re.search(r'([A-Za-zÀ-ÿ\- ]+)\s*\(\d{5}\)', contact)
    if ville:
        return ville.group(1).strip()
    else:
        return None
    

competences_connues = [ "PYTHON", "SQL", "POWER BI", "SAS", "MATLAB", "TABLEAU", "MYSQL", "EXCEL"]

def extract_competences(cv_text):
    texte = cv_text.upper()
    competences = []
    for comp in competences_connues:
        if comp in texte:
            competences.append(comp.title())
    return competences
langues_connues = ["FRANÇAIS", "ANGLAIS","ARABE"]

def extract_langues(cv_text):
    texte = cv_text.upper()
    langues = []
    for langue in langues_connues:
        if langue in texte:
            langues.append(langue.title())
    return langues

def extract_experience(cv_text):
    debut= cv_text.upper().find("EXPERIENCE")
    if debut == -1:
        return None 
    fin = cv_text.upper().find("DIPLOMES")
    experience = cv_text[debut:fin]
    
    experience=[ int(a) for a in re.findall(r'\b(20\d{2}|19\d{2})\b',experience)]
    if not experience:
        return 0
    return max(experience)- min(experience)
