import re

# A broad educational symptom vocabulary.
# Add more entries over time or move this into a JSON/database file.
SYMPTOMS = {
    # General
    "fever",
    "chills",
    "fatigue",
    "weakness",
    "weight loss",
    "loss of appetite",
    "night sweats",
    "dehydration",

    # Head / neurological
    "headache",
    "severe headache",
    "migraine",
    "dizziness",
    "fainting",
    "confusion",
    "seizure",
    "numbness",
    "tingling",
    "memory loss",
    "blurred vision",
    "double vision",

    # Eye / ear / nose / throat
    "eye pain",
    "red eye",
    "vision loss",
    "ear pain",
    "hearing loss",
    "ringing in ears",
    "runny nose",
    "nasal congestion",
    "sneezing",
    "sinus pain",
    "sore throat",
    "hoarseness",
    "difficulty swallowing",

    # Respiratory
    "cough",
    "dry cough",
    "wet cough",
    "persistent cough",
    "shortness of breath",
    "breathlessness",
    "wheezing",
    "chest congestion",
    "coughing blood",

    # Heart / circulation
    "chest pain",
    "chest pressure",
    "palpitations",
    "rapid heartbeat",
    "irregular heartbeat",
    "swelling in legs",

    # Gastrointestinal
    "abdominal pain",
    "stomach pain",
    "upper abdominal pain",
    "lower abdominal pain",
    "nausea",
    "vomiting",
    "diarrhea",
    "constipation",
    "blood in stool",
    "black stool",
    "bloating",
    "heartburn",
    "indigestion",

    # Urinary / kidney
    "kidney pain",
    "flank pain",
    "back pain",
    "lower back pain",
    "painful urination",
    "burning urination",
    "frequent urination",
    "blood in urine",
    "difficulty urinating",
    "urinary urgency",
    "dark urine",

    # Muscles / joints
    "body ache",
    "muscle pain",
    "joint pain",
    "joint swelling",
    "neck pain",
    "stiff neck",
    "shoulder pain",
    "knee pain",
    "leg pain",

    # Skin
    "rash",
    "itching",
    "skin redness",
    "hives",
    "swelling",

    # Infectious / flu-like
    "loss of taste",
    "loss of smell",
    "sweating",

    # Reproductive / pelvic
    "pelvic pain",
    "testicular pain",
    "vaginal bleeding",

    # Mental / sleep
    "insomnia",
    "anxiety",
}

ALIASES = {
    # General
    "high temperature": "fever",
    "temperature": "fever",
    "feeling hot": "fever",
    "tired": "fatigue",
    "tiredness": "fatigue",
    "exhausted": "fatigue",
    "no energy": "fatigue",

    # Respiratory
    "trouble breathing": "shortness of breath",
    "difficulty breathing": "shortness of breath",
    "breathing difficulty": "shortness of breath",
    "cannot breathe": "shortness of breath",
    "cant breathe": "shortness of breath",

    # Pain
    "stomach ache": "abdominal pain",
    "stomach pain": "abdominal pain",
    "head pain": "headache",
    "pain in my head": "headache",

    # Kidney / urinary
    "pain in kidney": "kidney pain",
    "pain in my kidney": "kidney pain",
    "kidneys hurt": "kidney pain",
    "kidney hurts": "kidney pain",
    "pain in side": "flank pain",
    "pain while urinating": "painful urination",
    "pain when urinating": "painful urination",
    "burning when urinating": "burning urination",
    "burning pee": "burning urination",
    "blood in pee": "blood in urine",

    # GI
    "throwing up": "vomiting",
    "throw up": "vomiting",
    "loose motion": "diarrhea",
    "loose motions": "diarrhea",

    # Neuro
    "passed out": "fainting",
    "passed out suddenly": "fainting",
    "pins and needles": "tingling",

    # ENT
    "blocked nose": "nasal congestion",
    "stuffy nose": "nasal congestion",
}


def extract_symptoms(text: str):
    clean = text.lower().strip()

    # Normalize aliases first
    for alias, canonical in ALIASES.items():
        clean = re.sub(
            r"\b" + re.escape(alias) + r"\b",
            canonical,
            clean
        )

    found = set()

    # Match longest phrases first
    for symptom in sorted(SYMPTOMS, key=len, reverse=True):
        pattern = r"\b" + re.escape(symptom) + r"\b"
        if re.search(pattern, clean):
            found.add(symptom)

    return sorted(found)
