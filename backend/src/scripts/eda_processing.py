"""
Phase 1: Dataset + EDA & Processing
=====================================
- Loads raw Credit Card Fraud dataset
- Performs EDA and generates visualizations
- Scales features (Amount, Time) and cleans data
- Saves processed dataset for model training
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, RobustScaler

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'creditcard.csv')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'processed.csv')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'figures')

def run_phase1():
    # Ensure directories exist
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # 1. Load Dataset
    print(f"[INFO] Loading data from {RAW_DATA_PATH}...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    initial_rows = len(df)
    print(f"[INFO] Initial rows: {initial_rows}")

    # 2. Clean Data (Drop duplicates)
    df.drop_duplicates(inplace=True)
    print(f"[INFO] Rows after dropping duplicates: {len(df)} ({initial_rows - len(df)} removed)")

    # 3. EDA & Visualizations
    sns.set_theme(style="whitegrid", palette="muted")
    
    # 3a. Class Imbalance
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(x='Class', data=df)
    plt.title('Class Distribution (0: No Fraud, 1: Fraud)')
    plt.yscale('log') # Log scale to see the imbalance clearly
    plt.savefig(os.path.join(REPORTS_DIR, 'plot1_class_imbalance.png'))
    plt.close()
    
    fraud_pct = (df['Class'].sum() / len(df)) * 100
    print(f"[INFO] Fraud percentage: {fraud_pct:.4f}%")

    # 3b. Transaction Amount Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df[df['Class'] == 0]['Amount'], color='blue', label='Normal', kde=True, stat="density", common_norm=False)
    sns.histplot(df[df['Class'] == 1]['Amount'], color='red', label='Fraud', kde=True, stat="density", common_norm=False)
    plt.title('Transaction Amount Distribution')
    plt.xlim(0, 2000) # Fraud typically at lower amounts
    plt.legend()
    plt.savefig(os.path.join(REPORTS_DIR, 'plot2_amount_distribution.png'))
    plt.close()

    # 3c. Fraud by Hour (Derived from Time)
    df['Hour'] = (df['Time'] // 3600) % 24
    plt.figure(figsize=(12, 6))
    sns.kdeplot(df[df['Class'] == 0]['Hour'], color='blue', label='Normal', fill=True)
    sns.kdeplot(df[df['Class'] == 1]['Hour'], color='red', label='Fraud', fill=True)
    plt.title('Transaction Density by Hour')
    plt.xlabel('Hour of Day')
    plt.xticks(range(0, 24))
    plt.legend()
    plt.savefig(os.path.join(REPORTS_DIR, 'plot3_fraud_by_hour.png'))
    plt.close()

    # 3d. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    corr = df.corr()
    sns.heatmap(corr, cmap='coolwarm', annot=False, fmt='.2f')
    plt.title('Feature Correlation Heatmap')
    plt.savefig(os.path.join(REPORTS_DIR, 'plot4_correlation_heatmap.png'))
    plt.close()

    # 4. Scaling Amount and Time
    # RobustScaler is better if there are outliers (Amount has many)
    rob_scaler = RobustScaler()
    df['scaled_amount'] = rob_scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    df['scaled_time'] = rob_scaler.fit_transform(df['Time'].values.reshape(-1, 1))
    
    # Drop original columns and the derived Hour column (only for EDA)
    df.drop(['Time', 'Amount', 'Hour'], axis=1, inplace=True)
    
    # Move scaled columns to the front
    scaled_amount = df['scaled_amount']
    scaled_time = df['scaled_time']
    df.drop(['scaled_amount', 'scaled_time'], axis=1, inplace=True)
    df.insert(0, 'scaled_amount', scaled_amount)
    df.insert(1, 'scaled_time', scaled_time)

    # 5. Save Processed Data
    print(f"[INFO] Saving processed data to {PROCESSED_DATA_PATH}...")
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print("[DONE] Phase 1 completed successfully.")

if __name__ == '__main__':
    run_phase1()
