import re

try:
    import spacy
    NLP = spacy.load("en_core_web_sm")
except Exception:
    NLP = None

SYMPTOMS = {
    "fever", "cough", "dry cough", "sore throat", "fatigue", "headache",
    "body ache", "muscle pain", "nausea", "vomiting", "diarrhea",
    "abdominal pain", "chest pain", "shortness of breath", "breathlessness",
    "runny nose", "congestion", "sneezing", "dizziness", "rash",
    "loss of taste", "loss of smell", "joint pain", "chills"
}

ALIASES = {
    "high temperature": "fever",
    "temperature": "fever",
    "tiredness": "fatigue",
    "stomach pain": "abdominal pain",
    "trouble breathing": "shortness of breath",
    "difficulty breathing": "shortness of breath",
    "breathing difficulty": "shortness of breath",
}

def extract_symptoms(text: str):
    clean = text.lower()
    for alias, canonical in ALIASES.items():
        clean = clean.replace(alias, canonical)

    found = set()
    for symptom in sorted(SYMPTOMS, key=len, reverse=True):
        if re.search(r"\b" + re.escape(symptom) + r"\b", clean):
            found.add(symptom)

    if NLP:
        doc = NLP(text)
        for chunk in doc.noun_chunks:
            phrase = chunk.text.lower().strip()
            if phrase in SYMPTOMS:
                found.add(phrase)

    return sorted(found)
