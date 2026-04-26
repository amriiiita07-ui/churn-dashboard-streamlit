"""
utils/data_loader.py
====================
Shared data loading utilities for the Streamlit dashboard.

WHY SEPARATE FILE:
- Avoids code duplication across pages
- Centralizes data source management
- Easy to switch between local and remote data
"""

import os
import pandas as pd
import numpy as np


def load_dashboard_data():
    """
    Load data for the dashboard.

    TRIES (in order):
    1. Local features_for_dashboard.csv (from python-analysis repo)
    2. Local cleaned_churn.csv (from data-pipeline repo)
    3. Synthetic data (fallback, always works)

    RETURNS:
    - pandas DataFrame ready for visualization
    """
    # Possible paths
    paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                     '..', 'churn-python-analysis', 'data', 'features_for_dashboard.csv'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                     '..', 'churn-data-pipeline', 'data', 'processed', 'cleaned_churn.csv'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'churn_data.csv'),
    ]

    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Ensure key columns exist
            if 'risk_segment' not in df.columns:
                df = add_default_features(df)
            return df

    # Fallback: generate synthetic data
    return generate_synthetic_data()


def add_default_features(df):
    """Add default features if missing from loaded data."""
    if 'risk_segment' not in df.columns:
        def segment(row):
            if row['Contract'] == 'Month-to-month':
                return 'High Risk' if row['tenure'] < 12 or row['MonthlyCharges'] > 80 else 'Medium Risk'
            elif row['Contract'] == 'One year':
                return 'Medium Risk' if row['tenure'] < 12 else 'Low Risk'
            return 'Low Risk'
        df['risk_segment'] = df.apply(segment, axis=1)

    if 'ltv_projected' not in df.columns:
        multipliers = {'Month-to-month': 6, 'One year': 12, 'Two year': 24}
        df['ltv_projected'] = df.apply(lambda r: r['MonthlyCharges'] * multipliers.get(r['Contract'], 12), axis=1)

    if 'cohort' not in df.columns:
        df['cohort'] = pd.cut(df['tenure'], bins=[-1, 6, 12, 24, 36, 72],
                               labels=['0-6m', '7-12m', '13-24m', '25-36m', '37m+'])

    return df


def generate_synthetic_data(n=3000):
    """Generate synthetic data for demo purposes."""
    np.random.seed(42)
    data = {
        'customerID': [f'CUST-{i:05d}' for i in range(n)],
        'gender': np.random.choice(['Male', 'Female'], n),
        'SeniorCitizen': np.random.choice([0, 1], n, p=[0.84, 0.16]),
        'Partner': np.random.choice(['Yes', 'No'], n, p=[0.48, 0.52]),
        'Dependents': np.random.choice(['Yes', 'No'], n, p=[0.30, 0.70]),
        'tenure': np.random.randint(0, 73, n),
        'PhoneService': np.random.choice(['Yes', 'No'], n, p=[0.90, 0.10]),
        'MultipleLines': np.random.choice(['Yes', 'No', 'No phone service'], n, p=[0.42, 0.48, 0.10]),
        'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n, p=[0.34, 0.44, 0.22]),
        'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n, p=[0.29, 0.50, 0.21]),
        'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n, p=[0.34, 0.44, 0.22]),
        'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n, p=[0.34, 0.44, 0.22]),
        'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n, p=[0.29, 0.50, 0.21]),
        'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n, p=[0.38, 0.40, 0.22]),
        'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n, p=[0.39, 0.39, 0.22]),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n, p=[0.55, 0.24, 0.21]),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n, p=[0.59, 0.41]),
        'PaymentMethod': np.random.choice(
            ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
            n, p=[0.34, 0.23, 0.22, 0.21]
        ),
        'MonthlyCharges': np.round(np.random.uniform(18.0, 118.0, n), 2),
        'TotalCharges': np.round(np.random.uniform(0, 8000, n), 2),
        'Churn': np.random.choice(['Yes', 'No'], n, p=[0.27, 0.73]),
    }
    df = pd.DataFrame(data)
    return add_default_features(df)
