"""
SmartHire AI - Resume API Routes
==================================
POST /api/resume/upload        → Upload + parse resume
GET  /api/resume/<id>          → Get resume details
POST /api/resume/<id>/analyze  → Run full analysis
POST /api/resume/<id>/enhance  → AI resume enhancement
"""

from flask import Blueprint, request, jsonify, current_app
import os, json, uuid
from werkzeug.utils import secure_filename
from database.db import db, Resume, Analysis
from utils.nlp_utils import (
    extract_resume_text, extract_skills, extract_all_skills_flat,
    calculate_ats_score, predict_job_roles, analyze_skill_gap,
    extract_contact_info
)

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and parse a resume file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Use PDF or DOCX."}), 400

    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    # Extract & analyse
    raw_text = extract_resume_text(file_path, file.filename)
    skills   = extract_all_skills_flat(raw_text)
    ats      = calculate_ats_score(raw_text)
    roles    = predict_job_roles(raw_text)
    contact  = extract_contact_info(raw_text)

    resume = Resume(
        filename        = file.filename,
        raw_text        = raw_text,
        extracted_skills= json.dumps(skills),
        ats_score       = ats["overall"],
        job_roles       = json.dumps([r["role"] for r in roles])
    )
    db.session.add(resume)
    db.session.commit()

    return jsonify({
        "resume_id":       resume.id,
        "filename":        resume.filename,
        "raw_text_length": len(raw_text),
        "skills":          skills,
        "contact":         contact,
        "ats_score":       ats,
        "predicted_roles": roles,
        "message":         "Resume parsed successfully"
    }), 201


@resume_bp.route('/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    return jsonify(resume.to_dict())


@resume_bp.route('/<int:resume_id>/analyze', methods=['POST'])
def analyze_resume(resume_id):
    """Full analysis: ATS + skill gap + job roles against a JD."""
    resume = Resume.query.get_or_404(resume_id)
    data   = request.get_json() or {}
    jd     = data.get("job_description", "")
    target = data.get("target_role")

    ats_result = calculate_ats_score(resume.raw_text, jd)
    gap_result = analyze_skill_gap(resume.raw_text, target)
    roles      = predict_job_roles(resume.raw_text)

    # Missing JD keywords
    missing_keywords = []
    if jd:
        import re
        jd_kws = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd.lower()))
        resume_kws = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume.raw_text.lower()))
        missing_keywords = list(jd_kws - resume_kws)[:20]

    result = {
        "ats": ats_result,
        "skill_gap": gap_result,
        "predicted_roles": roles,
        "missing_keywords": missing_keywords
    }

    analysis = Analysis(
        resume_id       = resume_id,
        analysis_type   = 'full',
        result_data     = json.dumps(result),
        job_description = jd
    )
    db.session.add(analysis)
    db.session.commit()

    return jsonify(result)


@resume_bp.route('/text', methods=['POST'])
def analyze_text():
    """Analyze resume pasted as plain text (no file upload)."""
    data = request.get_json() or {}
    text = data.get("text", "")
    jd   = data.get("job_description", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    skills   = extract_all_skills_flat(text)
    ats      = calculate_ats_score(text, jd)
    roles    = predict_job_roles(text)
    gap      = analyze_skill_gap(text)
    contact  = extract_contact_info(text)

    return jsonify({
        "skills":          skills,
        "contact":         contact,
        "ats_score":       ats,
        "predicted_roles": roles,
        "skill_gap":       gap
    })
