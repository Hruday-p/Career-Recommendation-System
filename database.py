import sqlite3
import hashlib
import json
from datetime import datetime

class CareerAdvisorDB:
    def __init__(self, db_name='career_advisor.db'):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mi_scores TEXT NOT NULL,
                academic_data TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                career_name TEXT NOT NULL,
                match_percentage INTEGER NOT NULL,
                rank INTEGER NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments (id)
            )
        ''')

        conn.commit()
        conn.close()
        print("Database initialized successfully!")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, full_name, email, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            password_hash = self.hash_password(password)

            cursor.execute('''
                INSERT INTO users (full_name, email, password_hash)
                VALUES (?, ?, ?)
            ''', (full_name, email, password_hash))

            user_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return {'success': True, 'user_id': user_id, 'message': 'Registration successful'}
        except sqlite3.IntegrityError:
            return {'success': False, 'message': 'Email already exists'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def login_user(self, email, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            password_hash = self.hash_password(password)

            cursor.execute('''
                SELECT id, full_name, email FROM users
                WHERE email = ? AND password_hash = ?
            ''', (email, password_hash))

            user = cursor.fetchone()

            if user:
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user[0],))
                conn.commit()

                conn.close()
                return {
                    'success': True,
                    'user_id': user[0],
                    'full_name': user[1],
                    'email': user[2],
                    'message': 'Login successful'
                }
            else:
                conn.close()
                return {'success': False, 'message': 'Invalid email or password'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def save_assessment(self, user_id, mi_scores, academic_data):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO assessments (user_id, mi_scores, academic_data)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(mi_scores), json.dumps(academic_data)))

            assessment_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return {'success': True, 'assessment_id': assessment_id}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_user_assessments(self, user_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, mi_scores, academic_data, completed_at
                FROM assessments
                WHERE user_id = ?
                ORDER BY completed_at DESC
            ''', (user_id,))

            assessments = []
            for row in cursor.fetchall():
                assessments.append({
                    'id': row[0],
                    'mi_scores': json.loads(row[1]),
                    'academic_data': json.loads(row[2]),
                    'completed_at': row[3]
                })

            conn.close()
            return {'success': True, 'assessments': assessments}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def save_recommendations(self, assessment_id, recommendations):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            for rank, rec in enumerate(recommendations, 1):
                cursor.execute('''
                    INSERT INTO recommendations (assessment_id, career_name, match_percentage, rank)
                    VALUES (?, ?, ?, ?)
                ''', (assessment_id, rec['career'], rec['matchPercentage'], rank))

            conn.commit()
            conn.close()

            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_recommendations(self, assessment_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT career_name, match_percentage, rank
                FROM recommendations
                WHERE assessment_id = ?
                ORDER BY rank
            ''', (assessment_id,))

            recommendations = []
            for row in cursor.fetchall():
                recommendations.append({
                    'career': row[0],
                    'matchPercentage': row[1],
                    'rank': row[2]
                })

            conn.close()
            return {'success': True, 'recommendations': recommendations}
        except Exception as e:
            return {'success': False, 'message': str(e)}

if __name__ == "__main__":
    db = CareerAdvisorDB()
    print("Career Advisor Database is ready!")
