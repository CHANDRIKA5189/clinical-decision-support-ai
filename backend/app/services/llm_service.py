import httpx
from app.config import settings


DISCLAIMER = (
    "Educational information only. This system does not provide a medical "
    "diagnosis or replace examination by a qualified healthcare professional."
)


def fallback_advice(symptoms, predictions, severity):

    if not predictions:
        return (
            "The reported symptoms did not produce a strong educational match. "
            "Consider discussing persistent or concerning symptoms with a qualified clinician."
        )

    top = predictions[0]

    disease = top.get(
        "disease",
        "an undetermined condition"
    )

    specialist = top.get(
        "specialist",
        "General physician"
    )

    matched = top.get(
        "matched_symptoms",
        symptoms
    )

    advice = (
        f"Educational assessment: the strongest symptom-pattern match was "
        f"'{disease}'. "
    )

    if matched:
        advice += (
            f"The symptoms contributing to this educational match include: "
            f"{', '.join(matched)}. "
        )

    advice += (
        f"For appropriate clinical evaluation, a suitable healthcare professional "
        f"may be a {specialist}. "
    )

    if severity == "high":
        advice += (
            "Because the severity classification is high, prompt medical evaluation "
            "is recommended. If symptoms are severe, rapidly worsening, or include "
            "difficulty breathing, severe chest pain, confusion, or loss of consciousness, "
            "seek emergency care."
        )

    elif severity == "medium":
        advice += (
            "Because the severity classification is moderate, monitoring alone may not "
            "be sufficient if symptoms persist or worsen. Consider contacting a qualified "
            "healthcare professional."
        )

    else:
        advice += (
            "The current severity classification is low, but symptoms should still be "
            "monitored. Seek professional medical advice if they persist, worsen, or "
            "new concerning symptoms develop."
        )

    return advice


async def generate_advice(symptoms, predictions, severity):

    if (
        not settings.llm_enabled
        or not settings.llm_api_key
        or not settings.llm_model
    ):
        return fallback_advice(
            symptoms,
            predictions,
            severity
        )

    top_prediction = predictions[0] if predictions else {}

    prompt = f"""
You are generating educational clinical decision-support information.

IMPORTANT:
- This is NOT a medical diagnosis.
- Do not claim certainty.
- Do not prescribe medication or dosage.
- Explain why the reported symptom pattern may relate to the educational match.
- Mention the most relevant healthcare specialist or type of clinician.
- Include clear advice about when urgent medical attention may be appropriate.
- Make the response specific to the symptoms instead of using generic repeated text.

Reported symptoms:
{", ".join(symptoms) if symptoms else "No recognized symptoms"}

Top educational prediction:
{top_prediction}

All predictions:
{predictions}

Severity:
{severity}

Write a concise but specific educational explanation.
"""

    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}"
    }

    payload = {
        "model": settings.llm_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a safety-focused educational health assistant. "
                    "Provide non-diagnostic symptom education."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4
    }

    async with httpx.AsyncClient(timeout=30) as client:

        response = await client.post(
            f"{settings.llm_base_url.rstrip('/')}/chat/completions",
            json=payload,
            headers=headers,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]
