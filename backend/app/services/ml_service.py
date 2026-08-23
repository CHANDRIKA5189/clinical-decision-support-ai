from pathlib import Path
import joblib
import numpy as np

class DiseaseModel:
    def __init__(self, model_path="app/models/disease_model.joblib"):
        self.model_path = Path(model_path)
        self.bundle = None
        if self.model_path.exists():
            self.bundle = joblib.load(self.model_path)

    def predict(self, symptoms):
        if not self.bundle:
            return [{"disease": "Insufficient data", "confidence": 0.0}]

        vectorizer = self.bundle["vectorizer"]
        model = self.bundle["model"]
        X = vectorizer.transform([" ".join(symptoms)])
        probabilities = model.predict_proba(X)[0]
        classes = model.classes_
        order = np.argsort(probabilities)[::-1][:3]
        return [
            {"disease": str(classes[i]), "confidence": round(float(probabilities[i]), 4)}
            for i in order
        ]
