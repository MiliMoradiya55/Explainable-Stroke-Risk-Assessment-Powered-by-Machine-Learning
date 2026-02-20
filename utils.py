import joblib
import pandas as pd
import os

required_files = ['stroke_model.pkl', 'scaler.pkl', 'label_encoders.pkl', 'imputer.pkl']
for f in required_files:
    if not os.path.exists(f):
        raise FileNotFoundError(f"❌ Missing {f}. Please run train_model.py first.")

model = joblib.load('stroke_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')
imputer = joblib.load('imputer.pkl')

feature_columns = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
                   'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']

def preprocess_input(data_dict):
    # Create a new dictionary with correct case for Residence_type
    processed_dict = {}
    for key, value in data_dict.items():
        if key == 'residence_type':
            processed_dict['Residence_type'] = value
        else:
            processed_dict[key] = value

    # Ensure all required columns are present (fill missing with defaults if needed)
    for col in feature_columns:
        if col not in processed_dict:
            print(f"⚠️ Warning: Missing column {col} in input data. Using default.")
            if col in ['hypertension', 'heart_disease']:
                processed_dict[col] = 0
            elif col == 'bmi':
                processed_dict[col] = imputer.statistics_[0]
            else:
                # For categorical, use the first class of the encoder
                if col in label_encoders:
                    processed_dict[col] = label_encoders[col].classes_[0]
                else:
                    processed_dict[col] = 'Unknown'

    df = pd.DataFrame([processed_dict])

    # Encode categoricals
    for col in ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']:
        le = label_encoders[col]
        # Handle unknown categories: map to the most frequent class (first in classes_)
        df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        df[col] = le.transform(df[col].astype(str))

    # Ensure correct column order
    df = df[feature_columns]

    # Impute BMI if still missing
    if pd.isna(df['bmi'].iloc[0]):
        df['bmi'] = imputer.statistics_[0]

    scaled = scaler.transform(df)
    return scaled

def predict_stroke(data_dict):
    processed = preprocess_input(data_dict)
    pred = model.predict(processed)[0]
    proba = model.predict_proba(processed)[0][1]
    return int(pred), float(proba)