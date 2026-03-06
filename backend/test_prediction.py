from feature_extractor import extract_features
from predict import predict_quality

sample_code = """
def calculate():
    total = 0
    for i in range(100):
        for j in range(50):
            if j % 2 == 0:
                total += j
    return total
"""

features = extract_features(sample_code)
print("Extracted Features:", features)

result = predict_quality(features)
print("Predicted Quality:", result)