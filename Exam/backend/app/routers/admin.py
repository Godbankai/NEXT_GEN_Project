from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.database import get_db
from backend.app.models.db_models import ChatMessage, ExamSession
from backend.app.models.schemas import SessionActionRequest
from backend.app.routers.deps import require_role
from backend.app.services.exam_service import analytics_summary, session_overview
from backend.app.services.file_service import public_path
from backend.app.services.report_service import build_session_report

router = APIRouter()


@router.get("/analytics")
def analytics(_: object = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return analytics_summary(db)


@router.get("/sessions")
def sessions(_: object = Depends(require_role("admin")), db: Session = Depends(get_db)):
    items = session_overview(db)
    for item in items:
        item["latest_snapshot_path"] = public_path(item["latest_snapshot_path"])
    return {"items": items}


@router.post("/sessions/{session_id}/resume")
def resume_session(session_id: int, payload: SessionActionRequest, _: object = Depends(require_role("admin")), db: Session = Depends(get_db)):
    session = db.get(ExamSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    session.is_locked = False
    session.lock_reason = None
    session.status = "in_progress"
    session.warning_count = 0
    db.add(session)
    db.commit()
    return {"status": session.status}


@router.post("/sessions/{session_id}/stop")
def stop_session(session_id: int, payload: SessionActionRequest, _: object = Depends(require_role("admin")), db: Session = Depends(get_db)):
    session = db.get(ExamSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    session.is_locked = True
    session.status = "locked"
    session.lock_reason = payload.reason or "Session stopped by admin."
    db.add(session)
    db.commit()
    return {"status": session.status}


@router.get("/sessions/{session_id}")
def session_detail(session_id: int, _: object = Depends(require_role("admin")), db: Session = Depends(get_db)):
    session = db.scalar(
        select(ExamSession)
        .options(
            joinedload(ExamSession.student),
            joinedload(ExamSession.exam),
            joinedload(ExamSession.events),
            joinedload(ExamSession.messages).joinedload(ChatMessage.sender),
        )
        .where(ExamSession.id == session_id)
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    events = [
        {"id": event.id, "event_type": event.event_type, "severity": event.severity, "message": event.message, "evidence_path": public_path(event.evidence_path), "created_at": event.created_at.isoformat()}
        for event in sorted(session.events, key=lambda item: item.created_at, reverse=True)
    ]
    messages = [
        {"id": item.id, "sender_role": item.sender_role, "sender_name": item.sender.full_name, "message": item.message, "created_at": item.created_at.isoformat()}
        for item in sorted(session.messages, key=lambda row: row.created_at)
    ]
    return {
        "session": {
            "id": session.id,
            "student": session.student.full_name,
            "exam": session.exam.title,
            "status": session.status,
            "score": session.score,
            "suspicious_score": session.suspicious_score,
            "warning_count": session.warning_count,
            "is_locked": session.is_locked,
            "lock_reason": session.lock_reason,
            "join_code": session.exam.join_code,
            "video_path": public_path(session.session_video_path),
            "latest_snapshot_path": public_path(session.latest_snapshot_path),
        },
        "events": events,
        "messages": messages,
    }


@router.get("/reports/{session_id}.pdf")
def session_report(session_id: int, _: object = Depends(require_role("admin")), db: Session = Depends(get_db)):
    session = db.scalar(select(ExamSession).options(joinedload(ExamSession.student), joinedload(ExamSession.exam), joinedload(ExamSession.events)).where(ExamSession.id == session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    pdf = build_session_report(session)
    return StreamingResponse(iter([pdf]), media_type="application/pdf", headers={"Content-Disposition": f'inline; filename="session-{session_id}-report.pdf"'})
