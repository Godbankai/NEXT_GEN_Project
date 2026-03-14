import json
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.db_models import ChatMessage, Exam, ExamSession, ProctorEvent


def _question_payload(exam: Exam) -> list[dict]:
    return json.loads(exam.questions_json)


def create_exam(db: Session, admin_id: int, payload) -> Exam:
    join_code = f"EXAM-{payload.subject[:2].upper()}-{int(datetime.utcnow().timestamp())}"
    exam = Exam(title=payload.title, subject=payload.subject, description=payload.description, duration_minutes=payload.duration_minutes, instructions=payload.instructions, questions_json=json.dumps(payload.questions), status=payload.status, join_code=join_code, created_by=admin_id)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def serialize_exam(exam: Exam) -> dict:
    questions = _question_payload(exam)
    total_marks = sum(int(question.get("marks", 4)) for question in questions)
    return {
        "id": exam.id,
        "title": exam.title,
        "subject": exam.subject,
        "description": exam.description,
        "duration_minutes": exam.duration_minutes,
        "instructions": exam.instructions,
        "questions": questions,
        "question_count": len(questions),
        "total_marks": total_marks,
        "status": exam.status,
        "join_code": exam.join_code,
        "created_at": exam.created_at.isoformat(),
    }


def list_exams(db: Session, role: str) -> list[dict]:
    exams = db.scalars(select(Exam).order_by(Exam.created_at.desc())).all()
    if role == "student":
        exams = [exam for exam in exams if exam.status == "published"]
    return [serialize_exam(exam) for exam in exams]


def start_session(db: Session, exam_id: int, student_id: int) -> ExamSession:
    existing = db.scalar(select(ExamSession).where(ExamSession.exam_id == exam_id, ExamSession.student_id == student_id))
    if existing:
        if existing.status == "submitted":
            return existing
        if existing.is_locked:
            return existing
        if existing.status == "in_progress":
            return existing

    session = existing or ExamSession(exam_id=exam_id, student_id=student_id)
    session.status = "in_progress"
    session.is_locked = False
    session.lock_reason = None
    if not session.started_at:
        session.started_at = datetime.utcnow()
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def submit_session(db: Session, session: ExamSession, answers: dict) -> ExamSession:
    exam_questions = _question_payload(session.exam)
    score = 0
    total_marks = 0
    for question in exam_questions:
        marks = int(question.get("marks", 4))
        correct = question.get("answer")
        question_id = str(question.get("id"))
        total_marks += marks
        if correct is None:
            continue
        if str(answers.get(question_id, "")).strip().lower() == str(correct).strip().lower():
            score += marks

    session.answers_json = json.dumps(answers)
    session.status = "submitted"
    session.submitted_at = datetime.utcnow()
    session.score = score if total_marks else None
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def session_overview(db: Session) -> list[dict]:
    sessions = db.scalars(select(ExamSession).options(joinedload(ExamSession.exam), joinedload(ExamSession.student)).order_by(ExamSession.created_at.desc())).all()
    return [{"id": session.id, "exam_title": session.exam.title, "student_name": session.student.full_name, "status": session.status, "score": session.score, "suspicious_score": session.suspicious_score, "warning_count": session.warning_count, "is_locked": session.is_locked, "lock_reason": session.lock_reason, "join_code": session.exam.join_code, "latest_snapshot_path": session.latest_snapshot_path, "started_at": session.started_at.isoformat() if session.started_at else None, "submitted_at": session.submitted_at.isoformat() if session.submitted_at else None} for session in sessions]


def analytics_summary(db: Session) -> dict:
    total_students = db.scalar(select(func.count()).select_from(ExamSession)) or 0
    total_exams = db.scalar(select(func.count()).select_from(Exam)) or 0
    flagged_events = db.scalar(select(func.count()).select_from(ProctorEvent)) or 0
    total_messages = db.scalar(select(func.count()).select_from(ChatMessage)) or 0
    avg_suspicious = db.scalar(select(func.avg(ExamSession.suspicious_score))) or 0
    return {"total_exams": total_exams, "total_sessions": total_students, "flagged_events": flagged_events, "total_messages": total_messages, "average_suspicious_score": round(float(avg_suspicious), 2)}
