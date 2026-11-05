"""
One-page, ATS-friendly resume builder.

Design:
- Single column; no tables, text boxes or graphics that ATS parsers choke on
- Built-in PDF font (Helvetica) so the text is always real and extractable
- Standard section order, plain bullets, left-aligned
- If content overflows one page, cut bullets; don't go below ~9pt fonts or 0.5in margins

resume_data schema (JSON or dict):
{
  "name": "Jane Doe",
  "location": "City, ST", "phone": "...", "email": "...", "linkedin": "..." (optional),
  "summary": "2-3 sentences" (optional),
  "experience": [
    {
      "org": "Company", "org_location": "City, ST" (optional),
      "title": "Official title", "dates": "Jan 2022 - Present",
      "bullets": ["...", "..."]            # flat entry
      # OR grouped entry: several project roles under one official title
      "roles": [{"title": "...", "dates": "...", "bullets": ["..."]}]
    }
  ],
  "skills": [["Category", "item, item, item"], ...],
  "certifications": "..." (optional),
  "education": [{"school": "...", "detail": "...", "dates": "..."}] (optional)
}
Text may use <b> and <i>. Bare "&" is escaped automatically.
Helvetica only covers Western-European characters: avoid arrows, emoji and
symbols (en/em dashes, curly quotes and bullets are fine).
"""

import re

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate

FONT, FONT_BOLD, FONT_ITALIC = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
MARGIN = 0.55 * inch
INK = "#1a1a1a"


def _s(name, **kw):
    base = dict(fontName=FONT, textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)


STYLES = {
    "name": _s("name", fontName=FONT_BOLD, fontSize=17, leading=19, spaceAfter=1),
    "contact": _s("contact", fontSize=9, leading=11, spaceAfter=6),
    "summary": _s("summary", fontSize=9.5, leading=12, spaceAfter=8),
    "section": _s("section", fontName=FONT_BOLD, fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=2),
    "org": _s("org", fontName=FONT_BOLD, fontSize=9.7, leading=12, spaceBefore=5),
    "meta": _s("meta", fontName=FONT_ITALIC, fontSize=9, leading=11, spaceAfter=2),
    "subrole": _s("subrole", fontName=FONT_BOLD, fontSize=9.2, leading=11.3, spaceBefore=3, spaceAfter=1.5),
    "bullet": _s("bullet", fontSize=9.3, leading=11.3, spaceAfter=1.5, leftIndent=12),
}


def esc(text: str) -> str:
    """Escape bare ampersands; leave entities and <b>/<i> tags alone."""
    return re.sub(r"&(?!#?\w+;)", "&amp;", str(text))


def _rule():
    return HRFlowable(width="100%", thickness=0.75, color=INK, spaceBefore=1, spaceAfter=5)


def _section(title):
    return [Paragraph(title.upper(), STYLES["section"]), _rule()]


def _bullets(items):
    return [Paragraph(f"&bull;&nbsp;&nbsp;{esc(i)}", STYLES["bullet"]) for i in items]


def build_resume(data: dict, output_path: str) -> None:
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
        title=f"{data['name']} - Resume", author=data["name"],
    )
    story = [Paragraph(esc(data["name"]), STYLES["name"])]
    contact = [data.get(k, "") for k in ("location", "phone", "email", "linkedin")]
    story.append(Paragraph(esc("  |  ".join(c for c in contact if c)), STYLES["contact"]))

    if data.get("summary"):
        story.append(Paragraph(esc(data["summary"]), STYLES["summary"]))

    story += _section("Experience")
    for job in data["experience"]:
        org = esc(job["org"]) + (f" — {esc(job['org_location'])}" if job.get("org_location") else "")
        header = [Paragraph(org, STYLES["org"]),
                  Paragraph(f"{esc(job['title'])} | {esc(job['dates'])}", STYLES["meta"])]
        if job.get("roles"):
            for n, sub in enumerate(job["roles"]):
                bl = _bullets(sub["bullets"])
                lead = [Paragraph(f"{esc(sub['title'])} | {esc(sub['dates'])}", STYLES["subrole"])] + bl[:1]
                story.append(KeepTogether((header if n == 0 else []) + lead))
                story += bl[1:]
        else:
            bl = _bullets(job["bullets"])
            story.append(KeepTogether(header + bl[:1]))
            story += bl[1:]

    if data.get("skills"):
        story += _section("Skills")
        for label, items in data["skills"]:
            story.append(Paragraph(f"<b>{esc(label)}:</b> {esc(items)}", STYLES["bullet"]))

    if data.get("certifications"):
        story += _section("Certifications")
        story.append(Paragraph(esc(data["certifications"]), STYLES["bullet"]))

    if data.get("education"):
        story += _section("Education")
        for ed in data["education"]:
            line = esc(ed["school"]) + (f" — {esc(ed['dates'])}" if ed.get("dates") else "")
            story.append(Paragraph(line, STYLES["org"]))
            if ed.get("detail"):
                story.append(Paragraph(esc(ed["detail"]), STYLES["bullet"]))

    doc.build(story)
