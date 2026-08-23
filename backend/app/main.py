from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.config import settings
from app.schemas import AnalyzeRequest, AnalysisResponse
from app.services.nlp_service import extract_symptoms
from app.services.ml_service import DiseaseModel
from app.services.severity_service import assess_severity
from app.services.llm_service import generate_advice, DISCLAIMER
from app.services.report_service import build_pdf

app = FastAPI(title="Clinical Decision Support AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = DiseaseModel(settings.model_path)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "clinical-decision-support-ai"}

async def run_analysis(request: AnalyzeRequest):
    symptoms = extract_symptoms(request.symptoms_text)
    predictions = model.predict(symptoms)
    severity, flags = assess_severity(symptoms)
    advice = await generate_advice(symptoms, predictions, severity) if request.include_llm else "LLM guidance disabled."
    return {
        "extracted_symptoms": symptoms,
        "predictions": predictions,
        "severity": severity,
        "red_flags": flags,
        "advice": advice,
        "disclaimer": DISCLAIMER,
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalyzeRequest):
    return await run_analysis(request)

@app.post("/api/report")
async def report(request: AnalyzeRequest):
    result = await run_analysis(request)
    pdf = build_pdf(result)
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="clinical_ai_report.pdf"'}
    )
