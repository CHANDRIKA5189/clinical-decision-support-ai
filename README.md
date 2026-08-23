# AI-Powered Clinical Decision Support System

A professional full-stack healthcare AI prototype combining NLP, machine learning, severity assessment, LLM-assisted explanations, PDF reporting, and browser voice input.

> **Important:** This project is an educational/engineering prototype, not a medical device and not a substitute for professional medical diagnosis or emergency care. Predictions are illustrative and should not be used for treatment decisions.

## Architecture

- **Frontend:** React + Vite
- **Backend:** FastAPI + Pydantic
- **NLP:** spaCy
- **ML:** scikit-learn Random Forest; optional XGBoost
- **LLM:** provider-agnostic OpenAI-compatible endpoint
- **Reports:** ReportLab PDF
- **Voice:** Web Speech API
- **Testing:** pytest + frontend unit-test-ready structure
- **Deployment:** Docker Compose

## Features

1. Natural-language symptom extraction with spaCy.
2. Disease prediction using a trained Random Forest model.
3. Optional XGBoost model support.
4. Top-k predictions with calibrated-style confidence scores.
5. Low/medium/high severity assessment.
6. Safety-oriented emergency red-flag detection.
7. LLM-generated plain-language educational guidance.
8. Downloadable PDF report.
9. Browser voice symptom input.
10. Responsive UI and API health endpoint.
11. Training script and sample synthetic dataset.
12. Dockerized development/production setup.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python scripts/train_model.py
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

### Docker

```bash
docker compose up --build
```

## Optional LLM configuration

Copy `.env.example` to `.env` and configure:

- `LLM_ENABLED=true`
- `LLM_BASE_URL=https://api.openai.com/v1`
- `LLM_API_KEY=your_key`
- `LLM_MODEL=your_model`

The application remains functional without an LLM; it falls back to a deterministic educational response.

## API

- `GET /api/health`
- `POST /api/analyze`
- `POST /api/report`

Example:

```json
{
  "symptoms_text": "I have fever, cough and sore throat for two days.",
  "include_llm": true
}
```

## Project structure

```text
clinical_decision_support_ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── schemas.py
│   │   ├── services/
│   │   │   ├── nlp_service.py
│   │   │   ├── ml_service.py
│   │   │   ├── severity_service.py
│   │   │   ├── llm_service.py
│   │   │   └── report_service.py
│   │   └── data/
│   │       └── symptom_disease.csv
│   ├── scripts/train_model.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Safety design

The backend deliberately distinguishes **prediction** from **clinical diagnosis**. High-risk red flags are surfaced separately. The UI tells users to seek emergency care when appropriate and recommends clinician review for concerning symptoms.

Do not train or evaluate this prototype on identifiable patient data. For production healthcare deployment, add clinical validation, privacy/security controls, audit logging, access control, monitoring, bias assessment, governance, regulatory review, and human-in-the-loop workflows.
