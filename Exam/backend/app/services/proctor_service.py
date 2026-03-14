import json

import cv2
import numpy as np
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.db_models import ExamSession, ProctorEvent
from backend.app.services.face_service import decode_image
from backend.app.services.file_service import save_base64_file

try:
    import mediapipe as mp
except Exception:
    mp = None


CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)
FACE_MESH = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2, refine_landmarks=True) if mp else None


def _severity(points: int) -> str:
    if points >= 25:
        return "high"
    if points >= 12:
        return "medium"
    return "low"


def _estimate_gaze_and_pose(frame: np.ndarray) -> dict:
    if not FACE_MESH:
        return {"eye_direction": "unknown", "head_pose": "unknown", "attention_score": 0.65}

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = FACE_MESH.process(rgb)
    if not results.multi_face_landmarks:
        return {"eye_direction": "unknown", "head_pose": "not_detected", "attention_score": 0.0}

    landmarks = results.multi_face_landmarks[0].landmark
    left_iris = np.mean([[landmarks[i].x, landmarks[i].y] for i in [468, 469, 470, 471]], axis=0)
    right_iris = np.mean([[landmarks[i].x, landmarks[i].y] for i in [473, 474, 475, 476]], axis=0)
    nose = np.array([landmarks[1].x, landmarks[1].y])
    left_face = np.array([landmarks[234].x, landmarks[234].y])
    right_face = np.array([landmarks[454].x, landmarks[454].y])
    face_center_x = float((left_face[0] + right_face[0]) / 2)

    eye_direction = "center"
    iris_center_x = float((left_iris[0] + right_iris[0]) / 2)
    if iris_center_x < face_center_x - 0.03:
        eye_direction = "left"
    elif iris_center_x > face_center_x + 0.03:
        eye_direction = "right"

    head_pose = "center"
    if nose[0] < face_center_x - 0.04:
        head_pose = "left"
    elif nose[0] > face_center_x + 0.04:
        head_pose = "right"

    attention_score = 0.95 if eye_direction == "center" and head_pose == "center" else 0.55
    return {"eye_direction": eye_direction, "head_pose": head_pose, "attention_score": attention_score}


def _detect_object_candidates(frame: np.ndarray, face_boxes) -> list[str]:
    h, w = frame.shape[:2]
    # Only inspect the lower center desk region, not the full background.
    roi_x1 = int(w * 0.25)
    roi_x2 = int(w * 0.75)
    roi_y1 = int(h * 0.58)
    roi = frame[roi_y1:h, roi_x1:roi_x2]
    if roi.size == 0:
        return []

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred, 80, 180)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    labels: list[str] = []
    roi_h, roi_w = gray.shape
    face_bottom = 0
    if len(face_boxes):
        face_bottom = max(y + height for (_, y, _, height) in face_boxes)

    for contour in contours[:40]:
        x, y, width, height = cv2.boundingRect(contour)
        area = width * height
        if area < (roi_w * roi_h) * 0.05 or area > (roi_w * roi_h) * 0.35:
            continue
        aspect = width / max(height, 1)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        region = gray[y : y + height, x : x + width]
        brightness = float(np.mean(region)) if region.size else 0
        # Ignore bright walls, railings, and distant background shapes.
        if brightness > 150:
            continue
        absolute_y = roi_y1 + y
        if absolute_y < max(int(h * 0.62), face_bottom + 20):
            continue
        if 0.45 <= aspect <= 0.8 and len(approx) <= 6 and width > 55 and height > 85:
            labels.append("phone_candidate")
        elif aspect >= 1.2 and aspect <= 1.9 and len(approx) <= 8 and width > 130 and height > 85:
            labels.append("book_candidate")

    return sorted(set(labels))


def analyze_frame_data(data_url: str, browser_visibility: str, tab_switch_count: int) -> dict:
    frame = decode_image(data_url)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = float(np.mean(gray))
    faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(90, 90))

    alerts: list[dict] = []
    suspicious_points = 0

    face_count = len(faces)
    if face_count == 0:
        alerts.append({"event_type": "no_face", "message": "No face detected in the frame.", "points": 18})
        suspicious_points += 18
    elif face_count > 1:
        alerts.append({"event_type": "multiple_faces", "message": f"Multiple faces detected ({face_count}).", "points": 30})
        suspicious_points += 30

    if brightness < 40:
        alerts.append({"event_type": "low_light", "message": "Lighting is too low for reliable monitoring.", "points": 6})
        suspicious_points += 6

    attention = _estimate_gaze_and_pose(frame)
    if attention["eye_direction"] not in {"center", "unknown"}:
        alerts.append({"event_type": "eye_movement", "message": f"Eyes looking {attention['eye_direction']}.", "points": 8})
        suspicious_points += 8
    if attention["head_pose"] not in {"center", "unknown", "not_detected"}:
        alerts.append({"event_type": "head_pose", "message": f"Head turned {attention['head_pose']}.", "points": 10})
        suspicious_points += 10

    if browser_visibility != "visible" or tab_switch_count > 0:
        alerts.append({"event_type": "tab_switch", "message": f"Window lost focus {tab_switch_count} time(s).", "points": 22})
        suspicious_points += 22

    object_candidates = _detect_object_candidates(frame, faces)
    if object_candidates and face_count > 0:
        alerts.append({"event_type": "object_detection", "message": "Suspicious object candidate detected near desk: " + ", ".join(object_candidates), "points": 20})
        suspicious_points += 20

    return {
        "face_count": face_count,
        "alerts": alerts,
        "suspicious_points": suspicious_points,
        "eye_direction": attention["eye_direction"],
        "head_pose": attention["head_pose"],
        "attention_score": attention["attention_score"],
        "brightness": brightness,
    }


def log_alerts(db: Session, session: ExamSession, alerts: list[dict], snapshot_data: str | None = None, meta=None) -> list[ProctorEvent]:
    evidence_path = save_base64_file(snapshot_data, settings.evidence_dir, ".jpg") if snapshot_data else None
    session.latest_snapshot_path = evidence_path or session.latest_snapshot_path
    created: list[ProctorEvent] = []

    for alert in alerts:
        event = ProctorEvent(session_id=session.id, event_type=alert["event_type"], severity=_severity(alert["points"]), message=alert["message"], evidence_path=evidence_path, meta_json=json.dumps(meta or {}))
        session.suspicious_score += alert["points"]
        created.append(event)
        db.add(event)

    db.add(session)
    db.commit()
    for item in created:
        db.refresh(item)
    return created


def log_manual_event(db: Session, session: ExamSession, event_type: str, message: str, severity: str, screenshot_data: str | None, meta: dict | None) -> ProctorEvent:
    evidence_path = save_base64_file(screenshot_data, settings.evidence_dir, ".jpg") if screenshot_data else None
    if evidence_path:
        session.latest_snapshot_path = evidence_path

    points = {"low": 5, "medium": 12, "high": 20}.get(severity, 12)
    session.suspicious_score += points
    event = ProctorEvent(session_id=session.id, event_type=event_type, severity=severity, message=message, evidence_path=evidence_path, meta_json=json.dumps(meta or {}))
    db.add(event)
    db.add(session)
    db.commit()
    db.refresh(event)
    return event


def save_session_video(data_url: str) -> str:
    return save_base64_file(data_url, settings.session_recordings_dir, ".webm")
