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
```
Fraud Detection System/
├── backend/
│   ├── src/
│   │   ├── api/                 # App/API entry points (app.py)
│   │   ├── core/                # Core logic/models
│   │   ├── scripts/             # Data scripts (eda_processing.py, train.py)
│   │   └── models/              # Saved model artifacts
│   └── requirements.txt
├── data/
│   ├── raw/                     # Original CSVs
│   └── processed/               # Cleaned/Scaled CSVs
├── frontend/
│   ├── src/                     # React Components (.tsx)
│   ├── package.json
│   └── tsconfig.json            # TS Configuration
├── reports/
│   └── figures/                 # EDA Plots
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

---
**Last Updated**: April 21, 2026
**Current Status**: Phase 2 Complete. Ready for Phase 3 (Advanced Modeling).
