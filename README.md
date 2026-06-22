# 🎓 Smart Exam Monitoring System

<div align="center">

![Smart Exam Monitoring](https://img.shields.io/badge/Smart%20Exam-Monitoring%20System-blue?style=for-the-badge&logo=graduation-cap)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)

**AI-powered proctoring system for fair and secure online examinations**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 📌 Overview

**Smart Exam Monitoring System** ek advanced AI-based proctoring solution hai jo online examinations ko fair, secure aur transparent banata hai. Yeh system real-time face detection, eye tracking, aur suspicious behavior analysis ke through cheating ko detect karta hai aur automatically flag karta hai.

> Designed for educational institutions, universities, and online learning platforms.

---

## ✨ Features

### 🔍 Real-Time Monitoring
- **Face Detection** – Exam ke dauran student ka face continuously track karta hai
- **Eye Tracking** – Gaze direction monitor karta hai (screen se bahar dekhna detect hota hai)
- **Multiple Face Alert** – Agar frame mein ek se zyada face aaye to alert trigger hota hai
- **Face Absence Alert** – Student camera se hat jaaye to warning deta hai

### 🤖 AI-Powered Analysis
- **Head Pose Estimation** – Head movement track karta hai (left/right/up/down)
- **Mouth Movement Detection** – Whispering ya baat karne ki activity detect karta hai
- **Suspicious Behavior Flagging** – Unusual patterns ko automatically flag karta hai
- **Confidence Score** – Har violation ka confidence score generate karta hai

### 📊 Reports & Logs
- **Automated Report Generation** – Exam ke baad detailed PDF/Excel report
- **Violation Timeline** – Har suspicious activity ka timestamp ke saath record
- **Screenshot Capture** – Violation ke waqt automatic screenshot
- **Analytics Dashboard** – Admin ke liye visual analytics

### 🔐 Security
- **Secure Login System** – Role-based access (Admin / Examiner / Student)
- **Session Management** – Secure exam sessions with token-based auth
- **Data Encryption** – Student data fully encrypted
- **Audit Logs** – Tamper-proof activity logs

### 🌐 Platform Support
- Web Browser (Chrome, Firefox, Edge)
- Desktop Application (Windows, macOS, Linux)
- Mobile Responsive Interface

---

## 📸 Demo

```
┌─────────────────────────────────────────────────────┐
│           SMART EXAM MONITORING SYSTEM              │
├──────────────────┬──────────────────────────────────┤
│  📷 Live Feed    │  📋 Exam Interface               │
│                  │                                  │
│  [Student Face]  │  Q1. What is ...?               │
│                  │  ○ Option A                      │
│  ✅ Face: OK     │  ○ Option B                      │
│  ✅ Eyes: OK     │  ○ Option C                      │
│  ⚠️ Head: Left   │  ○ Option D                      │
│                  │                                  │
├──────────────────┴──────────────────────────────────┤
│  🚨 Alert: Head turned left for 3 seconds           │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | React.js / HTML5 / CSS3 / Bootstrap |
| **Backend** | Python (Flask / Django) |
| **Computer Vision** | OpenCV, MediaPipe, Dlib |
| **AI/ML** | TensorFlow / PyTorch / scikit-learn |
| **Database** | PostgreSQL / MongoDB |
| **Real-time** | WebSocket / Socket.IO |
| **Authentication** | JWT / OAuth 2.0 |
| **Deployment** | Docker / AWS / Heroku |

---

## 📁 Project Structure

```
smart-exam-monitoring-system/
│
├── 📂 backend/
│   ├── 📂 api/                  # REST API endpoints
│   ├── 📂 models/               # Database models
│   ├── 📂 services/
│   │   ├── face_detection.py    # Face detection service
│   │   ├── eye_tracking.py      # Eye tracking module
│   │   ├── behavior_analysis.py # AI behavior analysis
│   │   └── report_generator.py  # Report generation
│   ├── 📂 utils/                # Helper utilities
│   └── app.py                   # Main application
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/       # React components
│   │   ├── 📂 pages/            # Page views
│   │   └── 📂 services/         # API services
│   └── public/
│
├── 📂 ml_models/                # Trained AI models
│   ├── face_model.h5
│   ├── gaze_model.pkl
│   └── behavior_model.pt
│
├── 📂 tests/                    # Unit & integration tests
├── 📂 docs/                     # Documentation
├── 📂 docker/                   # Docker config files
│
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── package.json                 # Node dependencies
├── docker-compose.yml           # Docker compose config
└── README.md                    # You are here!
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 ya usse upar
- Node.js 14+
- Webcam / Camera access
- Git

### Step 1: Repository Clone Karein

```bash
git clone https://github.com/yourusername/smart-exam-monitoring-system.git
cd smart-exam-monitoring-system
```

### Step 2: Python Environment Setup

```bash
# Virtual environment banayein
python -m venv venv

# Activate karein (Windows)
venv\Scripts\activate

# Activate karein (macOS/Linux)
source venv/bin/activate

# Dependencies install karein
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
cd frontend
npm install
npm run build
```

### Step 4: Environment Variables Configure Karein

```bash
cp .env.example .env
```

`.env` file mein apni settings daalen:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/exam_db

# Secret Keys
SECRET_KEY=your-super-secret-key
JWT_SECRET=your-jwt-secret

# Camera Settings
CAMERA_INDEX=0
FRAME_RATE=30

# Alert Thresholds
FACE_ABSENCE_THRESHOLD=3    # seconds
GAZE_DEVIATION_THRESHOLD=2  # seconds
```

### Step 5: Database Setup

```bash
python manage.py migrate
python manage.py create_superuser
```

### Step 6: Application Start Karein

```bash
# Backend start
python app.py

# Frontend (development mode)
cd frontend && npm start
```

Application `http://localhost:3000` par available hogi.

---

## 🚀 Usage

### Admin Panel

```
URL: http://localhost:3000/admin
Default Login:
  Username: admin
  Password: admin123 (pehli login par zaroor badlein!)
```

**Admin Dashboard Features:**
- Exam create aur manage karein
- Students enroll karein
- Live monitoring dashboard
- Reports download karein

### Exam Monitor

1. Student login karega apne credentials se
2. Camera permission grant karni hogi
3. System face verification karega
4. Exam shuru hogi with continuous monitoring
5. Violations automatically log honge

### API Endpoints

```http
POST   /api/auth/login          # Login
POST   /api/auth/logout         # Logout
GET    /api/exams               # Exams list
POST   /api/exams/create        # Exam create
GET    /api/exams/{id}/monitor  # Live monitoring
GET    /api/reports/{id}        # Report download
POST   /api/violations/log      # Violation log
```

---

## 📊 Monitoring Violations

| Violation Type | Trigger Condition | Severity |
|---------------|-------------------|----------|
| Face Not Found | > 3 seconds | 🔴 High |
| Multiple Faces | Any detection | 🔴 High |
| Gaze Away | > 2 seconds | 🟡 Medium |
| Head Turned | > 3 seconds | 🟡 Medium |
| Mouth Moving | Sustained motion | 🟢 Low |
| Tab Switched | Browser focus lost | 🔴 High |

---

## 🔧 Configuration

`config.yaml` file se system ko customize karein:

```yaml
monitoring:
  face_detection_confidence: 0.8
  eye_tracking_sensitivity: 0.7
  alert_cooldown_seconds: 5
  max_violations_before_suspend: 10

exam_settings:
  allow_calculator: false
  allow_notepad: false
  full_screen_required: true
  random_question_order: true

reports:
  auto_generate: true
  include_screenshots: true
  format: pdf  # pdf / excel / both
```

---

## 🧪 Tests Run Karein

```bash
# All tests
pytest tests/

# Specific module test
pytest tests/test_face_detection.py

# Coverage report
pytest --cov=backend tests/
```

---

## 🐳 Docker se Deploy Karein

```bash
# Build aur start all services
docker-compose up --build

# Background mein run karein
docker-compose up -d

# Logs dekhein
docker-compose logs -f
```

---

## 🤝 Contributing

Contributions bilkul welcome hain! Please follow these steps:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/smart-exam-monitoring-system.git`
3. **Branch** banayein: `git checkout -b feature/AmazingFeature`
4. **Changes** commit karein: `git commit -m 'Add some AmazingFeature'`
5. **Push** karein: `git push origin feature/AmazingFeature`
6. **Pull Request** open karein

### Contribution Guidelines

- Code mein comments zaroor daalen (Hinglish ya English)
- Tests likhein apne changes ke liye
- README update karein agar zaroorat ho
- Existing code style follow karein

---

## 🐛 Issues & Bug Reports

Koi bug mila? [Issue report karein](https://github.com/yourusername/smart-exam-monitoring-system/issues)

Please include karein:
- Bug ka description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (agar ho sakein)
- System information (OS, Python version, etc.)

---

## 📄 License

Yeh project **MIT License** ke under available hai. Details ke liye [LICENSE](LICENSE) file dekhein.

---

## 👨‍💻 Author

**Aysuh Trivedi **
- GitHub: (https://github.com/Godbankai))
- LinkedIn: (in/ayush-trivedi-powyan)
- Email: trivediayushpwn@gmail.com

---

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) – Computer vision library
- [MediaPipe](https://mediapipe.dev/) – Face mesh aur pose detection
- [TensorFlow](https://tensorflow.org/) – Machine learning framework
- [React.js](https://reactjs.org/) – Frontend framework
- Sab contributors aur testers ka shukriya! ❤️

---

## ⭐ Support

Agar yeh project aapke kaam aaya, toh please **Star** zaroor karein! ⭐

```
"Education ke liye technology, cheating ke khilaf ek kadam" 🎓
```

---

<div align="center">
Made with ❤️ for fair education
</div>
