from pydantic import BaseModel, Field
from typing import List

class AnalyzeRequest(BaseModel):
    symptoms_text: str = Field(min_length=2, max_length=5000)
    include_llm: bool = True

class Prediction(BaseModel):
    disease: str
    confidence: float

class AnalysisResponse(BaseModel):
    extracted_symptoms: List[str]
    predictions: List[Prediction]
    severity: str
    red_flags: List[str]
    advice: str
    disclaimer: str

class ReportRequest(AnalyzeRequest):
    pass
