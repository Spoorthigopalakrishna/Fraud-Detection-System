"""
Phase 2: Imbalance Handling + Baseline Model
===========================================
- Loads processed dataset
- Splits into training and testing sets
- Applies SMOTE to handling class imbalance (on training set ONLY)
- Trains a baseline Logistic Regression model
- Evaluates performance using PR-AUC and other fraud-specific metrics
- Saves metrics for comparison
"""

import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_recall_curve, 
    auc, 
    average_precision_score, 
    confusion_matrix, 
    classification_report,
    f1_score,
    precision_score,
    recall_score
)
from imblearn.over_sampling import SMOTE

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'processed.csv')
MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'backend', 'models', 'baseline_lr.pkl')
METRICS_SAVE_PATH = os.path.join(BASE_DIR, 'reports', 'metrics_baseline.json')

def train_model():
    # 1. Load Processed Data
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"[ERROR] Processed data not found at {PROCESSED_DATA_PATH}. Please run eda_processing.py first.")
        return

    print(f"[INFO] Loading processed data from {PROCESSED_DATA_PATH}...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    X = df.drop('Class', axis=1)
    y = df['Class']

    # 2. Train-Test Split (Stratified to maintain class ratio)
    print("[INFO] Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Imbalance Handling with SMOTE (Training set only)
    print("[INFO] Applying SMOTE to training set...")
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
    
    print(f"Original training shape: {X_train.shape}")
    print(f"Resampled training shape: {X_train_res.shape}")
    print(f"Fraud count after SMOTE: {y_train_res.sum()} / {len(y_train_res)}")

    # 4. Train Baseline Model (Logistic Regression)
    print("[INFO] Training Logistic Regression baseline...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_res, y_train_res)

    # 5. Evaluation
    print("[INFO] Evaluating model on raw test set...")
    y_pred = model.predict(X_test)
    y_probs = model.predict_proba(X_test)[:, 1]

    # PR-AUC Calculation
    precision, recall, _ = precision_recall_curve(y_test, y_probs)
    pr_auc = auc(recall, precision)
    avg_precision = average_precision_score(y_test, y_probs)

    # Standard metrics
    conf_matrix = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    metrics = {
        "model_name": "Logistic Regression (Baseline + SMOTE)",
        "pr_auc": pr_auc,
        "average_precision": avg_precision,
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "confusion_matrix": conf_matrix.tolist(),
        "classification_report": report
    }

    print("\n--- Baseline Model Performance ---")
    print(f"PR-AUC: {pr_auc:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")
    print("\nConfusion Matrix:")
    print(conf_matrix)

    # 6. Save Model and Metrics
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(METRICS_SAVE_PATH), exist_ok=True)

    print(f"\n[INFO] Saving model to {MODEL_SAVE_PATH}...")
    joblib.dump(model, MODEL_SAVE_PATH)

    print(f"[INFO] Saving metrics to {METRICS_SAVE_PATH}...")
    with open(METRICS_SAVE_PATH, 'w') as f:
        json.dump(metrics, f, indent=4)

    print("[DONE] Phase 2 completed successfully.")

if __name__ == "__main__":
    train_model()
