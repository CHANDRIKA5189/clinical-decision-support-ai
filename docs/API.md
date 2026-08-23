# API Reference

## GET /api/health

Returns service status.

## POST /api/analyze

Request:

```json
{
  "symptoms_text": "fever and cough",
  "include_llm": true
}
```

Response fields:

- `extracted_symptoms`
- `predictions`
- `severity`
- `red_flags`
- `advice`
- `disclaimer`

## POST /api/report

Accepts the same request and returns a PDF file.
