import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import joblib

# Symptom list used in my web application
symptomslist = [
    'abdominal_pain', 'acne', 'anxiety', 'cold_intolerance', 'constipation', 
    'darkening_of_skin', 'dehydration', 'depression', 'difficulty_sleeping', 
    'dizziness', 'dry_skin', 'excessive_hair_growth', 'fatigue', 
    'frequent_infections', 'frequent_urination', 'goiter', 'hair_loss', 
    'headache', 'heat_intolerance', 'high_blood_pressure', 'hoarseness', 
    'increased_hunger', 'increased_thirst', 'irregular_menstrual_cycles', 
    'joint_pain', 'low_blood_pressure', 'mood_swings', 'muscle_weakness', 
    'nausea', 'nervousness', 'palpitations', 'rapid_heart_rate', 'slow_heart_rate', 
    'sweating', 'tremors', 'vision_problems', 'vomiting', 'weight_gain', 'weight_loss'
]

# Original data (extended to match the symptoms list)
data = {
    'abdominal_pain': [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'acne': [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'anxiety': [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'cold_intolerance': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'constipation': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'darkening_of_skin': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'dehydration': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'depression': [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    'difficulty_sleeping': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'dizziness': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'dry_skin': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'excessive_hair_growth': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'fatigue': [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
    'frequent_infections': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'frequent_urination': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    'goiter': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'hair_loss': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'headache': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'heat_intolerance': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'high_blood_pressure': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'hoarseness': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'increased_hunger': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    'increased_thirst': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    'irregular_menstrual_cycles': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'joint_pain': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'low_blood_pressure': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'low_blood_sugar': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'mood_swings': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    'muscle_weakness': [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    'nausea': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'nervousness': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Osteoporosis': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'palpitations': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'rapid_heart_rate': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'salt_craving': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'sleep_disturbances': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'slow_healing_sows': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'slow_heart_rate': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'stretch_marks': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'sweating': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'tremors': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'thin_skin': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'vision_problems': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    'vomiting': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'weight_gain': [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'weight_loss': [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    'prognosis': ['Hypothyroidism', 'Hyperthyroidism', 'Cushing Syndrome', 'Diabetes Mellitus', 'Addisons Disease', 'Acromegaly', 'Hypopituitarism', 'Hyperparathyroidism', 'Hypoparathyroidism', 'Adrenal Insufficiency', 'Pineal Tumors', 'Type 2 Diabetes', 'Type 1 Diabetes']
}
# Extend other symptoms columns to match the length of the data
for symptom in symptomslist:
    if symptom not in data:
        data[symptom] = [0] * len(data['prognosis'])

df = pd.DataFrame(data)

# Generate synthetic data
def generate_synthetic_data(df, n_samples):
    synthetic_data = resample(df, replace=True, n_samples=n_samples, random_state=42)
    return synthetic_data

# Generate 100 synthetic samples
synthetic_df = generate_synthetic_data(df, 100)

# Prepare the data for training
X = synthetic_df.drop(columns=['prognosis'])
y = synthetic_df['prognosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Save the trained model
joblib.dump(model, 'trainedd_model')
