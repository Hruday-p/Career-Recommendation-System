import joblib
import pandas as pd

# Load the trained model and preprocessors
model = joblib.load('career_recommendation_model.pkl')
scaler = joblib.load('scaler.pkl')
encoders = joblib.load('label_encoders.pkl')

# Example: Prepare new student data
student_data = {
    'Linguistic': 7.5,
    'Logical_Mathematical': 8.2,
    'Spatial': 6.1,
    # ... (all 12 MI and academic scores)
    'Favorite_Subject': 'Math',
    'Hobbies': 'Coding',
    'Preferred_Work_Style': 'Solo'
}

# Encode categorical features
student_data['Favorite_Subject_Encoded'] = encoders['Favorite_Subject'].transform([student_data['Favorite_Subject']])[0]
# ... (encode other categorical features)

# Normalize and predict
X = pd.DataFrame([student_data])
prediction = model.predict(X)
career = encoders['Target'].inverse_transform(prediction)[0]
print(f"Recommended Career: {career}")
