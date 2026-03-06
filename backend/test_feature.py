from feature_extractor import extract_features

sample_code = """
def example():
    for i in range(10):
        for j in range(5):
            if j % 2 == 0:
                print(i, j)
"""

features = extract_features(sample_code)
print(features)