# AI Based Smart Exam Monitoring and Proctoring System

Python-first MCA final year project implementation based on the provided synopsis. The project uses FastAPI for the backend, Jinja2 plus Tailwind CSS for the frontend, SQLite for demo-friendly persistence, and Python computer-vision services for smart remote proctoring.

## Project Architecture

```text
                           +-------------------------------+
                           |        Admin Dashboard        |
                           | exam setup, live view, PDF    |
                           +---------------+---------------+
                                           |
                                           v
+----------------+      HTTPS/JWT      +---+---------------------------+
| Student Browser+--------------------->  FastAPI Web Application     |
| webcam + mic   |                     | auth, exams, proctor APIs    |
| lockdown JS    |<---------------------  pages, analytics, reports   |
+--------+-------+                     +---+---------------+----------+
         |                                   |               |
         | webcam frames / events            |               |
         v                                   v               v
 +-------+-------------------+      +--------+-----+   +-----+----------------+
 | AI Proctoring Services    |      | SQLite DB    |   | File Storage         |
 | OpenCV, MediaPipe, Face   |      | users, exams,|   | snapshots, videos,   |
 | recognition, audio rules  |      | sessions     |   | generated evidence   |
 +---------------------------+      +--------------+   +----------------------+
```

## Folder Structure

```text
C:\Users\trive\Documents\Exam
|-- backend/
|   |-- app/
|   |   |-- core/
|   |   |-- models/
|   |   |-- routers/
|   |   |-- services/
|   |   |-- static/js/
|   |   `-- templates/
|-- demo_assets/
|-- docs/
|   |-- screenshots/
|   `-- VIVA_GUIDE.md
|-- storage/
|   |-- evidence/
|   `-- session_recordings/
|-- .env.example
|-- main.py
|-- README.md
`-- requirements.txt
```

## Features Implemented

- Admin and student authentication with password login and optional face verification.
- Stronger registration/login validation that rejects missing or multiple-face biometric captures.
- Stored profile image reference for student biometric onboarding.
- Admin dashboard for exam creation, analytics, live session inspection, and PDF report downloads.
- Pre-seeded sample exam for immediate viva/demo use.
- Student dashboard with published exam lobby and secure exam room.
- Real-time proctoring with face count monitoring, no-face and multiple-face alerts, eye direction and head pose estimation, low-light alerts, suspicious object candidate detection, audio anomaly monitoring, tab switch and fullscreen exit tracking.
- Evidence snapshot capture and session recording upload.
- Automatic suspicious score aggregation per session.
- PDF report generation for each student session.
- Responsive UI suitable for laptop-based demo and viva presentation.

## Installation and Setup

```bash
cd C:\Users\trive\Documents\Exam
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Demo Credentials

- Admin email: `admin@example.com`
- Admin password: `Admin@123`

## Demo Assets

- Sample questions JSON: [demo_assets/sample_questions.json](C:\Users\trive\Documents\Exam\demo_assets\sample_questions.json)
- Viva guide: [docs/VIVA_GUIDE.md](C:\Users\trive\Documents\Exam\docs\VIVA_GUIDE.md)
- Screenshot checklist: [docs/screenshots/SCREENSHOT_GUIDE.md](C:\Users\trive\Documents\Exam\docs\screenshots\SCREENSHOT_GUIDE.md)

## How To Test All Features

1. Start the app and login as admin.
2. Show the pre-seeded sample exam or create another exam from the dashboard.
3. Register a student and capture a single clear face image.
4. Login as the student and start the exam.
5. Trigger cheating scenarios:
   - move away from the camera for `no_face`
   - bring another person into frame for `multiple_faces`
   - look left or right for gaze alerts
   - turn your head away for head pose alerts
   - darken the room to trigger low-light alert
   - place a phone or notebook near the desk camera area for object candidates
   - switch tabs or exit fullscreen
   - speak loudly or play audio nearby
6. Submit the exam.
7. Return to the admin dashboard, open the session, inspect evidence, and download the report.

## Deployment

### Render

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Add environment variables from `.env.example`
- Use persistent disk for `storage/`

### Railway

- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Add the same environment variables
- Mount persistent storage if you need recordings retained

### AWS

- Run behind Nginx with HTTPS
- Use `gunicorn -k uvicorn.workers.UvicornWorker backend.app.main:app`
- Replace SQLite with PostgreSQL or MongoDB for multi-user deployment

## Viva Walkthrough

Follow [docs/VIVA_GUIDE.md](C:\Users\trive\Documents\Exam\docs\VIVA_GUIDE.md) for the speaking flow, demo order, limitations, and future scope.

## Screenshot Checklist

Follow [docs/screenshots/SCREENSHOT_GUIDE.md](C:\Users\trive\Documents\Exam\docs\screenshots\SCREENSHOT_GUIDE.md) while preparing your project report.

## Production Notes

This project is runnable locally and structured for extension. For real institutional deployment, use HTTPS, stronger anti-tamper controls, managed storage, and a production database.
