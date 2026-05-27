"""
SmartHire AI - Interview Simulator Routes
==========================================
POST /api/interview/start    → Start a session
POST /api/interview/answer   → Submit an answer
GET  /api/interview/history  → Get past sessions
"""

from flask import Blueprint, request, jsonify
import json, random
from database.db import db, InterviewSession

interview_bp = Blueprint('interview', __name__)

# ─── Question Banks ────────────────────────────────────────────────────────────

QUESTION_BANK = {
    "General HR": [
        "Tell me about yourself and your career goals.",
        "What are your greatest strengths and areas for improvement?",
        "Where do you see yourself in 5 years?",
        "Why do you want to work at our company?",
        "Describe a challenge you overcame and what you learned.",
        "How do you handle pressure and tight deadlines?",
        "Describe your ideal work environment.",
    ],
    "Frontend Developer": [
        "Explain the difference between let, const, and var in JavaScript.",
        "What is the virtual DOM and why is it useful in React?",
        "How do you optimize a React application for performance?",
        "Explain CSS specificity with examples.",
        "What are React hooks? When would you use useEffect?",
        "How do you handle state management in large applications?",
        "Explain the concept of responsive design and how you implement it.",
    ],
    "Backend Developer": [
        "Explain REST vs GraphQL — when would you use each?",
        "How do you handle database transactions and rollbacks?",
        "Explain caching strategies and when to apply them.",
        "What is a microservices architecture? Pros and cons?",
        "How do you secure a REST API?",
        "Explain database indexing and query optimization.",
        "Describe your approach to handling 10,000 concurrent requests.",
    ],
    "Data Science": [
        "Explain the bias-variance tradeoff.",
        "When would you choose Random Forest over a neural network?",
        "How do you handle class imbalance in a dataset?",
        "Explain cross-validation and why it matters.",
        "What is gradient descent and how does it work?",
        "Explain precision vs recall and when each matters.",
        "How would you approach a time-series forecasting problem?",
    ],
    "Python Developer": [
        "What are Python decorators and how do you use them?",
        "Explain GIL (Global Interpreter Lock) and its implications.",
        "What is the difference between a generator and a list comprehension?",
        "How do you manage dependencies and virtual environments?",
        "Explain async/await in Python with an example.",
        "What are metaclasses and when would you use them?",
        "How do you optimize Python code for performance?",
    ],
    "Data Analyst": [
        "How would you approach analyzing a dataset with missing values?",
        "Explain the difference between SQL JOIN types with examples.",
        "What visualization would you choose for comparing KPIs over time?",
        "Describe your process for building a dashboard from scratch.",
        "How do you validate the integrity of your analytical results?",
        "Explain statistical significance in plain business terms.",
        "Walk me through how you'd solve a drop in conversion rate.",
    ],
}

EVALUATION_CRITERIA = {
    "keywords": ["implemented", "designed", "optimized", "developed", "managed",
                 "achieved", "improved", "reduced", "increased", "delivered"],
    "vague_words": ["thing", "stuff", "basically", "like", "kind of", "sort of"],
    "good_length": (50, 400),   # ideal word count range
}

def evaluate_answer(question: str, answer: str) -> dict:
    """Rule-based answer evaluator (augmented by AI in production)."""
    words = answer.split()
    wc = len(words)
    a_lower = answer.lower()

    # Length scoring
    min_w, max_w = EVALUATION_CRITERIA["good_length"]
    if wc < 20:
        length_score = 30
        length_feedback = "Answer is too short. Elaborate with specifics."
    elif wc > max_w:
        length_score = 70
        length_feedback = "Good detail, but consider being more concise."
    elif min_w <= wc <= max_w:
        length_score = 90
        length_feedback = "Good answer length."
    else:
        length_score = 60
        length_feedback = "Try to provide more detail."

    # Action verb usage
    kw_hits = sum(1 for kw in EVALUATION_CRITERIA["keywords"] if kw in a_lower)
    clarity_score = min(100, 40 + kw_hits * 12)

    # Vague language penalty
    vague_hits = sum(1 for v in EVALUATION_CRITERIA["vague_words"] if v in a_lower)
    vague_penalty = vague_hits * 8

    technical_score = max(30, min(100, clarity_score - vague_penalty))
    overall = round((length_score + technical_score + clarity_score) / 3)

    suggestions = []
    if wc < 30:
        suggestions.append("Structure your answer using the STAR method (Situation, Task, Action, Result).")
    if kw_hits < 2:
        suggestions.append("Use strong action verbs: 'implemented', 'designed', 'optimized'.")
    if vague_hits > 0:
        suggestions.append("Avoid vague language. Be specific with examples and metrics.")
    if overall >= 80:
        suggestions.append("Excellent answer! You demonstrated confidence and clarity.")

    return {
        "scores": {
            "Confidence":  length_score,
            "Clarity":     clarity_score,
            "Technical":   technical_score,
            "Overall":     overall
        },
        "suggestions": suggestions or ["Good answer. Keep practicing for consistency."],
        "word_count": wc
    }


@interview_bp.route('/start', methods=['POST'])
def start_session():
    data  = request.get_json() or {}
    role  = data.get("role", "General HR")
    count = int(data.get("question_count", 5))

    pool = QUESTION_BANK.get(role, QUESTION_BANK["General HR"])
    hr_pool = QUESTION_BANK["General HR"]

    # Mix role-specific + 2 HR questions
    selected = random.sample(pool, min(count - 2, len(pool)))
    selected += random.sample(hr_pool, min(2, len(hr_pool)))
    random.shuffle(selected)
    selected = selected[:count]

    session = InterviewSession(role=role, history=json.dumps([]), overall_score=0)
    db.session.add(session)
    db.session.commit()

    return jsonify({
        "session_id": session.id,
        "role":       role,
        "questions":  selected,
        "total":      len(selected)
    })


@interview_bp.route('/answer', methods=['POST'])
def submit_answer():
    data       = request.get_json() or {}
    session_id = data.get("session_id")
    question   = data.get("question", "")
    answer     = data.get("answer", "")

    if not answer.strip():
        return jsonify({"error": "Answer cannot be empty"}), 400

    evaluation = evaluate_answer(question, answer)

    # Update session history
    if session_id:
        session = InterviewSession.query.get(session_id)
        if session:
            history = json.loads(session.history or '[]')
            history.append({"question": question, "answer": answer, "evaluation": evaluation})
            session.history = json.dumps(history)
            # Running average of overall
            scores = [h["evaluation"]["scores"]["Overall"] for h in history]
            session.overall_score = round(sum(scores) / len(scores))
            db.session.commit()

    return jsonify({"evaluation": evaluation})


@interview_bp.route('/session/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = InterviewSession.query.get_or_404(session_id)
    return jsonify(session.to_dict())


@interview_bp.route('/roles', methods=['GET'])
def get_roles():
    return jsonify({"roles": list(QUESTION_BANK.keys())})
