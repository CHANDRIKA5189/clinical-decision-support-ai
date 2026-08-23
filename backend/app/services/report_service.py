from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def build_pdf(result):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("AI-Powered Clinical Decision Support Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph("Educational prototype — not a medical diagnosis.", styles["Heading2"]),
        Spacer(1, 12),
        Paragraph("Extracted symptoms: " + ", ".join(result["extracted_symptoms"]) or "None", styles["BodyText"]),
        Spacer(1, 10),
        Paragraph(f"Severity: {result['severity'].upper()}", styles["BodyText"]),
        Spacer(1, 10),
    ]
    data = [["Disease / condition", "Model confidence"]]
    data += [[p["disease"], f"{p['confidence']:.1%}"] for p in result["predictions"]]
    table = Table(data, colWidths=[320, 120])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    story += [table, Spacer(1, 14), Paragraph("Advice", styles["Heading2"]),
              Paragraph(result["advice"], styles["BodyText"]), Spacer(1, 14)]
    if result["red_flags"]:
        story += [Paragraph("Safety flags", styles["Heading2"])]
        story += [Paragraph("• " + x, styles["BodyText"]) for x in result["red_flags"]]
        story += [Spacer(1, 12)]
    story += [Paragraph(result["disclaimer"], styles["BodyText"])]
    doc.build(story)
    buffer.seek(0)
    return buffer
