
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

# Calculate risk score
df['risk_score'] = (
    (df['MonthlyCharges'] / df['MonthlyCharges'].max()) * 0.5 +
    (1 - df['tenure'] / df['tenure'].max()) * 0.5
) * 100

# Top 50 at-risk customers
st.subheader("🏆 Top 50 At-Risk Customers")
cols_to_show = [c for c in ['customerID', 'Contract', 'tenure', 'MonthlyCharges', 'risk_score']
                if c in df.columns]
top_50 = df.nlargest(50, 'risk_score')[cols_to_show]
st.dataframe(top_50, use_container_width=True)

# Risk distribution chart — FIXED
st.subheader("📊 Risk Score Distribution")
df['risk_category'] = pd.cut(
    df['risk_score'],
    bins=[0, 20, 40, 60, 80, 100],
    labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
)
risk_counts = df['risk_category'].value_counts().sort_index().reset_index()
risk_counts.columns = ['Risk Category', 'Count']
st.bar_chart(risk_counts.set_index('Risk Category'))
