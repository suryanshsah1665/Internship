import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
DATA_PATH = "../data/training_dataset.csv"
MODEL_DIR = "../models"
MODEL_PATH = os.path.join(MODEL_DIR, "code_quality_model.pkl")

# Ensure models folder exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(DATA_PATH)

# Separate features and label
X = df.drop("label", axis=1)
y = df["label"]

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model + label encoder
joblib.dump((model, label_encoder), MODEL_PATH)

print("\nModel saved successfully at:", MODEL_PATH)