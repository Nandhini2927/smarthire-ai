# SmartHire AI 🚀

> **AI-Powered Career Copilot** — Resume Analysis · ATS Scoring · Interview Prep · Career Roadmaps

SmartHire AI combines the power of NLP, ML, and Generative AI to give students and job seekers a complete career preparation platform — all in one place.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Analyzer** | Paste resume text → instant AI analysis, skill extraction, contact parsing |
| 🎯 **ATS Score Calculator** | 6-dimension ATS scoring with keyword gap analysis |
| 💼 **Job Role Predictor** | ML-based role matching with compatibility percentages |
| 📊 **Skill Gap Analysis** | Compare your skills vs. industry requirements |
| 🗺️ **Career Roadmap** | AI-generated personalized weekly learning plans |
| 🤖 **Interview Simulator** | Real-time AI interviewer with answer evaluation |
| ✨ **Resume Enhancer** | Transform weak bullets into ATS-optimized statements |

---

## 🚀 Quick Start

### Option 1: React Frontend (Recommended — runs in Claude.ai)
The `SmartHireAI.jsx` artifact runs directly in Claude.ai with Claude API integration built in.

### Option 2: Full Stack (Flask Backend)

#### 1. Clone & Setup
```bash
git clone https://github.com/yourname/smarthire-ai
cd smarthire-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Download NLP Models
```bash
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
```

#### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

#### 4. Run Backend
```bash
cd backend
python app.py
# Server starts at http://localhost:5000
```

#### 5. Open Frontend
Open `frontend/templates/index.html` in your browser, or serve via Flask.

---

## 🏗️ Project Structure

```
smarthire-ai/
├── backend/
│   ├── app.py                    # Flask app factory
│   ├── database/
│   │   └── db.py                 # SQLAlchemy models
│   ├── routes/
│   │   ├── resume.py             # Resume upload & analysis API
│   │   ├── interview.py          # Interview simulator API
│   │   └── roadmap_analysis.py   # Roadmap & enhancement API
│   └── utils/
│       └── nlp_utils.py          # NLP, skill extraction, ATS scoring
├── frontend/
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       └── index.html
├── SmartHireAI.jsx               # React artifact (Claude.ai)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔌 API Endpoints

### Resume
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/resume/upload` | Upload PDF/DOCX resume |
| POST | `/api/resume/text` | Analyze pasted text |
| GET  | `/api/resume/:id` | Get parsed resume |
| POST | `/api/resume/:id/analyze` | Full analysis with JD |

### Interview
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/interview/start` | Start interview session |
| POST | `/api/interview/answer` | Submit answer + get feedback |
| GET  | `/api/interview/session/:id` | Get session history |

### Roadmap & Analysis
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/roadmap/generate` | Generate career roadmap |
| POST | `/api/analysis/enhance` | Enhance resume bullets |
| POST | `/api/analysis/skills` | Detailed skill analysis |

---

## 🌐 Deployment

### Render (Free Tier)
```yaml
# render.yaml
services:
  - type: web
    name: smarthire-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd backend && gunicorn app:create_app()
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: OPENAI_API_KEY
        sync: false
```

### Railway
```bash
railway init
railway up
```

### Environment Variables
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///smarthire.db
OPENAI_API_KEY=sk-...          # Optional: for advanced AI features
ANTHROPIC_API_KEY=sk-ant-...  # Optional: for Claude integration
FLASK_DEBUG=False
PORT=5000
```

---

## 🤖 AI Integration

The platform uses a tiered AI approach:
1. **Rule-based NLP** (always free) — skill extraction, ATS scoring, role prediction
2. **Claude API** (via React artifact) — AI summaries, roadmap generation, interview Q&A
3. **OpenAI/Gemini** (optional Flask backend) — enhanced question generation, deep analysis

---

## 📊 Technical Architecture

```
User → React Frontend → Claude API (AI features)
     ↕
Flask REST API → SQLite DB
     ↓
NLP Pipeline:
  pdfplumber → text extraction
  spaCy      → entity recognition
  scikit-learn → TF-IDF skill matching
  Custom ML  → role prediction (cosine similarity)
```

---

## 🎓 Use Cases

- **Students** — Pre-placement resume audit & skill building
- **Freshers** — Interview prep and role targeting
- **Job Seekers** — ATS optimization for job applications
- **Colleges** — Placement preparation tool for TPOs
- **Hackathons** — Full-stack AI project demonstration

---

## 🛠️ Tech Stack

**Frontend:** React, CSS3 (Glassmorphism), Fetch API  
**Backend:** Python Flask, SQLAlchemy, SQLite  
**NLP/ML:** spaCy, NLTK, scikit-learn, TF-IDF, Cosine Similarity  
**AI:** Anthropic Claude API, OpenAI API (optional)  
**Deployment:** Render / Railway / Vercel compatible  

---

## 📄 License

MIT License — free to use, modify, and deploy.

---

*Built with ❤️ as an AI-powered career acceleration platform*
