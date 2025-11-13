import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 1. Load the dataset
df = pd.read_csv('career_recommendation_dataset.csv')

# 2. Specify feature columns
continuous = [
    'Linguistic', 'Logical-Mathematical', 'Spatial', 'Bodily-Kinesthetic',
    'Musical', 'Interpersonal', 'Intrapersonal', 'Naturalistic',
    'Programming', 'Data_Analysis', 'Creativity', 'Mechanical_Skills',
    'Building_Skills', 'Communication', 'Empathy', 'Writing', 'Marketing', 'Design_Skills'
]
categorical = []

target = 'Recommended_Career_1'

# 3. Normalize continuous features
scaler = MinMaxScaler()
df[continuous] = scaler.fit_transform(df[continuous])

# 4. Encode categorical features
label_encoders = {}
for col in categorical:
    le = LabelEncoder()
    df[col + '_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# 5. Encode the target
le_target = LabelEncoder()
df['Target_Encoded'] = le_target.fit_transform(df[target])
label_encoders['Target'] = le_target  # Save for inverse_transform

# 6. Prepare feature matrix and target vector
all_features = continuous + [col + '_Encoded' for col in categorical]
X = df[all_features]
y = df['Target_Encoded']

# 7. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 8. Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 9. Save all pipeline parts
joblib.dump(model, 'career_recommendation_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

# 10. Optionally, save feature info for deployment
feature_info = {
    'continuous_features': continuous,
    'categorical_features': categorical,
    'all_features': all_features,
    'career_classes': list(le_target.classes_)
}
with open('model_info.json', 'w') as f:
    json.dump(feature_info, f, indent=2)

acc = accuracy_score(y_test, model.predict(X_test))
pre = precision_score(y_test, model.predict(X_test), average='weighted')
rec = recall_score(y_test, model.predict(X_test), average='weighted')
f1 = f1_score(y_test, model.predict(X_test), average='weighted')

print(f"Accuracy: {acc:.4f}")
print(f"Precision: {pre:.4f}")
print(f"Recall: {rec:.4f}")
print(f"F1 Score: {f1:.4f}")

print("All models and encoders saved successfully")
