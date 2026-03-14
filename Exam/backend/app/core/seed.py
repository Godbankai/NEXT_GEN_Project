import json
from sqlalchemy import inspect, select, text

from backend.app.core.config import settings
from backend.app.core.database import SessionLocal, engine
from backend.app.core.security import hash_password
from backend.app.models.db_models import Exam, User


AI_QUESTIONS = [
    {"id": 1, "question": "AI stands for?", "type": "mcq", "marks": 4, "options": ["Artificial Intelligence", "Automated Interface", "Applied Internet", "Analog Input"], "answer": "Artificial Intelligence"},
    {"id": 2, "question": "Which library is used for computer vision in Python?", "type": "mcq", "marks": 4, "options": ["OpenCV", "Flask", "Pandas", "SQLAlchemy"], "answer": "OpenCV"},
    {"id": 3, "question": "Face recognition is used for?", "type": "mcq", "marks": 4, "options": ["Identity verification", "Styling pages", "Database backup", "Port scanning"], "answer": "Identity verification"},
    {"id": 4, "question": "MediaPipe helps with?", "type": "mcq", "marks": 4, "options": ["Face landmarks", "Email sending", "SQL queries", "Deployment"], "answer": "Face landmarks"},
    {"id": 5, "question": "JWT is mainly used for?", "type": "mcq", "marks": 4, "options": ["Authentication", "Image editing", "Audio playback", "Video compression"], "answer": "Authentication"},
    {"id": 6, "question": "FastAPI is a?", "type": "mcq", "marks": 4, "options": ["Python web framework", "Database engine", "CSS library", "Face model"], "answer": "Python web framework"},
    {"id": 7, "question": "Which database is used in this demo project?", "type": "mcq", "marks": 4, "options": ["SQLite", "Cassandra", "Neo4j", "Redis"], "answer": "SQLite"},
    {"id": 8, "question": "Tab switching during an exam is considered?", "type": "mcq", "marks": 4, "options": ["Suspicious behavior", "Normal operation", "Database error", "Login success"], "answer": "Suspicious behavior"},
    {"id": 9, "question": "Multiple faces in the webcam frame indicate?", "type": "mcq", "marks": 4, "options": ["Possible cheating", "Better lighting", "Normal login", "Audio issue"], "answer": "Possible cheating"},
    {"id": 10, "question": "A phone near the candidate can be flagged as?", "type": "mcq", "marks": 4, "options": ["Suspicious object", "Valid ID", "System file", "Browser tab"], "answer": "Suspicious object"},
    {"id": 11, "question": "What does real-time proctoring mainly do?", "type": "mcq", "marks": 4, "options": ["Monitor suspicious activity", "Style dashboards", "Create databases", "Compile code"], "answer": "Monitor suspicious activity"},
    {"id": 12, "question": "A low-light alert means?", "type": "mcq", "marks": 4, "options": ["Camera visibility is poor", "Exam submitted", "Database locked", "Audio normal"], "answer": "Camera visibility is poor"},
    {"id": 13, "question": "Audio spikes can indicate?", "type": "mcq", "marks": 4, "options": ["Possible speaking or outside help", "Login failure", "Video crash", "No internet"], "answer": "Possible speaking or outside help"},
    {"id": 14, "question": "Which module generates PDF reports?", "type": "mcq", "marks": 4, "options": ["ReportLab", "NumPy", "Uvicorn", "bcrypt"], "answer": "ReportLab"},
    {"id": 15, "question": "What should happen after repeated cheating warnings?", "type": "mcq", "marks": 4, "options": ["Exam auto-submit", "Open more tabs", "Disable camera", "Restart laptop"], "answer": "Exam auto-submit"},
    {"id": 16, "question": "Why is fullscreen enforced during the exam?", "type": "text", "marks": 4, "answer": "to reduce cheating"},
    {"id": 17, "question": "Write one use of face recognition in online exams.", "type": "text", "marks": 4, "answer": "student authentication"},
    {"id": 18, "question": "Name one suspicious behavior detected by this system.", "type": "text", "marks": 4, "answer": "tab switch"},
    {"id": 19, "question": "Why is audio monitoring useful in proctoring?", "type": "text", "marks": 4, "answer": "detect speaking"},
    {"id": 20, "question": "Write one benefit of AI-based proctoring.", "type": "text", "marks": 4, "answer": "reduces cheating"},
    {"id": 21, "question": "What is the role of the admin dashboard?", "type": "text", "marks": 4, "answer": "monitor exams"},
    {"id": 22, "question": "Why is evidence snapshot capture important?", "type": "text", "marks": 4, "answer": "for review"},
    {"id": 23, "question": "What does head pose tracking help detect?", "type": "text", "marks": 4, "answer": "looking away"},
    {"id": 24, "question": "Why should only one face be visible during an exam?", "type": "text", "marks": 4, "answer": "prevent cheating"},
    {"id": 25, "question": "Write one advantage of support chat during an exam.", "type": "text", "marks": 4, "answer": "report issues"}
]

