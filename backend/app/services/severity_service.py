HIGH_RISK = {
    "chest pain": "Chest pain can require urgent medical assessment.",
    "shortness of breath": "Breathing difficulty can require urgent medical assessment.",
    "breathlessness": "Breathing difficulty can require urgent medical assessment."
}

def assess_severity(symptoms):
    flags = [message for key, message in HIGH_RISK.items() if key in symptoms]
    if flags:
        return "high", flags
    if len(symptoms) >= 4 or any(s in symptoms for s in {"fever", "vomiting", "dizziness"}):
        return "medium", []
    return "low", []
