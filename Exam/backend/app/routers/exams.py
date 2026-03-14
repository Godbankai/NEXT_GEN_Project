from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.database import get_db
from backend.app.models.db_models import ChatMessage, Exam, ExamSession
from backend.app.models.schemas import ChatMessageRequest, ExamCreateRequest, SessionStartRequest, SessionSubmitRequest
from backend.app.routers.deps import get_current_user, require_role
from backend.app.services.exam_service import create_exam, list_exams, serialize_exam, start_session, submit_session

router = APIRouter()


def _load_session(db: Session, session_id: int) -> ExamSession | None:
    return db.scalar(select(ExamSession).options(joinedload(ExamSession.exam), joinedload(ExamSession.student)).where(ExamSession.id == session_id))


@router.get("")
def get_exams(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return {"items": list_exams(db, current_user.role)}


@router.get("/join/{join_code}")
def get_exam_by_join_code(join_code: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    exam = db.scalar(select(Exam).where(Exam.join_code == join_code))
    if not exam or exam.status != "published":
        raise HTTPException(status_code=404, detail="Join link is invalid.")
    return {"exam_id": exam.id, "exam_url": f"/exam/{exam.id}"}


@router.post("")
def create_exam_route(payload: ExamCreateRequest, db: Session = Depends(get_db), admin=Depends(require_role("admin"))):
    exam = create_exam(db, admin.id, payload)
    return {"item": serialize_exam(exam)}


@router.post("/sessions/start")
def start_exam_session(payload: SessionStartRequest, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    session = start_session(db, payload.exam_id, student.id)
    return {"session_id": session.id, "status": session.status, "is_locked": session.is_locked, "lock_reason": session.lock_reason}


@router.get("/sessions/{session_id}/status")
def session_status(session_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = _load_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if current_user.role != "admin" and session.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")
    return {
        "status": session.status,
        "is_locked": session.is_locked,
        "lock_reason": session.lock_reason,
        "warning_count": session.warning_count,
        "suspicious_score": session.suspicious_score,
    }


@router.get("/sessions/{session_id}/chat")
def list_chat_messages(session_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = _load_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if current_user.role != "admin" and session.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")
    messages = db.scalars(select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())).all()
    return {"items": [{"id": item.id, "sender_role": item.sender_role, "sender_name": item.sender.full_name, "message": item.message, "created_at": item.created_at.isoformat()} for item in messages]}


@router.post("/sessions/{session_id}/chat")
def send_chat_message(session_id: int, payload: ChatMessageRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = _load_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if current_user.role != "admin" and session.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")
    message = ChatMessage(session_id=session_id, sender_id=current_user.id, sender_role=current_user.role, message=payload.message)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"item": {"id": message.id, "sender_role": message.sender_role, "sender_name": current_user.full_name, "message": message.message, "created_at": message.created_at.isoformat()}}


@router.post("/sessions/{session_id}/submit")
def submit_exam_session(session_id: int, payload: SessionSubmitRequest, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    session = db.scalar(select(ExamSession).options(joinedload(ExamSession.exam)).where(ExamSession.id == session_id, ExamSession.student_id == student.id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.is_locked:
        raise HTTPException(status_code=423, detail=session.lock_reason or "Exam is locked by admin/proctoring system.")
    session = submit_session(db, session, payload.answers)
    return {"score": session.score, "status": session.status}


@router.get("/{exam_id}")
def exam_detail(exam_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    exam = db.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")
    if current_user.role == "student" and exam.status != "published":
        raise HTTPException(status_code=403, detail="Exam is not available.")
    return {"item": serialize_exam(exam)}
