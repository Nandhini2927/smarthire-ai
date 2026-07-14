SmartHire AI is a full-stack AI-powered career preparation platform that combines NLP, Machine Learning, and REST APIs to give students and job seekers a complete career toolkit — all in one place.


💡 Think of it as LinkedIn Premium + ChatGPT + ATS Checker combined into one free platform.



🎯 Problem It Solves


75% of resumes get rejected by ATS before a human ever reads them
Students don't know which skills are missing for their target role
Interview preparation is scattered across multiple platforms
No single free tool covers resume analysis + interview prep + career guidance


SmartHire AI solves all of this in one platform.


✨ Features

#FeatureDescription1📄 Resume AnalyzerUpload PDF/DOCX → extract skills, contact info, resume strength2🎯 ATS Score CalculatorScore across 6 dimensions: Skills, Education, Experience, Projects, Formatting, Keywords3💼 Job Role PredictorML cosine similarity to match skills against 9 job roles4📊 Skill Gap AnalysisCompare current skills vs industry requirements5🗺️ Career Roadmap GeneratorPersonalized week-by-week learning plan with resources6🤖 AI Interview SimulatorReal-time mock interview with answer evaluation and scoring7✨ Resume EnhancerRewrite weak bullets into ATS-optimized statements + download8📈 Score History & ChartsTrack ATS score improvement over time with Chart.js9🔗 LinkedIn Profile AnalyzerScore LinkedIn profile strength with 8-point checklist10📝 Cover Letter GeneratorAI-generated personalized cover letters with download11💼 Job ListingsMatching jobs from top companies based on predicted role


🛠️ Tech Stack

Frontend


HTML5, CSS3 (Glassmorphism dark UI), JavaScript ES6+, Chart.js


Backend


Python 3.11, Flask 3.0, Flask-SQLAlchemy, Flask-CORS


AI / NLP / ML


scikit-learn (TF-IDF + Cosine Similarity), NLTK, pdfplumber, python-docx
Custom NLP Pipeline for skill extraction and ATS scoring


Database & Deployment


SQLite, Gunicorn, Render (cloud), GitHub (CI/CD)



📁 Project Structure

smarthire-ai/
├── backend/
│   ├── app.py                    # Flask application factory
│   ├── database/
│   │   └── db.py                 # SQLAlchemy models
│   ├── routes/
│   │   ├── resume.py             # Resume upload and analysis API
│   │   ├── interview.py          # Interview simulator API
│   │   └── roadmap_analysis.py   # Roadmap and enhancement API
│   └── utils/
│       └── nlp_utils.py          # NLP pipeline and ML utilities
├── frontend/
│   └── index.html                # Complete frontend (single file)
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render deployment config
├── runtime.txt                   # Python version
└── README.md


🚀 Getting Started

Local Installation

bash# 1. Clone the repo
git clone https://github.com/Nandhini2927/smarthire-ai.git
cd smarthire-ai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -m nltk.downloader punkt stopwords

# 5. Run backend
cd backend
python app.py

# 6. Open frontend/index.html in browser


🔌 API Endpoints

MethodEndpointDescriptionPOST/api/resume/uploadUpload and parse PDF/DOCXPOST/api/resume/textAnalyze pasted resume textPOST/api/interview/startStart interview sessionPOST/api/interview/answerSubmit answer and get feedbackGET/api/interview/rolesGet interview rolesPOST/api/analysis/enhanceEnhance resume bulletsPOST/api/analysis/skillsAnalyze skillsPOST/api/roadmap/generateGenerate career roadmap


🌐 Deployment

Live on Render (Free tier):
🔗 https://smarthire-ai-0qjo.onrender.com


⚠️ Free tier spins down after inactivity. First load may take 30-50 seconds.



Deploy Your Own


Fork this repo
Go to render.com → Sign up with GitHub
New + → Web Service → Select your fork
Build Command: pip install -r requirements.txt
Start Command: cd backend && gunicorn "app:create_app()"
Click Create Web Service ✅



🎯 How It Works

User uploads PDF Resume
        ↓
pdfplumber extracts raw text
        ↓
NLP Pipeline:
  → Regex skill extraction (50+ tech skills)
  → ATS score calculation (6 dimensions)
  → Cosine similarity job role prediction
  → Skill gap analysis vs industry standards
        ↓
Flask REST API returns JSON
        ↓
Frontend renders interactive dashboard


📊 Project Stats

MetricValueFeatures11Job Roles9Tech Skills Detected50+API Endpoints10+Lines of Code3000+


🏆 Use Cases


🎓 Students — Pre-placement resume audit and skill building
👨‍💼 Freshers — Interview prep and job role targeting
🔍 Job Seekers — ATS optimization for applications
🏫 Colleges — Placement preparation tool for TPOs
🏆 Hackathons — Full-stack AI project showcase



👩‍💻 Author

Nandhini


GitHub: @Nandhini2927
Project Link: https://github.com/Nandhini2927/smarthire-ai
