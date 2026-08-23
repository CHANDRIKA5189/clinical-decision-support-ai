import httpx
from app.config import settings

DISCLAIMER = (
    "Educational information only. This system does not provide a medical diagnosis "
    "or replace a qualified healthcare professional."
)

def fallback_advice(predictions, severity):
    top = predictions[0]["disease"] if predictions else "an undetermined condition"
    if severity == "high":
        return (
            f"Some reported symptoms may warrant prompt medical evaluation. "
            f"The model's top educational match was {top}. If symptoms are severe, "
            "rapidly worsening, or involve difficulty breathing or significant chest pain, "
            "seek urgent medical care."
        )
    return (
        f"The model's top educational match was {top}. Rest, hydration, and monitoring "
        "may be reasonable for mild symptoms, but persistent, worsening, or concerning "
        "symptoms should be assessed by a qualified clinician."
    )

async def generate_advice(symptoms, predictions, severity):
    if not settings.llm_enabled or not settings.llm_api_key or not settings.llm_model:
        return fallback_advice(predictions, severity)

    prompt = (
        "Provide cautious, non-diagnostic educational health guidance. "
        "Do not prescribe medication or claim certainty. Encourage clinician review "
        "where appropriate. Reported symptoms: " + ", ".join(symptoms) +
        ". Model predictions: " + str(predictions) +
        f". Severity category: {severity}."
    )
    headers = {"Authorization": f"Bearer {settings.llm_api_key}"}
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": "You are a safety-focused health education assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{settings.llm_base_url.rstrip('/')}/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
