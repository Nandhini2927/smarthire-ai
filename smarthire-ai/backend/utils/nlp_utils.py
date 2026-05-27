"""
SmartHire AI - NLP & Resume Processing Utilities
==================================================
Handles resume text extraction, skill detection,
ATS scoring, job role prediction via ML/NLP.

Libraries: spaCy, NLTK, scikit-learn, pdfplumber, python-docx
"""

import re
import json
import math
from collections import Counter

# ─── Skill Taxonomy ───────────────────────────────────────────────────────────

TECH_SKILLS = {
    "languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "kotlin", "swift", "ruby", "php", "scala", "r", "matlab", "perl", "bash",
        "shell", "sql", "html", "css", "sass", "less"
    ],
    "frameworks": [
        "react", "angular", "vue", "next.js", "nuxt", "django", "flask", "fastapi",
        "spring", "express", "node.js", "laravel", "rails", "asp.net", "tensorflow",
        "pytorch", "keras", "scikit-learn", "pandas", "numpy", "opencv", "huggingface"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "cassandra",
        "elasticsearch", "dynamodb", "firebase", "supabase", "neo4j"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "github actions",
        "terraform", "ansible", "ci/cd", "linux", "nginx", "apache"
    ],
    "tools": [
        "git", "github", "gitlab", "jira", "confluence", "postman", "figma",
        "tableau", "power bi", "excel", "spark", "hadoop", "airflow", "kafka"
    ],
    "ai_ml": [
        "machine learning", "deep learning", "nlp", "computer vision", "data science",
        "neural networks", "transformers", "bert", "gpt", "llm", "rag",
        "reinforcement learning", "feature engineering", "model deployment"
    ]
}

SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
    "time management", "project management", "agile", "scrum", "collaboration",
    "analytical", "creative", "adaptable", "detail-oriented", "self-motivated"
]

JOB_ROLE_SKILLS = {
    "Frontend Developer": ["react", "vue", "angular", "html", "css", "javascript", "typescript", "next.js", "figma"],
    "Backend Developer": ["python", "java", "node.js", "django", "flask", "spring", "postgresql", "mysql", "rest api"],
    "Full Stack Developer": ["react", "node.js", "python", "javascript", "mongodb", "postgresql", "docker", "git"],
    "Data Analyst": ["python", "sql", "pandas", "tableau", "power bi", "excel", "statistics", "r", "numpy"],
    "Data Scientist": ["python", "machine learning", "deep learning", "pandas", "scikit-learn", "tensorflow", "statistics", "nlp"],
    "AI/ML Engineer": ["python", "tensorflow", "pytorch", "deep learning", "machine learning", "nlp", "transformers", "mlops"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "ci/cd", "terraform", "linux", "jenkins", "ansible"],
    "Cloud Engineer": ["aws", "azure", "gcp", "terraform", "kubernetes", "docker", "cloud architecture"],
    "Python Developer": ["python", "django", "flask", "fastapi", "pandas", "sqlalchemy", "rest api", "celery"],
    "Mobile Developer": ["react native", "flutter", "swift", "kotlin", "ios", "android", "mobile"],
    "Cybersecurity Analyst": ["networking", "linux", "penetration testing", "siem", "firewalls", "encryption", "risk assessment"],
    "Database Administrator": ["sql", "postgresql", "mysql", "oracle", "mongodb", "database design", "query optimization"]
}

INDUSTRY_SKILL_REQUIREMENTS = {
    "Software Engineering": ["data structures", "algorithms", "system design", "git", "testing", "agile"],
    "Data Science": ["statistics", "python", "sql", "machine learning", "data visualization", "big data"],
    "Web Development": ["html", "css", "javascript", "responsive design", "web security", "performance"],
    "Cloud/DevOps": ["linux", "networking", "docker", "cloud platforms", "monitoring", "automation"],
}

