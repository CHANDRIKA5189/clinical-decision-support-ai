from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analysis():
    response = client.post("/api/analyze", json={
        "symptoms_text": "I have fever, cough and sore throat.",
        "include_llm": False
    })
    assert response.status_code == 200
    data = response.json()
    assert "extracted_symptoms" in data
    assert "predictions" in data
    assert data["severity"] in {"low", "medium", "high"}
