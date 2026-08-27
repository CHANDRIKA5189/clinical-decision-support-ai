from pathlib import Path
import joblib
import numpy as np


CONDITION_PROFILES = {
    "Influenza": {
        "symptoms": {
            "fever",
            "chills",
            "cough",
            "sore throat",
            "fatigue",
            "body ache",
            "headache"
        },
        "specialist": "General physician"
    },

    "Common Cold": {
        "symptoms": {
            "cough",
            "runny nose",
            "nasal congestion",
            "sneezing",
            "sore throat"
        },
        "specialist": "General physician or ENT specialist"
    },

    "COVID-19-like Viral Illness": {
        "symptoms": {
            "fever",
            "cough",
            "fatigue",
            "loss of taste",
            "loss of smell",
            "sore throat"
        },
        "specialist": "General physician"
    },

    "Migraine": {
        "symptoms": {
            "headache",
            "severe headache",
            "migraine",
            "nausea",
            "vomiting",
            "blurred vision"
        },
        "specialist": "Neurologist"
    },

    "Gastroenteritis": {
        "symptoms": {
            "abdominal pain",
            "nausea",
            "vomiting",
            "diarrhea",
            "fever"
        },
        "specialist": "General physician or gastroenterologist"
    },

    "Urinary Tract Infection": {
        "symptoms": {
            "painful urination",
            "burning urination",
            "frequent urination",
            "urinary urgency",
            "blood in urine"
        },
        "specialist": "General physician or urologist"
    },

    "Kidney Stone": {
        "symptoms": {
            "kidney pain",
            "flank pain",
            "back pain",
            "blood in urine",
            "nausea",
            "vomiting",
            "painful urination"
        },
        "specialist": "Urologist"
    },

    "Asthma-like Airway Condition": {
        "symptoms": {
            "shortness of breath",
            "wheezing",
            "cough",
            "chest congestion"
        },
        "specialist": "Pulmonologist"
    },

    "Possible Pneumonia": {
        "symptoms": {
            "fever",
            "cough",
            "shortness of breath",
            "chills",
            "chest pain",
            "fatigue"
        },
        "specialist": "General physician or pulmonologist"
    },

    "Possible Cardiac Concern": {
        "symptoms": {
            "chest pain",
            "chest pressure",
            "shortness of breath",
            "palpitations",
            "dizziness"
        },
        "specialist": "Cardiologist or emergency care"
    },

    "Sinusitis-like Condition": {
        "symptoms": {
            "sinus pain",
            "headache",
            "nasal congestion",
            "runny nose",
            "fever"
        },
        "specialist": "ENT specialist"
    },

    "Allergic Reaction": {
        "symptoms": {
            "rash",
            "itching",
            "hives",
            "swelling",
            "sneezing"
        },
        "specialist": "General physician or allergist"
    },
}


class DiseaseModel:

    def __init__(self, model_path="app/models/disease_model.joblib"):
        self.model_path = Path(model_path)
        self.bundle = None

        if self.model_path.exists():
            self.bundle = joblib.load(self.model_path)

    def knowledge_predict(self, symptoms):
        symptom_set = set(symptoms)

        results = []

        for disease, profile in CONDITION_PROFILES.items():
            disease_symptoms = profile["symptoms"]

            matches = symptom_set.intersection(disease_symptoms)

            if not matches:
                continue

            score = len(matches) / len(disease_symptoms)

            # Educational matching score
            confidence = min(
                0.95,
                0.15 + score * 0.80
            )

            results.append({
                "disease": disease,
                "confidence": round(confidence, 4),
                "matched_symptoms": sorted(matches),
                "specialist": profile["specialist"]
            })

        results.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return results[:3]

    def predict(self, symptoms):

        # First use the educational knowledge base
        knowledge_results = self.knowledge_predict(symptoms)

        # If nothing matched, return a meaningful response
        if not knowledge_results:
            return [{
                "disease": "No strong educational match",
                "confidence": 0.0,
                "matched_symptoms": symptoms,
                "specialist": "General physician"
            }]

        return knowledge_results
