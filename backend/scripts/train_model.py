from pathlib import Path
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

BASE = Path(__file__).resolve().parents[1]
data_path = BASE / "app" / "data" / "symptom_disease.csv"
model_dir = BASE / "app" / "models"
model_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_path)
X_text = df["symptoms"].fillna("")
y = df["disease"]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(X_text)

model = RandomForestClassifier(
    n_estimators=250,
    random_state=42,
    class_weight="balanced_subsample"
)
model.fit(X, y)

joblib.dump(
    {"vectorizer": vectorizer, "model": model},
    model_dir / "disease_model.joblib"
)
print(f"Saved model to {model_dir / 'disease_model.joblib'}")
