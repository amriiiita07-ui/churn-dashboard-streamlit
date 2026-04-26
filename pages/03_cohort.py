import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Cohort Analysis", page_icon="👥", layout="wide")

# Custom CSS - matching theme
st.markdown("""
<style>
    .main { background-color: #0a1628; }
    .stApp { background-color: #0a1628; }
    .metric-card {
        background-color: #0f3460;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #00d2ff;
        text-align: center;
    }
    .metric-value {
        color: #00d2ff;
        font-size: 24px;
        font-weight: bold;
    }
    .metric-label {
        color: #a0a0a0;
        font-size: 14px;
    }
    .insight-box {
        background-color: #0f3460;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #00d2ff;
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .insight-box h4 {
        color: #00d2ff;
        margin-top: 0;
        font-size: 18px;
        margin-bottom: 15px;
    }
    .insight-box strong { color: #f39c12; }
</style>
""", unsafe_allow_html=True)

st.title("👥 Cohort Analysis")
st.markdown('<p style="color: #a0a0a0; margin-bottom: 25px;">Understand retention patterns across customer cohorts over time</p>', unsafe_allow_html=True)
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    except Exception as e:
        st.error(f"Could not load data file: {e}")
        st.stop()

df = load_data()

# Create cohort_month from tenure
df['signup_date'] = datetime.now() - pd.to_timedelta(df['tenure'] * 30, unit='D')
df['cohort_month'] = df['signup_date'].dt.to_period('M').astype(str)
df['tenure_group'] = pd.cut(
    df['tenure'],
    bins=[0, 12, 24, 36, 48, 72],
    labels=['0-12 mo', '13-24 mo', '25-36 mo', '37-48 mo', '49+ mo']
)

# KPI Cards
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📈 Cohort Overview</h3>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total = len(df)
churned_count = (df['Churn'] == 'Yes').sum()
churn_rate = churned_count / total * 100
avg_tenure = df['tenure'].mean()
best_cohort = df.groupby('tenure_group')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).idxmin()

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total:,}</div>
        <div class="metric-label">Total Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{churn_rate:.1f}%</div>
        <div class="metric-label">Overall Churn Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_tenure:.0f} mo</div>
        <div class="metric-label">Avg Customer Tenure</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{best_cohort}</div>
        <div class="metric-label">Best Retention Cohort</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Charts
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📊 Cohort Analysis Charts</h3>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    contract_churn = df.groupby('Contract')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).reset_index()
    contract_churn.columns = ['Contract', 'Churn Rate (%)']

    fig1 = px.bar(
        contract_churn,
        x='Contract',
        y='Churn Rate (%)',
        color='Churn Rate (%)',
        color_continuous_scale='Blues',
        title="Churn Rate by Contract Type"
    )
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0'
    )
    fig1.update_xaxes(gridcolor='#1a4a7a')
    fig1.update_yaxes(gridcolor='#1a4a7a')
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    tenure_churn = df.groupby('tenure_group')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).reset_index()
    tenure_churn.columns = ['Tenure Group', 'Churn Rate (%)']

    fig2 = px.bar(
        tenure_churn,
        x='Tenure Group',
        y='Churn Rate (%)',
        color='Churn Rate (%)',
        color_continuous_scale='Blues',
        title="Churn Rate by Tenure Group"
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0'
    )
    fig2.update_xaxes(gridcolor='#1a4a7a')
    fig2.update_yaxes(gridcolor='#1a4a7a')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Cohort summary table
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📋 Cohort Details Table</h3>', unsafe_allow_html=True)

cohort_summary = df.groupby(['Contract', 'tenure_group']).agg(
    Churn_Rate=('Churn', lambda x: round((x == 'Yes').mean() * 100, 1)),
    Customer_Count=('customerID', 'count'),
    Avg_Monthly_Charge=('MonthlyCharges', lambda x: round(x.mean(), 2))
).reset_index()

cohort_summary.columns = ['Contract', 'Tenure Group', 'Churn Rate (%)', 'Customers', 'Avg Monthly Charge ($)']
st.dataframe(cohort_summary, use_container_width=True)

st.markdown("---")

st.markdown("""
<div class="insight-box">
<h4>💡 Cohort Insight</h4>
<p><strong>Highest Risk Cohort:</strong> Month-to-month customers in the 0-12 month tenure group</p>
<p><strong>Best Retention:</strong> Two-year contract customers show dramatically lower churn across all tenure groups</p>
<p><strong>Action:</strong> Encourage early contract upgrades within the first 6 months to lock in retention</p>
</div>
""", unsafe_allow_html=True)
