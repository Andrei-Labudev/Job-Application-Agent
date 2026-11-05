"""
One-page cover letter builder with the same header style as the resume.

cover_data schema (JSON or dict):
{
  "name": "Jane Doe", "location": "City, ST", "phone": "...", "email": "...",
  "date": "October 28, 2026",
  "recipient": ["Hiring Team", "Company Name"],
  "paragraphs": ["Dear Hiring Team,", "...", "..."],
  "closing": "Sincerely," (optional)
}
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

from resume_builder import esc

S = {
    "name": ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=17, leading=19, spaceAfter=1),
    "contact": ParagraphStyle("c", fontName="Helvetica", fontSize=9, leading=11, spaceAfter=6),
    "body": ParagraphStyle("b", fontName="Helvetica", fontSize=10.5, leading=14.5, spaceAfter=10),
}


def build_cover(data: dict, output_path: str) -> None:
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        title=f"{data['name']} - Cover Letter", author=data["name"],
    )
    contact = [data.get(k, "") for k in ("location", "phone", "email", "linkedin")]
    story = [
        Paragraph(esc(data["name"]), S["name"]),
        Paragraph(esc("  |  ".join(c for c in contact if c)), S["contact"]),
        HRFlowable(width="100%", thickness=0.75, color="#1a1a1a", spaceAfter=14),
        Paragraph(esc(data["date"]), S["body"]),
    ]
    if data.get("recipient"):
        story.append(Paragraph("<br/>".join(esc(r) for r in data["recipient"]), S["body"]))
    story += [Paragraph(esc(p), S["body"]) for p in data["paragraphs"]]
    story.append(Paragraph(f"{esc(data.get('closing', 'Sincerely,'))}<br/>{esc(data['name'])}", S["body"]))
    doc.build(story)
