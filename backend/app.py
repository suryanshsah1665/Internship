from flask import Flask, request, jsonify
from feature_extractor import extract_features
from predict import predict_quality
from database import save_analysis, get_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# -------------------------------
# Health Check Route
# -------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Code Quality Classification API Running"})


# -------------------------------
# Analyze Code Route
# -------------------------------
@app.route("/analyze", methods=["POST"])
def analyze_code():

    try:
        data = request.get_json()
        code_text = data.get("code")
        user_id = data.get("user_id", "default_user")

        print("Extracting features...")
        features = extract_features(code_text)
        print("Features:", features)

        print("Predicting...")
        prediction, confidence = predict_quality(features)
        print("Prediction:", prediction, confidence)

        # 🔹 Save result to database
        save_analysis(features, prediction, user_id)

        response = {
            "features": features,
            "predicted_quality": prediction,
            "confidence": confidence
        }

        return jsonify(response)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
# -------------------------------
# History Route
# -------------------------------
@app.route("/history", methods=["GET"])
def get_history():
    try:
        conn = get_connection()
        cur = conn.cursor()
        data = request.args.get("user_id")

        cur.execute("""
                    SELECT id,
                           lines_of_code,
                           num_functions,
                           num_loops,
                           num_conditionals,
                           nested_loop_depth,
                           avg_function_length,
                           cyclomatic_complexity,
                           predicted_label,
                           created_at
                    FROM analyses
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    """, (data,))


        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "lines_of_code": row[1],
                "num_functions": row[2],
                "num_loops": row[3],
                "num_conditionals": row[4],
                "nested_loop_depth": row[5],
                "avg_function_length": row[6],
                "cyclomatic_complexity": row[7],
                "predicted_label": row[8],
                "created_at": row[9].strftime("%Y-%m-%d %H:%M:%S")
            })

        cur.close()
        conn.close()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))