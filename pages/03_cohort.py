import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Cohort Analysis", page_icon="👥", layout="wide")

st.markdown('<h1 style="color: #00d2ff;">👥 Cohort Analysis</h1>', unsafe_allow_html=True)

# Load data
try:
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
except Exception as e:
    st.error(f"Could not load data file: {e}")
    st.stop()

# Create cohort_month from tenure (NOT in original CSV - we create it)
df['signup_date'] = datetime.now() - pd.to_timedelta(df['tenure'] * 30, unit='D')
df['cohort_month'] = df['signup_date'].dt.to_period('M').astype(str)

# Cohort summary
st.subheader("📋 Cohort Details")

cohort_summary = df.groupby(['Contract', 'cohort_month']).agg({
    'Churn': lambda x: (x == 'Yes').mean() * 100,
    'customerID': 'count'
}).reset_index()

cohort_summary.columns = ['Contract', 'Cohort_Month', 'Churn_Rate_%', 'Customer_Count']
st.dataframe(cohort_summary, use_container_width=True)

# Churn by contract type
st.subheader("📈 Churn Rate by Contract Type")
contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
st.bar_chart(contract_churn)
