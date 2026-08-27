from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    symptoms_text: str
    include_llm: bool = True


class Prediction(BaseModel):
    disease: str
    confidence: float
    matched_symptoms: List[str] = []
    specialist: str = "General physician"


class AnalysisResponse(BaseModel):
    extracted_symptoms: List[str]
    predictions: List[Prediction]
    severity: str
    red_flags: List[str]
    advice: str
    disclaimer: str
