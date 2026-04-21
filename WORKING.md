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

---
**Last Updated**: April 2026
**Current Status**: Phase 1 Complete. Ready for Phase 2 (Model Training).
