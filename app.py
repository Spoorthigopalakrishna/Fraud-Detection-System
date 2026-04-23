from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import json
import pandas as pd
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
CORS(app)

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'backend', 'models', 'baseline_lr.pkl')
METRICS_PATH = os.path.join(BASE_DIR, 'reports', 'metrics_baseline.json')

# --- LOAD ASSETS AT STARTUP ---
def load_assets():
    try:
        model = joblib.load(MODEL_PATH)
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)
        return model, metrics
    except Exception as e:
        print(f"Error loading model or metrics: {e}")
        return None, None

model, metrics_data = load_assets()

# --- INPUT VALIDATION SCHEMA ---
class TransactionSchema(Schema):
    scaled_amount = fields.Float(required=True)
    scaled_time = fields.Float(required=True)
    # Define V1 to V28 fields
    V1 = fields.Float(required=True)
    V2 = fields.Float(required=True)
    V3 = fields.Float(required=True)
    V4 = fields.Float(required=True)
    V5 = fields.Float(required=True)
    V6 = fields.Float(required=True)
    V7 = fields.Float(required=True)
    V8 = fields.Float(required=True)
    V9 = fields.Float(required=True)
    V10 = fields.Float(required=True)
    V11 = fields.Float(required=True)
    V12 = fields.Float(required=True)
    V13 = fields.Float(required=True)
    V14 = fields.Float(required=True)
    V15 = fields.Float(required=True)
    V16 = fields.Float(required=True)
    V17 = fields.Float(required=True)
    V18 = fields.Float(required=True)
    V19 = fields.Float(required=True)
    V20 = fields.Float(required=True)
    V21 = fields.Float(required=True)
    V22 = fields.Float(required=True)
    V23 = fields.Float(required=True)
    V24 = fields.Float(required=True)
    V25 = fields.Float(required=True)
    V26 = fields.Float(required=True)
    V27 = fields.Float(required=True)
    V28 = fields.Float(required=True)

transaction_schema = TransactionSchema()

# --- ENDPOINTS ---

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict fraud for a given transaction.
    Expected body: JSON with scaled_amount, scaled_time, and V1-V28.
    """
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
    
    # Validate input using Marshmallow
    try:
        validated_data = transaction_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 422
    
    # Convert to DataFrame
    input_df = pd.DataFrame([validated_data])
    
    # Ensure correct feature order
    feature_cols = ['scaled_amount', 'scaled_time'] + [f'V{i}' for i in range(1, 29)]
    input_df = input_df[feature_cols]
    
    try:
        # Get probability of class 1 (Fraud)
        prob = model.predict_proba(input_df)[0][1]
        is_fraud = bool(prob > 0.5)
        
        return jsonify({
            "fraud": is_fraud,
            "score": round(float(prob), 4)
        })
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Return model performance metrics and threshold used.
    """
    if not metrics_data:
        return jsonify({"error": "Metrics data not available"}), 500
    
    return jsonify({
        "accuracy": round(metrics_data.get('classification_report', {}).get('accuracy', 0), 4),
        "precision": round(metrics_data.get('precision', 0), 4),
        "recall": round(metrics_data.get('recall', 0), 4),
        "threshold_used": 0.5,
        "model_name": metrics_data.get('model_name', 'Baseline Model')
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None}), 200

if __name__ == '__main__':
    # Run: flask run --port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
