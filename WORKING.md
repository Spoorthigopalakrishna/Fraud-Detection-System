# WORKING.md — Project Progress Log
# Fraud Detection System

## Phase 1 — Dataset + EDA & Processing (COMPLETED)
**Goal**: Prepare the credit card fraud dataset and extract initial insights.

### Implementation Details
- **Data Source**: Kaggle Credit Card Fraud Detection (284,807 rows).
- **Cleaning**: 
    - Dropped 1,081 duplicate transactions.
    - Handled extreme class imbalance (0.17% fraud).
- **Feature Engineering**:
    - Derived `Hour` from the `Time` column to analyze temporal patterns.
    - Scaled `Amount` and `Time` using `RobustScaler` to handle outliers effectively.
- **EDA & Processing Script**: Migrated logic from `.ipynb` to `backend/src/scripts/eda_processing.py` for deployment stability.

## Frontend Migration (COMPLETED)
- **TypeScript Transition**: Renamed all `.jsx` files to `.tsx` and configured `tsconfig.json`.
- **Type Safety**: Integrated `@types/react` and `@types/react-dom` for robust component development.

### Key Insights
- **Amount Clustering**: Fraudulent transactions predominantly occur at low amounts (often < $100), likely to avoid triggering immediate suspicion or automated limits.
- **Temporal Patterns**: Fraud density is significantly higher during late-night and early-morning hours (e.g., 2 AM - 5 AM), suggesting attackers exploit periods when users are less likely to monitor their accounts.
- **Class Imbalance**: The 0.17% fraud rate necessitates specialized techniques like SMOTE or cost-sensitive learning in Phase 2.

### File Structure Reference
```text
Fraud Detection System/
├── backend/
│   ├── src/
│   │   ├── api/                 # App/API entry points (app.py)
│   │   ├── core/                # Core logic/models
│   │   ├── scripts/             # Data scripts (eda_processing.py, train.py)
│   │   └── models/              # Saved model artifacts
│   └── requirements.txt
├── frontend/
│   ├── data/                    # Datasets (raw & processed)
│   ├── reports/                 # EDA Plots & Metrics
│   ├── src/                     # React Application (.js)
│   │   ├── components/          # UI Components
│   │   ├── services/            # API Integration
│   │   └── styles/              # Global CSS & Tailwind
│   └── package.json             # Frontend dependencies
└── WORKING.md                   # This file
```

## Phase 2 — Imbalance Handling + Baseline Model (COMPLETED)
**Goal**: Address class imbalance and establish a performance baseline.

### Implementation Details
- **Imbalance Handling**: Applied **SMOTE** (Synthetic Minority Over-sampling Technique) to the training set only, balancing the classes to a 50/50 ratio.
- **Baseline Model**: Trained a **Logistic Regression** model using `scikit-learn`.
- **Evaluation**: Prioritized **PR-AUC** (Precision-Recall Area Under Curve) over accuracy due to extreme class imbalance (99.8% legit).
- **Deliverables**: 
    - Confusion Matrix, Precision, Recall, and F1-score computed on the raw (unbalanced) test set.
    - Metrics saved to `reports/metrics_baseline.json`.
    - Model artifact saved to `backend/models/baseline_lr.pkl`.

### Baseline Metrics
- **PR-AUC**: 0.7088
- **Recall**: 87.37% (Caught 83 out of 95 fraud cases)
- **Precision**: 5.39% (High false positive rate, expected for a simple baseline with SMOTE)
- **F1-Score**: 0.1015

### Key Takeaway
The baseline model shows high recall (87%), which is crucial for fraud detection, but the low precision (5.39%) indicates a need for more sophisticated models (e.g., Random Forest, XGBoost) in Phase 3 to reduce false positives while maintaining or improving fraud detection rates.

## Phase 3 — Two models, one winner (COMPLETED)
**Goal**: Implement unsupervised and deep learning anomaly detection models to catch fraud without labels.

### Implementation Details
- **Isolation Forest**:
    - Unsupervised approach, ideal for production where fraud labels are delayed.
    - Configured with `contamination=0.002` (matching the dataset fraud rate).
    - **PR-AUC**: 0.1091
- **Autoencoder**:
    - Deep learning approach using Keras.
    - Trained exclusively on **legitimate transactions** to learn the "normal" pattern.
    - **Architecture**: 14-dim bottleneck relu layer, sigmoid output, MSE loss.
    - **Anomaly Detection**: Reconstruction error (MSE) used as a natural anomaly score.
    - **PR-AUC**: 0.3424 (The Winner)
- **Deliverables**:
    - Precision-Recall curve comparison plot saved to `reports/phase3_pr_curve.png`.
    - Metrics saved to `reports/metrics_phase3.json`.
    - Autoencoder model saved to `backend/models/autoencoder_model.h5`.

### Key Insights
- **The Winner**: The **Autoencoder** significantly outperformed the Isolation Forest (0.34 PR-AUC vs 0.11). It's more effective at capturing the complex, non-linear relationships in transaction data.
- **Natural Scoring**: Using reconstruction error provides a clear, interpretable score for "how unusual" a transaction is, which is highly valuable for risk teams.

---
## Phase 4 — Flask REST API (COMPLETED)
**Goal**: Build a production-ready REST API to serve predictions and model metrics.

### Implementation Details
- **Framework**: Flask with CORS enabled for frontend integration.
- **Input Validation**: Integrated **Marshmallow** for strict transaction JSON validation (scaled_amount, scaled_time, V1-V28).
- **Endpoints**:
    - `POST /predict`: Receives transaction data, returns fraud verdict and probability score.
    - `GET /metrics`: Returns model accuracy, precision, recall, and the threshold used.
    - `GET /health`: Basic health check for monitoring.
- **Optimization**: The model (`baseline_lr.pkl`) and metrics are loaded once at startup to ensure low-latency responses.

### Key Features
- **Strict Validation**: Returns 422 Unprocessable Entity if input features are missing or malformed.
- **CORS Support**: Ready to be consumed by the React dashboard in Phase 5.
- **Clean Structure**: Separated validation schemas from route logic for maintainability.

---
---
## Phase 5 — React frontend (COMPLETED)
**Goal**: Build a dynamic, real-time dashboard to interface with the Fraud Detection API.

### Implementation Details
- **Framework & Styling**: Initialized with React and integrated Tailwind CSS v3 for a premium, responsive glassmorphism UI.
- **Component Architecture**:
    - `TransactionForm`: Includes customized range sliders for PCA features (V1-V5) to dynamically test transactions.
    - `ResultCard`: Provides immediate, color-coded visual feedback (Legitimate/Fraudulent) with an animated anomaly score bar.
    - `LiveFeed`: Displays a rolling table of the last 10 transactions and their statuses.
    - `Dashboard`: Uses `recharts` for a live Donut Chart tracking the fraud-to-legit ratio and a Line Chart tracking historical anomaly scores.
- **Integration**:
    - Centralized `axios` logic into `src/services/api.js` to securely push `POST` requests to `http://localhost:5000/predict`.
- **Refactoring**: Professionally reorganized the `frontend/` directory structure, removed unused boilerplate, and moved the `data/` and `reports/` folders inside it per request.

### Key Features
- Dynamic layout updating instantly via React state tracking (`stats`, `history`, `transactions`).
- Robust error handling for Flask server connection drops.
- Aesthetic details including CSS keyframe animations and transparent gradient visuals.

---
**Last Updated**: April 24, 2026
**Current Status**: Phase 5 Complete. The full-stack pipeline (React Dashboard + Flask API) is successfully integrated and operational.
