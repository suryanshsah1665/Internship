import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "code_quality_model.pkl")


model, label_encoder = joblib.load(MODEL_PATH)

def predict_quality(features_dict):
    input_df = pd.DataFrame([features_dict])

    # Get prediction
    prediction_encoded = model.predict(input_df)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

    # Get probabilities
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    return prediction_label, float(round(confidence, 4))