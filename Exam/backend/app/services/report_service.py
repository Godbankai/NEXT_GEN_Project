from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from backend.app.models.db_models import ExamSession


def build_session_report(session: ExamSession) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("AI Based Smart Exam Monitoring and Proctoring Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Student: {session.student.full_name}", styles["BodyText"]),
        Paragraph(f"Email: {session.student.email}", styles["BodyText"]),
        Paragraph(f"Exam: {session.exam.title}", styles["BodyText"]),
        Paragraph(f"Subject: {session.exam.subject}", styles["BodyText"]),
        Paragraph(f"Status: {session.status}", styles["BodyText"]),
        Paragraph(f"Score: {session.score if session.score is not None else 'Pending'}", styles["BodyText"]),
        Paragraph(f"Suspicious Score: {session.suspicious_score}", styles["BodyText"]),
        Spacer(1, 14),
    ]

    data = [["Time", "Type", "Severity", "Message"]]
    for event in session.events:
        data.append([
            event.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            event.event_type,
            event.severity,
            event.message,
        ])
    if len(data) == 1:
        data.append(["-", "clean_session", "low", "No suspicious activity recorded."])

    table = Table(data, repeatRows=1, colWidths=[110, 100, 70, 230])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(table)
    doc.build(story)
    return buffer.getvalue()
