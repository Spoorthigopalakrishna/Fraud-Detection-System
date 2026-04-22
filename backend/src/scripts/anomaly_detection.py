"""
Phase 3: Isolation Forest + Autoencoder (Anomaly Detection)
==========================================================
- Implements Isolation Forest (Unsupervised, contamination=0.002)
- Implements Autoencoder (Semi-supervised, trained on legit only)
- Uses a specific 14-dim bottleneck architecture for Autoencoder
- Compares performance and saves the final models
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    average_precision_score, 
    precision_recall_curve,
    confusion_matrix,
    classification_report
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'processed.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'backend', 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

def run_phase3():
    # 1. Load Data
    print(f"[INFO] Loading processed data from {PROCESSED_DATA_PATH}...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # -------------------------------------------------------------------------
    # PART 1: ISOLATION FOREST (Unsupervised)
    # -------------------------------------------------------------------------
    print("\n--- [PART 1] Isolation Forest ---")
    # contamination=0.002 as requested
    iso_forest = IsolationForest(contamination=0.002, random_state=42, n_jobs=-1)
    
    print("[INFO] Training Isolation Forest...")
    iso_forest.fit(X_train)
    
    # decision_function: lower values are more anomalous. 
    # For PR-AUC, we want higher values for anomalies.
    iso_scores = -iso_forest.decision_function(X_test)
    
    iso_pr_auc = average_precision_score(y_test, iso_scores)
    print(f"Isolation Forest PR-AUC: {iso_pr_auc:.4f}")

    # -------------------------------------------------------------------------
    # PART 2: AUTOENCODER (Deep Learning Anomaly Detection)
    # -------------------------------------------------------------------------
    print("\n--- [PART 2] Autoencoder ---")
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Dense
        from tensorflow.keras.callbacks import EarlyStopping
    except ImportError:
        print("[ERROR] TensorFlow not found. Please install it to run the Autoencoder.")
        return

    # Train only on legitimate transactions
    X_train_legit = X_train[y_train == 0]
    
    # Autoencoders with Sigmoid output work best with [0, 1] scaled data
    ae_scaler = MinMaxScaler()
    X_train_ae = ae_scaler.fit_transform(X_train_legit)
    X_test_ae = ae_scaler.transform(X_test)
    
    input_dim = X_train.shape[1]
    encoding_dim = 14
    
    # Architecture as requested
    inputs = Input(shape=(input_dim,))
    encoded = Dense(encoding_dim, activation='relu')(inputs)
    decoded = Dense(input_dim, activation='sigmoid')(encoded)
    
    autoencoder = Model(inputs, decoded)
    autoencoder.compile(optimizer='adam', loss='mse')
    
    print(f"[INFO] Training Autoencoder (bottleneck={encoding_dim}) on legit data...")
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    history = autoencoder.fit(
        X_train_ae, X_train_ae,
        epochs=50,
        batch_size=128,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1
    )
    
    # Calculate reconstruction error (MSE) as anomaly score
    X_test_pred = autoencoder.predict(X_test_ae)
    mse = np.mean(np.power(X_test_ae - X_test_pred, 2), axis=1)
    
    ae_pr_auc = average_precision_score(y_test, mse)
    print(f"Autoencoder PR-AUC: {ae_pr_auc:.4f}")

    # -------------------------------------------------------------------------
    # PART 3: SAVE MODELS AND METRICS
    # -------------------------------------------------------------------------
    print("\n--- [PART 3] Saving Results ---")
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Save Isolation Forest
    joblib.dump(iso_forest, os.path.join(MODELS_DIR, 'iso_forest_model.pkl'))
    
    # Save Autoencoder and its Scaler
    autoencoder.save(os.path.join(MODELS_DIR, 'autoencoder_model.h5'))
    joblib.dump(ae_scaler, os.path.join(MODELS_DIR, 'ae_scaler.pkl'))
    
    # Save metrics
    metrics = {
        "isolation_forest": {"pr_auc": float(iso_pr_auc)},
        "autoencoder": {"pr_auc": float(ae_pr_auc)}
    }
    
    with open(os.path.join(REPORTS_DIR, 'metrics_phase3.json'), 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"[INFO] Models saved to {MODELS_DIR}")
    print(f"[INFO] Metrics saved to {os.path.join(REPORTS_DIR, 'metrics_phase3.json')}")
    
    # Plot PR Curves
    plt.figure(figsize=(10, 6))
    
    # ISO Forest
    p_iso, r_iso, _ = precision_recall_curve(y_test, iso_scores)
    plt.plot(r_iso, p_iso, label=f'Isolation Forest (AUC={iso_pr_auc:.4f})')
    
    # Autoencoder
    p_ae, r_ae, _ = precision_recall_curve(y_test, mse)
    plt.plot(r_ae, p_ae, label=f'Autoencoder (AUC={ae_pr_auc:.4f})')
    
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve Comparison')
    plt.legend()
    plt.savefig(os.path.join(REPORTS_DIR, 'phase3_pr_curve.png'))
    plt.close()
    
    print("[DONE] Phase 3 completed.")

if __name__ == "__main__":
    run_phase3()