CV_QUESTIONS = [
    {"id": 1, "question": "Computer vision mainly deals with?", "type": "mcq", "marks": 4, "options": ["Image and video understanding", "Database indexing", "Audio editing", "Spreadsheet formulas"], "answer": "Image and video understanding"},
    {"id": 2, "question": "OpenCV is short for?", "type": "mcq", "marks": 4, "options": ["Open Source Computer Vision", "Open Cloud Video", "Object Camera Verification", "Online Code Viewer"], "answer": "Open Source Computer Vision"},
    {"id": 3, "question": "Which camera issue can affect proctoring quality?", "type": "mcq", "marks": 4, "options": ["Low light", "Strong password", "Fast CPU", "Stable internet"], "answer": "Low light"},
    {"id": 4, "question": "Head pose tracking is useful to detect?", "type": "mcq", "marks": 4, "options": ["Looking away frequently", "Database size", "Login time", "IP address"], "answer": "Looking away frequently"},
    {"id": 5, "question": "Eye movement tracking can suggest?", "type": "mcq", "marks": 4, "options": ["Attention changes", "Printer issues", "Hard disk errors", "Text formatting"], "answer": "Attention changes"},
    {"id": 6, "question": "Object detection in exams is used to find?", "type": "mcq", "marks": 4, "options": ["Phone or book", "Passwords", "PDF marks", "Mouse clicks only"], "answer": "Phone or book"},
    {"id": 7, "question": "A second person entering frame should trigger?", "type": "mcq", "marks": 4, "options": ["Suspicious alert", "Exam completion", "Chat reply", "Auto login"], "answer": "Suspicious alert"},
    {"id": 8, "question": "Webcam mirror view helps the student by?", "type": "mcq", "marks": 4, "options": ["Making preview natural", "Increasing marks", "Disabling alerts", "Stopping upload"], "answer": "Making preview natural"},
    {"id": 9, "question": "Why is session recording stored?", "type": "mcq", "marks": 4, "options": ["For later review", "To change questions", "To disable login", "To send OTP"], "answer": "For later review"},
    {"id": 10, "question": "Who can resume a blocked exam in this system?", "type": "mcq", "marks": 4, "options": ["Admin", "Any student", "Browser", "Camera"], "answer": "Admin"},
    {"id": 11, "question": "Support chat is useful for?", "type": "mcq", "marks": 4, "options": ["Reporting technical issues", "Changing admin password", "Deleting evidence", "Skipping questions"], "answer": "Reporting technical issues"},
    {"id": 12, "question": "Which event is blocked in the exam page?", "type": "mcq", "marks": 4, "options": ["Copy and paste", "Reading question", "Typing answer", "Viewing timer"], "answer": "Copy and paste"},
    {"id": 13, "question": "What does three-warning logic do?", "type": "mcq", "marks": 4, "options": ["Auto-submits exam", "Changes subject", "Resets timer", "Deletes user"], "answer": "Auto-submits exam"},
    {"id": 14, "question": "Why are join links useful?", "type": "mcq", "marks": 4, "options": ["Easy exam access", "Better camera quality", "Higher marks", "Faster database"], "answer": "Easy exam access"},
    {"id": 15, "question": "What is one goal of secure exam browsers?", "type": "mcq", "marks": 4, "options": ["Reduce cheating paths", "Increase screen size", "Change font", "Play video"], "answer": "Reduce cheating paths"},
    {"id": 16, "question": "Write one reason to record suspicious events.", "type": "text", "marks": 4, "answer": "for evidence"},
    {"id": 17, "question": "Write one use of the join code.", "type": "text", "marks": 4, "answer": "join exam"},
    {"id": 18, "question": "Why should tab switching be monitored?", "type": "text", "marks": 4, "answer": "prevent cheating"},
    {"id": 19, "question": "What can the student do if the exam locks by mistake?", "type": "text", "marks": 4, "answer": "message admin"},
    {"id": 20, "question": "Write one benefit of fullscreen mode in online exams.", "type": "text", "marks": 4, "answer": "focus on exam"},
    {"id": 21, "question": "What does face count monitoring help detect?", "type": "text", "marks": 4, "answer": "multiple faces"},
    {"id": 22, "question": "Why is webcam access necessary in this system?", "type": "text", "marks": 4, "answer": "monitor student"},
    {"id": 23, "question": "What kind of problem should be sent in support chat?", "type": "text", "marks": 4, "answer": "technical issue"},
    {"id": 24, "question": "Why is AI monitoring better than only manual monitoring?", "type": "text", "marks": 4, "answer": "automatic detection"},
    {"id": 25, "question": "Write one future improvement for this system.", "type": "text", "marks": 4, "answer": "better object detection"}
]

