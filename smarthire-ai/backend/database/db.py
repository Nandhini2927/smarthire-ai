"""
SmartHire AI - Database Layer
==============================
SQLite database setup with SQLAlchemy ORM.
Handles: Users, Resumes, Analysis results, Interview sessions.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

def init_db(app):
    """Initialize database with the Flask app."""
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///smarthire.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

# ─── Models ───────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(120), unique=True, nullable=True)
    name        = db.Column(db.String(100), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    resumes     = db.relationship('Resume', backref='owner', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'name': self.name}


class Resume(db.Model):
    __tablename__ = 'resumes'
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    filename        = db.Column(db.String(255))
    raw_text        = db.Column(db.Text)
    extracted_skills = db.Column(db.Text)   # JSON list
    ats_score       = db.Column(db.Float)
    job_roles       = db.Column(db.Text)    # JSON list
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    analyses        = db.relationship('Analysis', backref='resume_ref', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'ats_score': self.ats_score,
            'extracted_skills': json.loads(self.extracted_skills or '[]'),
            'job_roles': json.loads(self.job_roles or '[]'),
            'created_at': self.created_at.isoformat()
        }


class Analysis(db.Model):
    __tablename__ = 'analyses'
    id              = db.Column(db.Integer, primary_key=True)
    resume_id       = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    analysis_type   = db.Column(db.String(50))  # 'ats', 'gap', 'roadmap', 'enhance'
    result_data     = db.Column(db.Text)         # JSON
    job_description = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'analysis_type': self.analysis_type,
            'result_data': json.loads(self.result_data or '{}'),
            'created_at': self.created_at.isoformat()
        }


class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'
    id          = db.Column(db.Integer, primary_key=True)
    resume_id   = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    role        = db.Column(db.String(100))
    history     = db.Column(db.Text)   # JSON list of {q, a, feedback}
    overall_score = db.Column(db.Float)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'history': json.loads(self.history or '[]'),
            'overall_score': self.overall_score,
            'created_at': self.created_at.isoformat()
        }
