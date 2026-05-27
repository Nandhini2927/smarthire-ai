"""
SmartHire AI - Career Roadmap & Analysis Routes
================================================
POST /api/roadmap/generate  → Personalized career roadmap
POST /api/analysis/enhance  → AI resume bullet point enhancer
"""

from flask import Blueprint, request, jsonify

roadmap_bp  = Blueprint('roadmap',  __name__)
analysis_bp = Blueprint('analysis', __name__)

# ─── Roadmap Templates ────────────────────────────────────────────────────────

ROADMAP_DATA = {
    "Frontend Developer": {
        "phases": [
            {
                "phase": "Phase 1 — Foundations (Weeks 1–3)",
                "goals": ["Master HTML5 semantics & accessibility", "CSS Flexbox, Grid, animations", "JavaScript ES6+ fundamentals"],
                "resources": ["MDN Web Docs", "CSS-Tricks", "JavaScript.info"],
                "project": "Build a responsive portfolio website"
            },
            {
                "phase": "Phase 2 — React Ecosystem (Weeks 4–7)",
                "goals": ["React fundamentals + hooks", "State management (Zustand/Redux)", "React Router + Next.js basics"],
                "resources": ["React Docs (react.dev)", "Scrimba React Course", "Next.js Docs"],
                "project": "Build a full CRUD app with React + API"
            },
            {
                "phase": "Phase 3 — Professional Skills (Weeks 8–10)",
                "goals": ["TypeScript fundamentals", "Testing (Jest + RTL)", "CI/CD + Deployment (Vercel)"],
                "resources": ["TypeScript Handbook", "Testing Library Docs", "Vercel Docs"],
                "project": "Deploy a production-ready TypeScript React app"
            },
            {
                "phase": "Phase 4 — Job Ready (Weeks 11–12)",
                "goals": ["System design basics for frontend", "DSA for interviews (Arrays, Strings)", "Portfolio polish + LinkedIn"],
                "resources": ["Frontend Masters", "LeetCode Easy-Medium", "Blind 75"],
                "project": "3 portfolio projects + active job applications"
            }
        ]
    },
    "Data Scientist": {
        "phases": [
            {
                "phase": "Phase 1 — Python & Stats (Weeks 1–3)",
                "goals": ["Python: NumPy, Pandas, Matplotlib", "Statistics: distributions, hypothesis testing", "SQL for data extraction"],
                "resources": ["Python for Data Analysis (book)", "StatQuest YouTube", "Mode SQL Tutorial"],
                "project": "EDA on a Kaggle dataset"
            },
            {
                "phase": "Phase 2 — ML Fundamentals (Weeks 4–7)",
                "goals": ["Scikit-learn: regression, classification, clustering", "Feature engineering + cross-validation", "Model evaluation metrics"],
                "resources": ["Hands-On ML (Aurélien Géron)", "fast.ai", "Kaggle Learn"],
                "project": "Build and deploy a Kaggle competition model"
            },
            {
                "phase": "Phase 3 — Deep Learning (Weeks 8–10)",
                "goals": ["Neural networks with PyTorch/TensorFlow", "CNNs for computer vision", "NLP with Transformers/BERT"],
                "resources": ["Deep Learning Specialization (Coursera)", "HuggingFace Docs", "Papers With Code"],
                "project": "Fine-tune a BERT model on custom data"
            },
            {
                "phase": "Phase 4 — MLOps & Deployment (Weeks 11–12)",
                "goals": ["MLflow for experiment tracking", "Docker + cloud deployment", "Build an ML portfolio with case studies"],
                "resources": ["Made With ML", "AWS SageMaker Docs", "MLOps Zoomcamp"],
                "project": "End-to-end ML pipeline on AWS/GCP"
            }
        ]
    },
    "Full Stack Developer": {
        "phases": [
            {
                "phase": "Phase 1 — Frontend Core (Weeks 1–3)",
                "goals": ["HTML/CSS/JS mastery", "React + hooks", "Responsive design + UI libraries"],
                "resources": ["The Odin Project", "React Docs", "Tailwind CSS"],
                "project": "Responsive React SPA"
            },
            {
                "phase": "Phase 2 — Backend Development (Weeks 4–7)",
                "goals": ["Node.js + Express or Python/Django", "REST API design + authentication (JWT)", "PostgreSQL + MongoDB"],
                "resources": ["Node.js Docs", "Django Docs", "PostgreSQL Tutorial"],
                "project": "Full CRUD REST API with auth"
            },
            {
                "phase": "Phase 3 — Integration + DevOps (Weeks 8–10)",
                "goals": ["Full stack integration", "Docker containers", "CI/CD with GitHub Actions"],
                "resources": ["Docker Docs", "GitHub Actions Docs", "DigitalOcean Tutorials"],
                "project": "Dockerized full stack app on cloud"
            },
            {
                "phase": "Phase 4 — Production (Weeks 11–12)",
                "goals": ["System design patterns", "Performance optimization", "Security best practices"],
                "resources": ["System Design Primer (GitHub)", "OWASP Top 10", "Web.dev"],
                "project": "Production SaaS MVP"
            }
        ]
    },
    "DevOps Engineer": {
        "phases": [
            {
                "phase": "Phase 1 — Linux & Networking (Weeks 1–3)",
                "goals": ["Linux fundamentals + shell scripting", "TCP/IP, DNS, HTTP basics", "Git + version control workflows"],
                "resources": ["Linux Journey", "Networking Fundamentals (YouTube)", "Pro Git Book"],
                "project": "Automated server setup with bash scripts"
            },
            {
                "phase": "Phase 2 — Containers & Cloud (Weeks 4–7)",
                "goals": ["Docker: images, containers, compose", "Kubernetes: pods, deployments, services", "AWS/GCP fundamentals"],
                "resources": ["Docker Docs", "Kubernetes.io", "AWS Free Tier + Tutorials"],
                "project": "Containerized multi-service app on K8s"
            },
            {
                "phase": "Phase 3 — IaC & CI/CD (Weeks 8–10)",
                "goals": ["Terraform for infrastructure", "Jenkins + GitHub Actions pipelines", "Ansible for configuration management"],
                "resources": ["Terraform Docs", "Jenkins Docs", "Ansible Docs"],
                "project": "Full CI/CD pipeline for a web app"
            },
            {
                "phase": "Phase 4 — Monitoring & Reliability (Weeks 11–12)",
                "goals": ["Prometheus + Grafana monitoring", "ELK Stack for logging", "SRE concepts + incident response"],
                "resources": ["Prometheus Docs", "Grafana Labs", "Google SRE Book"],
                "project": "Observable production infrastructure"
            }
        ]
    }
}