DEMO_EXAMS = [
    {"title": "AI Fundamentals Final Mock Test", "subject": "Artificial Intelligence", "description": "25-question, 100-mark AI mock paper with MCQ and written questions.", "duration_minutes": 45, "instructions": "Three warnings will auto-submit the exam. Use support chat if any genuine issue occurs.", "join_code": "AI-DEMO-101", "questions": AI_QUESTIONS},
    {"title": "Computer Vision and Proctoring Mock Test", "subject": "Machine Learning", "description": "25-question, 100-mark exam focused on computer vision and smart proctoring.", "duration_minutes": 45, "instructions": "Keep your face centered, avoid talking, and do not switch tabs.", "join_code": "CV-DEMO-202", "questions": CV_QUESTIONS},
]


def upgrade_schema() -> None:
    inspector = inspect(engine)
    with engine.begin() as conn:
        exam_columns = {column["name"] for column in inspector.get_columns("exams")} if inspector.has_table("exams") else set()
        if "join_code" not in exam_columns and inspector.has_table("exams"):
            conn.execute(text("ALTER TABLE exams ADD COLUMN join_code VARCHAR(64)"))
        session_columns = {column["name"] for column in inspector.get_columns("exam_sessions")} if inspector.has_table("exam_sessions") else set()
        if "warning_count" not in session_columns and inspector.has_table("exam_sessions"):
            conn.execute(text("ALTER TABLE exam_sessions ADD COLUMN warning_count INTEGER DEFAULT 0"))
        if "is_locked" not in session_columns and inspector.has_table("exam_sessions"):
            conn.execute(text("ALTER TABLE exam_sessions ADD COLUMN is_locked BOOLEAN DEFAULT 0"))
        if "lock_reason" not in session_columns and inspector.has_table("exam_sessions"):
            conn.execute(text("ALTER TABLE exam_sessions ADD COLUMN lock_reason TEXT"))


def ensure_default_admin() -> None:
    upgrade_schema()
    with SessionLocal() as db:
        admin = db.scalar(select(User).where(User.email == settings.default_admin_email))
        if not admin:
            admin = User(full_name=settings.default_admin_name, email=settings.default_admin_email, role="admin", hashed_password=hash_password(settings.default_admin_password), is_active=True)
            db.add(admin)
            db.commit()
            db.refresh(admin)

        for exam_data in DEMO_EXAMS:
            existing = db.scalar(select(Exam).where(Exam.join_code == exam_data["join_code"]))
            if existing:
                existing.title = exam_data["title"]
                existing.subject = exam_data["subject"]
                existing.description = exam_data["description"]
                existing.duration_minutes = exam_data["duration_minutes"]
                existing.instructions = exam_data["instructions"]
                existing.questions_json = json.dumps(exam_data["questions"])
                existing.status = "published"
                existing.created_by = admin.id
                db.add(existing)
            else:
                db.add(Exam(title=exam_data["title"], subject=exam_data["subject"], description=exam_data["description"], duration_minutes=exam_data["duration_minutes"], instructions=exam_data["instructions"], questions_json=json.dumps(exam_data["questions"]), status="published", join_code=exam_data["join_code"], created_by=admin.id))
        db.commit()
