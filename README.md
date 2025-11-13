# AI-Powered Career Recommendation System

## 🎯 Project Overview

An intelligent career recommendation system that uses Multiple Intelligence Assessment to suggest personalized career paths.

## ✨ Key Features Implemented

### 1. Assessment

- **40 Questions Total** (5 questions per intelligence category)
- **1-5 Rating Scale** (Strongly Disagree to Strongly Agree)
- 8 Multiple Intelligence Categories:
  - Linguistic
  - Logical-Mathematical
  - Spatial
  - Bodily-Kinesthetic
  - Musical
  - Interpersonal
  - Intrapersonal
  - Naturalistic

### 2. Database Integration

- **SQLite Database** for persistent data storage
- **User Management**: Registration, login, and authentication
- **Assessment History**: Stores all user assessments
- **Career Recommendations**: Saves recommendations for future reference
- **Secure Password Hashing** using SHA-256

### 3. Career Recommendations

- Top 3 career matches based on MI scores and preferences
- Match percentage for each career
- Detailed 5-stage career progression path
- Skills requirements for each career

## 📁 Project Structure

```
project/
├── index.html                    # Landing page
├── signup.html                   # Registration page
├── login.html                    # Login page
├── assessment.html               # MI Assessment (40 questions, 1-5 scale)
├── results_updated.html          # Career recommendations
├── database.py                   # SQLite database management
├── app.py                        # Flask backend API
├── mi_questions_40.json          # Question bank
├── requirements.txt              # Python dependencies
└── career_advisor.db             # SQLite database (auto-created)
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
python database.py
```

This will create the SQLite database with all required tables.

### Step 3: Start the Flask Backend

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 4: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

## 🔄 User Flow

1. **Landing Page** → User sees welcome screen
2. **Sign Up** → New users create an account
3. **Login** → Existing users log in
4. **Assessment** → Complete 40 MI questions (1-5 scale)
5. **Academic Input** → Enter scores and preferences
6. **Results** → View top 3 career recommendations
7. **Career Paths** → Explore 5-stage progression for each career

## 💾 Database Schema

### Users Table

- id (Primary Key)
- full_name
- email (Unique)
- password_hash
- created_at
- last_login

### Assessments Table

- id (Primary Key)
- user_id (Foreign Key)
- mi_scores (JSON)
- academic_data (JSON)
- completed_at

### Recommendations Table

- id (Primary Key)
- assessment_id (Foreign Key)
- career_name
- match_percentage
- rank

## 🎨 Key Changes from Previous Version

1. **Questions**: Increased from 24 (3 per category) to 40 (5 per category)
2. **Rating Scale**: Changed from 1-10 to 1-5 for better user experience
3. **Database**: Replaced localStorage with SQLite for persistent storage
4. **Backend**: Added Flask API for frontend-backend communication
5. **Authentication**: Secure user registration and login system
6. **Data Persistence**: All assessments and recommendations saved in database

## 🔧 API Endpoints

- `POST /api/register` - Register new user
- `POST /api/login` - Authenticate user
- `POST /api/save-assessment` - Save assessment data
- `GET /api/get-assessments/<user_id>` - Get user's assessment history
- `POST /api/save-recommendations` - Save career recommendations
- `GET /api/get-recommendations/<assessment_id>` - Get recommendations

## 📊 Career Options

The system recommends from 5 career paths:

1. Software Engineer
2. Data Scientist
3. Graphic Designer
4. Teacher
5. Psychologist

Each career includes:

- Detailed description
- Required skills
- 5-stage career progression (Entry → Mid → Senior → Lead → Executive)

## 🔒 Security Features

- Password hashing using SHA-256
- Session management with sessionStorage
- Input validation on both frontend and backend
- SQL injection prevention through parameterized queries

## 🐛 Troubleshooting

### Backend Not Starting

- Ensure all dependencies are installed
- Check if port 5000 is available
- Run `pip install -r requirements.txt` again

### Database Errors

- Delete `career_advisor.db` and run `python database.py` again
- Check file permissions

### Frontend Not Loading

- Ensure Flask server is running
- Check browser console for errors
- Verify API_URL in HTML files is `http://localhost:5000/api`

## 📝 Notes

- The system uses sessionStorage for temporary session data
- Database file (`career_advisor.db`) is created automatically
- All user passwords are securely hashed
- Assessment data is permanently stored and retrievable

## 🎓 Future Enhancements

- More career options (expandable database)
- Email verification
- Password reset functionality
- Advanced analytics dashboard
- PDF report generation
- Machine learning model integration

## 📧 Support

For issues or questions, please refer to the troubleshooting section or check the console logs for detailed error messages.

---

**Version**: 2.0  
**Last Updated**: November 2025  
**Features**: 40 Questions, 1-5 Scale, Database Integration