CERTIFICATIONS = {
    "Frontend Developer": ["Meta Front-End Developer (Coursera)", "AWS Cloud Practitioner", "Google UX Design"],
    "Data Scientist": ["IBM Data Science Professional (Coursera)", "Google Advanced Data Analytics", "AWS ML Specialty"],
    "Full Stack Developer": ["Meta Back-End Developer (Coursera)", "AWS Developer Associate", "MongoDB Associate Developer"],
    "DevOps Engineer": ["AWS DevOps Engineer Professional", "Certified Kubernetes Administrator (CKA)", "HashiCorp Terraform Associate"],
    "Python Developer": ["Python Institute PCEP/PCAP", "Django Certification", "AWS Developer Associate"],
    "Data Analyst": ["Google Data Analytics (Coursera)", "Tableau Desktop Specialist", "Microsoft Power BI Data Analyst"],
}


@roadmap_bp.route('/generate', methods=['POST'])
def generate_roadmap():
    data  = request.get_json() or {}
    role  = data.get("role", "Full Stack Developer")
    level = data.get("level", "beginner")

    template = ROADMAP_DATA.get(role, ROADMAP_DATA["Full Stack Developer"])
    certs    = CERTIFICATIONS.get(role, [])

    return jsonify({
        "role":       role,
        "level":      level,
        "roadmap":    template["phases"],
        "certifications": certs,
        "practice_platforms": [
            "LeetCode — DSA practice",
            "HackerRank — Skill assessments",
            "Kaggle — Data science competitions",
            "GitHub — Open source contribution",
            "Frontend Mentor — UI challenges"
        ],
        "estimated_weeks": len(template["phases"]) * 3
    })


@roadmap_bp.route('/roles', methods=['GET'])
def roadmap_roles():
    return jsonify({"roles": list(ROADMAP_DATA.keys())})


# ─── Resume Enhancement ───────────────────────────────────────────────────────

ENHANCEMENT_TEMPLATES = [
    ("Developed", "Engineered and delivered"),
    ("Worked on", "Spearheaded development of"),
    ("Helped with", "Collaborated cross-functionally to deliver"),
    ("Made", "Architected and implemented"),
    ("Did", "Executed and optimized"),
    ("Fixed bugs", "Resolved critical production issues, reducing error rate by X%"),
    ("Used Python", "Leveraged Python to build scalable, maintainable solutions"),
    ("Wrote code", "Developed clean, documented, production-ready code"),
]

WEAK_BULLET_TIPS = [
    "Add quantifiable results (%, time saved, users, revenue impact).",
    "Start bullet points with strong action verbs: Built, Developed, Engineered.",
    "Show impact, not just activity: 'Reduced load time by 40%' vs 'Improved performance'.",
    "Include tech stack context: 'using React + Node.js' not just 'using web technologies'.",
    "Mention scale: team size, user count, data volume handled.",
]


@analysis_bp.route('/enhance', methods=['POST'])
def enhance_resume():
    """Provide enhancement suggestions for resume bullet points."""
    data  = request.get_json() or {}
    text  = data.get("text", "")
    lines = [l.strip() for l in text.split('\n') if l.strip()]

    enhanced = []
    for line in lines[:20]:  # Process up to 20 lines
        suggestion = None
        line_lower = line.lower()

        for weak, strong in ENHANCEMENT_TEMPLATES:
            if weak.lower() in line_lower:
                suggestion = line.replace(weak, strong, 1)
                break

        # Generic improvements
        if not suggestion:
            if len(line.split()) < 8:
                suggestion = f"{line} — expand with specific tools, impact, and team context."
            elif not any(c.isdigit() for c in line):
                suggestion = f"{line} — add quantifiable metric (e.g., 'improving performance by 35%')."
            else:
                suggestion = line  # Already decent

        enhanced.append({
            "original":   line,
            "enhanced":   suggestion,
            "improved":   suggestion != line
        })

    return jsonify({
        "enhanced_bullets": enhanced,
        "general_tips":     WEAK_BULLET_TIPS,
        "total_processed":  len(enhanced)
    })


@analysis_bp.route('/skills', methods=['POST'])
def analyze_skills():
    from utils.nlp_utils import extract_skills, predict_job_roles, analyze_skill_gap
    data = request.get_json() or {}
    text = data.get("text", "")
    skills_detail = extract_skills(text)
    roles         = predict_job_roles(text)
    gap           = analyze_skill_gap(text, data.get("target_role"))
    return jsonify({
        "skills_detail": skills_detail,
        "predicted_roles": roles,
        "skill_gap": gap
    })
