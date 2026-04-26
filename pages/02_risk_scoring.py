import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Risk Scoring", page_icon="🎯", layout="wide")

st.markdown('<h1 style="color: #00d2ff;">🎯 Risk Scoring</h1>', unsafe_allow_html=True)

# Load data
try:
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
except Exception as e:
    st.error(f"Could not load data file: {e}")
    st.stop()

# Calculate risk_score (this column doesn't exist in CSV, we create it)
df['risk_score'] = (
    (df['MonthlyCharges'] / df['MonthlyCharges'].max()) * 0.5 +
    (1 - df['tenure'] / df['tenure'].max()) * 0.5
) * 100

# Top 50 at-risk customers
st.subheader("🏆 Top 50 At-Risk Customers")

cols_to_show = [c for c in ['customerID', 'Contract', 'tenure', 'MonthlyCharges', 'risk_score']
                if c in df.columns]

if len(cols_to_show) == 0:
    st.error("No matching columns found!")
    st.write("Available columns:", df.columns.tolist())
else:
    top_50 = df.nlargest(50, 'risk_score')[cols_to_show]
    st.dataframe(top_50, use_container_width=True)

# Risk distribution chart
st.subheader("📊 Risk Score Distribution")
risk_bins = pd.cut(df['risk_score'], bins=10)
st.bar_chart(risk_bins.value_counts().sort_index())