# ─── Resume Text Extraction ────────────────────────────────────────────────────

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using pdfplumber."""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except ImportError:
        # Fallback: PyPDF2
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"[Error extracting PDF: {e}]"
    except Exception as e:
        return f"[Error: {e}]"


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        from docx import Document
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    except ImportError:
        return "[python-docx not installed. Run: pip install python-docx]"
    except Exception as e:
        return f"[Error: {e}]"


def extract_resume_text(file_path: str, filename: str) -> str:
    """Route to correct extractor based on file extension."""
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ('docx', 'doc'):
        return extract_text_from_docx(file_path)
    else:
        with open(file_path, 'r', errors='ignore') as f:
            return f.read()

# ─── Skill Extraction ─────────────────────────────────────────────────────────

def extract_skills(text: str) -> dict:
    """Extract technical and soft skills from resume text."""
    text_lower = text.lower()
    found = {"technical": {}, "soft": []}

    for category, skills in TECH_SKILLS.items():
        matched = [s for s in skills if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
        if matched:
            found["technical"][category] = matched

    found["soft"] = [s for s in SOFT_SKILLS if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
    return found


def extract_all_skills_flat(text: str) -> list:
    """Return a flat list of all detected skills."""
    skills_dict = extract_skills(text)
    flat = []
    for cat_skills in skills_dict["technical"].values():
        flat.extend(cat_skills)
    flat.extend(skills_dict["soft"])
    return list(set(flat))

# ─── ATS Scoring ──────────────────────────────────────────────────────────────

def calculate_ats_score(text: str, job_description: str = "") -> dict:
    """
    Compute ATS score across 6 dimensions.
    Returns scores (0-100) per category + overall.
    """
    text_lower = text.lower()
    
    # 1. Skills score
    all_skills = extract_all_skills_flat(text)
    skill_score = min(100, len(all_skills) * 4)

    # 2. Education score
    edu_keywords = ["bachelor", "master", "phd", "b.tech", "b.e", "m.tech", "degree",
                    "university", "college", "gpa", "cgpa", "graduation"]
    edu_hits = sum(1 for kw in edu_keywords if kw in text_lower)
    edu_score = min(100, edu_hits * 15)

    # 3. Experience score
    exp_keywords = ["experience", "worked", "developed", "built", "designed", "managed",
                    "led", "implemented", "years", "internship", "project"]
    exp_hits = sum(1 for kw in exp_keywords if kw in text_lower)
    exp_score = min(100, exp_hits * 9)

    # 4. Projects score
    proj_keywords = ["project", "github", "deployed", "repository", "application",
                     "system", "platform", "tool", "api", "website"]
    proj_hits = sum(1 for kw in proj_keywords if kw in text_lower)
    proj_score = min(100, proj_hits * 10)

    # 5. Formatting score (length, sections)
    sections = ["experience", "education", "skills", "projects", "summary", "contact"]
    sec_hits = sum(1 for s in sections if s in text_lower)
    word_count = len(text.split())
    fmt_score = min(100, sec_hits * 12 + min(40, word_count // 15))

    # 6. JD Keyword match (if JD provided)
    if job_description:
        jd_words = set(re.findall(r'\b\w{4,}\b', job_description.lower()))
        resume_words = set(re.findall(r'\b\w{4,}\b', text_lower))
        match_ratio = len(jd_words & resume_words) / max(len(jd_words), 1)
        kw_score = min(100, int(match_ratio * 200))
    else:
        kw_score = skill_score  # fallback

    overall = round((skill_score + edu_score + exp_score + proj_score + fmt_score + kw_score) / 6)

    return {
        "overall": overall,
        "categories": {
            "Skills": skill_score,
            "Education": edu_score,
            "Experience": exp_score,
            "Projects": proj_score,
            "Formatting": fmt_score,
            "Keywords": kw_score
        }
    }

# ─── Job Role Prediction ──────────────────────────────────────────────────────

def predict_job_roles(text: str) -> list:
    """
    Predict top matching job roles using TF-IDF-inspired skill cosine similarity.
    Returns list of {role, score, match_percent, matching_skills, missing_skills}.
    """
    user_skills = set(extract_all_skills_flat(text))
    if not user_skills:
        return []

    scores = []
    for role, req_skills in JOB_ROLE_SKILLS.items():
        req_set = set(req_skills)
        matching = user_skills & req_set
        missing  = req_set - user_skills
        
        # Cosine-like similarity
        score = len(matching) / math.sqrt(len(user_skills) * len(req_set)) if user_skills and req_set else 0
        pct   = round(len(matching) / len(req_set) * 100)
        
        scores.append({
            "role": role,
            "score": round(score, 3),
            "match_percent": pct,
            "matching_skills": list(matching),
            "missing_skills": list(missing)[:5]
        })

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:5]

# ─── Skill Gap Analysis ───────────────────────────────────────────────────────

def analyze_skill_gap(text: str, target_role: str = None) -> dict:
    """Compare user skills against industry standards for the target role."""
    user_skills = set(extract_all_skills_flat(text))

    if target_role and target_role in JOB_ROLE_SKILLS:
        required = set(JOB_ROLE_SKILLS[target_role])
        domain = target_role
    else:
        # Use top predicted role
        predictions = predict_job_roles(text)
        if predictions:
            top = predictions[0]
            required = set(JOB_ROLE_SKILLS.get(top["role"], []))
            domain = top["role"]
        else:
            required = set()
            domain = "General Software Engineering"

    present  = user_skills & required
    missing  = required - user_skills
    extra    = user_skills - required

    return {
        "domain": domain,
        "user_skills": list(user_skills),
        "required_skills": list(required),
        "present_skills": list(present),
        "missing_skills": list(missing),
        "extra_skills": list(extra),
        "readiness_score": round(len(present) / max(len(required), 1) * 100)
    }

# ─── Contact & Section Extraction ────────────────────────────────────────────

def extract_contact_info(text: str) -> dict:
    """Extract email, phone, LinkedIn, GitHub from resume text."""
    email   = re.search(r'\b[\w.+-]+@[\w-]+\.\w+\b', text)
    phone   = re.search(r'(\+?\d[\d\s\-().]{7,15})', text)
    linkedin = re.search(r'linkedin\.com/in/[\w-]+', text, re.I)
    github  = re.search(r'github\.com/[\w-]+', text, re.I)
    return {
        "email":    email.group()    if email    else None,
        "phone":    phone.group()    if phone    else None,
        "linkedin": linkedin.group() if linkedin else None,
        "github":   github.group()   if github   else None,
    }
