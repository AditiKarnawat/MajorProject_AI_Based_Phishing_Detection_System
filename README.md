# 🛡️ AI-Powered Phishing Detection System

An enterprise-grade, production-quality AI phishing detection platform engineered with a **Python FastAPI** backend, **Scikit-Learn & XGBoost ML Pipeline**, **Google Gemini AI Explanation Engine**, and a modern **Next.js & TypeScript** cybersecurity dashboard styled with **Tailwind CSS**.

---

## 🌟 Key Features

### 🔍 Multi-Vector Threat Detection
1. **URL Phishing Engine**:
   - Analyzes 16+ numerical & lexical features including Shannon domain entropy, IP address hosts, high-risk TLDs, subdomains, special character ratios, and brand squatting heuristics.
2. **Email Phishing & NLP Inspector**:
   - Evaluates social engineering urgency triggers, embedded IP links, script payloads, inline forms, and sender header spoofing anomalies.
3. **Website Content Auditor**:
   - Performs live web page inspection for cross-domain form submission targets, unencrypted HTTP password fields, hidden inputs, iframe overlays, broken anchor links, and brand impersonation.

### 🤖 Machine Learning & AI
- **Automated Model Training & Evaluation**: Auto-trains and benchmarks **Random Forest**, **XGBoost**, and **Logistic Regression** classifiers using 5-fold cross-validation. Automatically selects and persists the highest F1-score model (`.joblib`).
- **Google Gemini AI Explainer**: Generates structured executive threat summaries, key risk indicators, deep technical analysis, and actionable mitigation steps (with automated local fallback).
- **Risk & Confidence Scores**: Computes a dynamic 0–100 Risk Score and Model Confidence percentage for every scan.

### 📊 Modern Security Dashboard
- Executive KPIs: Total Scans, Threat Rate, Safe Scans, and Average Risk Score.
- Interactive Recharts Visualizations: Threat level breakdown pie charts and 7-day scan activity timeline.
- Deep Threat Diagnosis Drawer with full indicator lists and Gemini AI recommendations.
- ML Model Studio for live performance monitoring and 1-click automated model retraining.

### 🔒 Enterprise Security
- **Authentication**: JWT token authentication with Bcrypt password hashing (`/api/v1/auth/register`, `/api/v1/auth/login`).
- **SQL Injection Prevention**: Built with SQLAlchemy ORM and parameterized queries.
- **XSS & Input Validation**: Pydantic schema validation and HTML sanitization.
- **CORS & Rate Limiting**: Scoped origins and endpoint rate controls.

---

## 🏗️ Project Architecture

```
AI_Phising_Detection_System/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST Endpoint Controllers (auth, scan, history, stats, model)
│   │   ├── core/            # Config, Database setup, Bcrypt Security, Dependencies
│   │   ├── models/          # SQLAlchemy Database Models (User, ScanRecord)
│   │   ├── schemas/         # Pydantic Request/Response Models
│   │   ├── services/        # Feature Extraction, ML Trainer, Gemini Explainer, Website Auditor
│   │   └── main.py          # FastAPI Application & Lifespan Setup
│   ├── models_store/        # Saved Trained ML Model Artifacts (.joblib)
│   ├── data/                # SQLite Database File
│   ├── tests/               # Pytest Unit & Integration Test Suite
│   ├── requirements.txt     # Python Dependencies
│   └── pytest.ini           # Pytest Configuration
└── frontend/
    ├── src/
    │   ├── app/             # Next.js App Router Pages (Dashboard, Scanners, History, Model Studio, Auth)
    │   ├── components/      # UI Components (Sidebar, Navbar, RiskGauge, ThreatDrawer)
    │   ├── lib/             # API Client & Auth Helpers
    │   └── types/           # TypeScript Type Definitions
    └── package.json
```

---

## 🚀 Quick Setup & Installation

### 1. Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r requirements.txt

# (Optional) Set Google Gemini API Key in .env
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Run FastAPI backend server
uvicorn app.main:app --reload --port 8000
```
- API Documentation (Swagger UI): `http://localhost:8000/docs`
- Health Check Endpoint: `http://localhost:8000/api/v1/health`

### 2. Frontend Setup (Next.js)

```bash
cd frontend

# Install Node dependencies
npm install

# Start Next.js development server
npm run dev
```
- Frontend Dashboard: `http://localhost:3000`

---

## 🧪 Testing

Run the automated Pytest suite for backend ML extractors, authentication, and REST APIs:

```bash
cd backend
.\venv\Scripts\python -m pytest -v
```

---

## 📡 API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register a new user account |
| `POST` | `/api/v1/auth/login` | Authenticate user and issue JWT token |
| `GET` | `/api/v1/auth/me` | Retrieve authenticated user profile |
| `POST` | `/api/v1/scan/url` | Run ML & AI scan on URL input |
| `POST` | `/api/v1/scan/email` | Audit email body & raw headers for phishing |
| `POST` | `/api/v1/scan/website` | Inspect live web page DOM, forms, & SSL |
| `GET` | `/api/v1/history` | Retrieve paginated, filterable scan history |
| `GET` | `/api/v1/history/{id}` | Get detailed threat report by scan ID |
| `GET` | `/api/v1/stats/dashboard` | Fetch dashboard analytics and KPIs |
| `GET` | `/api/v1/model/status` | Get active ML model metrics & benchmark |
| `POST` | `/api/v1/model/retrain` | Trigger automated ML model retraining pipeline |

---

## 📄 License
Licensed under the MIT License.
