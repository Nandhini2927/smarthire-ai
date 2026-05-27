"""
SmartHire AI - Deployment Ready app.py
Replace your backend/app.py with this file before deploying
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from database.db import init_db
from routes.resume import resume_bp
from routes.interview import interview_bp
from routes.roadmap_analysis import analysis_bp, roadmap_bp
import os
import nltk

# Download nltk data on startup
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

def create_app():
    app = Flask(__name__,
                static_folder='../frontend/static',
                template_folder='../frontend/templates')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smarthire-secret-2024')
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/smarthire.db')

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    init_db(app)

    app.register_blueprint(resume_bp,   url_prefix='/api/resume')
    app.register_blueprint(interview_bp,url_prefix='/api/interview')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(roadmap_bp,  url_prefix='/api/roadmap')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Serve frontend index.html at root URL
    @app.route('/')
    def serve_frontend():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../frontend', path)

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
