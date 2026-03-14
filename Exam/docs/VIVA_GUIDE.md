# Viva Guide

## 1. Project One-Line Summary

AI Based Smart Exam Monitoring and Proctoring System is a Python-based remote examination platform that combines secure exam delivery with automated AI proctoring, live admin monitoring, evidence capture, and report generation.

## 2. Problem Statement

Traditional remote exams rely heavily on manual invigilation, which is expensive, inconsistent, and difficult to scale. This project solves that by detecting suspicious behavior automatically and presenting evidence to the administrator.

## 3. Modules To Explain In Viva

1. Authentication module
Role-based login for admin and students using password and optional facial verification.

2. Exam management module
Admin creates and publishes exams, students start sessions, answer questions, and submit online.

3. AI proctoring module
Webcam frames are analyzed for no-face, multiple-face, gaze shift, head pose, low light, suspicious object candidates, and browser tampering.

4. Monitoring and evidence module
Snapshots, events, and session recordings are stored for review.

5. Analytics and reporting module
Admin sees overall stats and downloads a PDF report for each student session.

## 4. Suggested Live Demo Flow

1. Login as admin using `admin@smartproctor.local` / `Admin@123`.
2. Show the pre-seeded sample exam in the dashboard.
3. Register a student and capture face data.
4. Login as student and start the exam.
5. Trigger cheating examples:
No face, extra face, tab switch, fullscreen exit, loud sound.
6. Submit the exam.
7. Return to admin dashboard and open session details.
8. Download the PDF report.

## 5. Important Technical Points

- Backend uses FastAPI for speed and clean API design.
- SQLite is used for simple local demo deployment.
- OpenCV handles frame operations and fallback face detection.
- MediaPipe improves gaze and head pose estimation.
- `face_recognition` is used when available for stronger biometric comparison.
- JavaScript in the browser handles fullscreen monitoring, tab switch detection, and media capture.

## 6. Limitations To Say Honestly

- Browser lockdown is simulation-based and cannot fully replace OS-level kiosk mode.
- Object detection is heuristic-based in this demo version, not a trained YOLO model.
- Audio analysis uses threshold monitoring, not full speech classification.
- For large-scale production, PostgreSQL or MongoDB and persistent cloud storage would be better.

## 7. Future Scope

- Liveness detection during face login.
- Stronger object detection using trained deep-learning weights.
- Browser extension or kiosk-mode client.
- Cloud deployment with managed database and storage.
- Human review queue with automated severity ranking.
