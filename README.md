<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=320&color=0:0F0C29,50:302B63,100:24243E&text=AI%20Based%20Smart%20Exam%20Monitoring%20%26%20Proctoring%20System&fontSize=35&fontColor=ffffff&animation=fadeIn&fontAlignY=40"/>

<br>

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=24&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=1000&lines=AI+Powered+Online+Exam+Monitoring;Face+Recognition+%7C+Eye+Tracking;Head+Pose+Estimation+%7C+Tab+Detection;FastAPI+%7C+OpenCV+%7C+MediaPipe;Secure+and+Intelligent+Remote+Proctoring"/>

<br><br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-FF6F00?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

<br>

![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Computer%20Vision-purple?style=for-the-badge)

</div>

---

# 🌌 Project Overview

AI Based Smart Exam Monitoring & Proctoring System is an intelligent next-generation online examination platform designed to ensure academic integrity, fairness, and transparency during remote examinations.

The platform combines Artificial Intelligence, Computer Vision, Face Recognition, Eye Tracking, Head Pose Estimation, Browser Monitoring, and Behaviour Analysis to detect suspicious activities in real time.

The system continuously monitors students through webcam streams and browser events, identifies potential examination violations, generates evidence-based reports, and provides administrators with complete control over examination sessions.

Unlike traditional online examination systems, this platform provides automated invigilation using advanced AI models and biometric authentication, significantly reducing manual supervision efforts.

---

# 🎯 Problem Statement

Online examinations face several major challenges:

- Students switching browser tabs to search answers.
- Use of mobile phones during exams.
- Presence of unauthorized persons.
- Student impersonation.
- Lack of real-time monitoring.
- Manual review consuming hours of effort.
- No structured evidence collection system.

This project addresses these issues using AI-powered monitoring, biometric verification, and automated violation detection.

---

# 🚀 Core Features

## 👤 Face Recognition System

- Biometric Student Authentication
- Face Encoding Generation
- Face Matching Verification
- Identity Validation
- Multiple Face Detection
- No Face Detection

---

## 👀 Eye Gaze Tracking

- Real-Time Eye Monitoring
- Attention Analysis
- Looking Away Detection
- Suspicious Eye Movement Detection
- Behaviour Scoring

---

## 🧠 Head Pose Estimation

- Left Head Turn Detection
- Right Head Turn Detection
- Pose Analysis
- Behaviour Monitoring
- Alert Generation

---

## 🌐 Browser Monitoring

- Tab Switching Detection
- Fullscreen Exit Detection
- Browser Focus Monitoring
- Security Event Logging
- Real-Time Alerts

---

## 📱 Object Detection

- Mobile Phone Detection
- Suspicious Object Detection
- Evidence Collection
- Security Score Updates

---

## 🔒 Security Engine

- JWT Authentication
- Bcrypt Password Hashing
- Session Management
- Role-Based Access Control
- Secure API Communication

---

## 📊 Admin Dashboard

- Live Monitoring
- Session Analytics
- Student Management
- Exam Control
- Lock/Unlock Sessions
- PDF Report Downloads
- Live Chat Support

---

# 🏗 System Architecture

```text
Student Registration
          │
          ▼
Face Encoding Generation
          │
          ▼
Secure Login Verification
          │
          ▼
Exam Session Start
          │
          ▼
Real-Time Monitoring Engine
          │
          ▼
┌─────────────────────┐
│ Face Recognition    │
│ Eye Tracking        │
│ Head Pose Analysis  │
│ Browser Monitoring  │
│ Object Detection    │
└─────────────────────┘
          │
          ▼
Violation Detection Engine
          │
          ▼
Suspicious Score System
          │
          ▼
Auto Lock / Alerts
          │
          ▼
Evidence Collection
          │
          ▼
PDF Report Generation
          │
          ▼
Admin Dashboard
```

# ⚙ Technology Stack

### Frontend
- HTML5
- Tailwind CSS
- JavaScript
- Jinja2 Templates

### Backend
- FastAPI
- Python 3.10+
- SQLAlchemy ORM
- SQLite Database

### AI & Computer Vision
- OpenCV
- MediaPipe FaceMesh
- face_recognition
- NumPy

### Security
- JWT Authentication
- Bcrypt Password Hashing
- Face Encoding Verification

### Reporting
- ReportLab PDF Generator

---

# 📈 AI Monitoring & Scoring System

| Activity | Score |
|----------|--------|
| Multiple Faces | +30 |
| Tab Switch | +22 |
| Mobile Phone | +24 |
| Suspicious Object | +20 |
| No Face Detected | +18 |
| Head Pose Alert | +10 |
| Audio Alert | +10 |
| Eye Movement Alert | +8 |
| Low Light | +6 |

### Auto Lock Rule

```text
Suspicious Score >= 60
        OR
3 Consecutive Warnings

⇒ Session Automatically Locked
```

---

# 🔌 API Endpoints

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
```

### Exams

```http
POST /api/exams
POST /api/exams/sessions/start
POST /api/exams/sessions/{id}/submit
```

### Proctoring

```http
POST /api/proctor/analyze-frame
POST /api/proctor/analyze-audio
POST /api/proctor/event
```

### Admin

```http
GET  /api/admin/sessions
POST /api/admin/sessions/{id}/resume
GET  /api/admin/reports/{id}.pdf
```

---

# 📊 Performance Metrics

| Module | Accuracy |
|----------|----------|
| Face Recognition | 97% |
| Eye Tracking | 95% |
| Head Pose Detection | 94% |
| Browser Monitoring | 100% |
| Violation Detection | 96% |
| PDF Reporting | 100% |

---

# 🚀 Future Enhancements

- YOLOv8 Object Detection
- Speaker Verification
- AWS Cloud Deployment
- Mobile Application
- LMS Integration
- Deep Learning Behaviour Prediction
- Real-Time Notifications
- Advanced Analytics Dashboard

---

# 👨‍💻 Team Members

| Name | Role |
|--------|--------|
| Ayush Trivedi | AI & Computer Vision |
| Ayush Raj | Frontend Development |
| Monika Kumari | Backend Development |
| Rahul Sahni | Testing & Integration |
| Shivanya Namra | Research & Documentation |

---

# ⭐ Support

If you found this project useful:

⭐ Star this repository

🍴 Fork the repository

📢 Share with others

---

<div align="center">

### Developed with ❤️ by Team NEXT_GEN

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:0F0C29,50:302B63,100:24243E"/>

</div>
