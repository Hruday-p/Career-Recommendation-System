from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import CareerAdvisorDB
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Initialize database
db = CareerAdvisorDB()

# Serve HTML files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('fullName')
    email = data.get('email')
    password = data.get('password')

    result = db.register_user(full_name, email, password)
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    result = db.login_user(email, password)
    return jsonify(result)

@app.route('/api/save-assessment', methods=['POST'])
def save_assessment():
    data = request.json
    user_id = data.get('userId')
    mi_scores = data.get('miScores')
    academic_data = data.get('academicData')

    result = db.save_assessment(user_id, mi_scores, academic_data)
    return jsonify(result)

@app.route('/api/get-assessments/<int:user_id>', methods=['GET'])
def get_assessments(user_id):
    result = db.get_user_assessments(user_id)
    return jsonify(result)

@app.route('/api/save-recommendations', methods=['POST'])
def save_recommendations():
    data = request.json
    assessment_id = data.get('assessmentId')
    recommendations = data.get('recommendations')

    result = db.save_recommendations(assessment_id, recommendations)
    return jsonify(result)

@app.route('/api/get-recommendations/<int:assessment_id>', methods=['GET'])
def get_recommendations(assessment_id):
    result = db.get_recommendations(assessment_id)
    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, port=5000)
