from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.database import get_db
from backend.app.models.db_models import ExamSession
from backend.app.models.schemas import AudioAnalysisRequest, EventLogRequest, FrameAnalysisRequest, VideoUploadRequest
from backend.app.routers.deps import require_role
from backend.app.services.proctor_service import analyze_frame_data, log_alerts, log_manual_event, save_session_video

router = APIRouter()
LOCK_THRESHOLD = 60


def _student_session(db: Session, session_id: int, student_id: int) -> ExamSession:
    session = db.scalar(select(ExamSession).options(joinedload(ExamSession.exam)).where(ExamSession.id == session_id, ExamSession.student_id == student_id))
    if not session:
        raise HTTPException(status_code=404, detail="Exam session not found.")
    return session


def _maybe_lock_session(db: Session, session: ExamSession, reason: str | None = None) -> ExamSession:
    if session.suspicious_score >= LOCK_THRESHOLD or session.warning_count >= 3:
        session.is_locked = True
        session.status = "locked"
        session.lock_reason = reason or "Three warnings reached. Exam is being auto-submitted due to repeated cheating alerts."
        db.add(session)
        db.commit()
        db.refresh(session)
    return session


@router.post("/analyze-frame")
def analyze_frame(payload: FrameAnalysisRequest, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    session = _student_session(db, payload.session_id, student.id)
    if session.is_locked:
        return {"session_locked": True, "lock_reason": session.lock_reason, "alerts": []}

    analysis = analyze_frame_data(payload.frame_data, payload.browser_visibility, payload.tab_switch_count)
    if analysis["alerts"]:
        log_alerts(db, session, analysis["alerts"], snapshot_data=payload.frame_data, meta={"eye_direction": analysis["eye_direction"], "head_pose": analysis["head_pose"], "active_app": payload.active_app})
        session = db.get(ExamSession, session.id)
        session.warning_count += 1
        db.add(session)
        db.commit()
        db.refresh(session)
        session = _maybe_lock_session(db, session)

    return {
        "face_count": analysis.get("face_count", 0),
        "eye_direction": analysis.get("eye_direction"),
        "head_pose": analysis.get("head_pose"),
        "attention_score": analysis.get("attention_score"),
        "suspicious_points": analysis.get("suspicious_points", 0),
        "alerts": analysis.get("alerts", []),
        "session_locked": session.is_locked,
        "lock_reason": session.lock_reason,
    }


@router.post("/analyze-audio")
def analyze_audio(payload: AudioAnalysisRequest, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    session = _student_session(db, payload.session_id, student.id)
    if session.is_locked:
        return {"session_locked": True, "lock_reason": session.lock_reason, "alerts": []}
    alerts = []
    if payload.level > 0.18 or payload.speaking_detected:
        alerts.append({"event_type": "audio_alert", "message": f"Suspicious sound level detected ({payload.level:.2f}).", "points": 10})
        log_alerts(db, session, alerts, meta={"level": payload.level})
        session = db.get(ExamSession, session.id)
        session.warning_count += 1
        db.add(session)
        db.commit()
        db.refresh(session)
        session = _maybe_lock_session(db, session)
    return {"alerts": alerts, "session_locked": session.is_locked, "lock_reason": session.lock_reason}


@router.post("/event")
def log_event(payload: EventLogRequest, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    session = _student_session(db, payload.session_id, student.id)
    event = log_manual_event(db, session, payload.event_type, payload.message, payload.severity, payload.screenshot_data, payload.meta)
    session = db.get(ExamSession, session.id)
    if payload.severity in {"medium", "high"}:
        session.warning_count += 1
        db.add(session)
        db.commit()
        db.refresh(session)
        session = _maybe_lock_session(db, session, "Exam locked because suspicious browser activity was detected repeatedly.")
    return {"event_id": event.id, "severity": event.severity, "session_locked": session.is_locked, "lock_reason": session.lock_reason}


@router.post("/upload-session-video")
def upload_session_video(payload: VideoUploadRequest, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    session = _student_session(db, payload.session_id, student.id)
    video_path = save_session_video(payload.video_data)
    session.session_video_path = video_path
    db.add(session)
    db.commit()
    return {"video_path": video_path}
