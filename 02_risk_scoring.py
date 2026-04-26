"""
02_risk_scoring.py
==================
Risk Scoring page - identify and rank at-risk customers.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Risk Scoring", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0a1628;
    }
    .stApp {
        background-color: #0a1628;
    }
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
    .risk-high {
        background-color: rgba(231, 76, 60, 0.2);
        color: #e74c3c;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }
    .risk-medium {
        background-color: rgba(243, 156, 18, 0.2);
        color: #f39c12;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }
    .risk-low {
        background-color: rgba(46, 204, 113, 0.2);
        color: #2ecc71;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }
    .recommendation-box {
        background-color: #0f3460;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #00d2ff;
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .recommendation-box h4 {
        color: #00d2ff;
        margin-top: 0;
        font-size: 18px;
        margin-bottom: 15px;
    }
    .recommendation-box p {
        margin: 8px 0;
        line-height: 1.5;
    }
    .recommendation-box strong {
        color: #f39c12;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Risk Scoring")
st.markdown('<p style="color: #a0a0a0; margin-bottom: 25px;">Identify and prioritize at-risk customers for retention campaigns</p>', unsafe_allow_html=True)

st.markdown("---")

# Load data
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, 'data', 'churn_data.csv')
    
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    
    pipeline_path = os.path.join(
        os.path.dirname(project_root),
        'churn-data-pipeline', 'data', 'processed', 'cleaned_churn.csv'
    )
    if os.path.exists(pipeline_path):
        return pd.read_csv(pipeline_path)
    
    np.random.seed(42)
    return pd.DataFrame({
        'Churn': np.random.choice(['Yes', 'No'], 1000, p=[0.27, 0.73]),
        'MonthlyCharges': np.random.uniform(18, 118, 1000),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], 1000),
        'tenure': np.random.randint(0, 72, 1000),
        'OnlineSecurity': np.random.choice(['Yes', 'No'], 1000),
        'TechSupport': np.random.choice(['Yes', 'No'], 1000),
        'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], 1000),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], 1000)
    })

df = load_data()

# Calculate Risk Score
def calculate_risk_score(row):
    score = 0
    if row['Contract'] == 'Month-to-month': score += 35
    elif row['Contract'] == 'One year': score += 15
    else: score += 5
    
    if row['tenure'] < 6: score += 25
    elif row['tenure'] < 12: score += 20
    elif row['tenure'] < 24: score += 10
    
    if row.get('PaymentMethod', '') == 'Electronic check': score += 10
    if row.get('InternetService', '') == 'Fiber optic': score += 10
    if row.get('OnlineSecurity', '') == 'No': score += 10
    if row.get('TechSupport', '') == 'No': score += 5
    if row['MonthlyCharges'] > 90: score += 5
    
    return min(score, 100)

# Apply to active customers
active_df = df[df['Churn'] == 'No'].copy()
active_df['risk_score'] = active_df.apply(calculate_risk_score, axis=1)
active_df['risk_tier'] = pd.cut(active_df['risk_score'], 
                                bins=[0, 40, 60, 80, 100],
                                labels=['Low', 'Medium', 'High', 'Critical'])

# KPI Cards
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📈 Risk Overview</h3>', unsafe_allow_html=True)

high_risk = len(active_df[active_df['risk_tier'] == 'Critical'])
medium_risk = len(active_df[active_df['risk_tier'] == 'High'])
total_at_risk = high_risk + medium_risk
avg_risk_score = active_df['risk_score'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_at_risk}</div>
        <div class="metric-label">High/Medium Risk Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{high_risk}</div>
        <div class="metric-label">Critical Risk</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_risk_score:.1f}</div>
        <div class="metric-label">Average Risk Score</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    revenue_at_risk = active_df[active_df['risk_tier'].isin(['High', 'Critical'])]['MonthlyCharges'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${revenue_at_risk:,.0f}</div>
        <div class="metric-label">Monthly Revenue at Risk</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Risk Distribution Chart
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📊 Risk Distribution</h3>', unsafe_allow_html=True)

col_chart, col_table = st.columns([2, 1])

with col_chart:
    risk_dist = active_df['risk_tier'].value_counts().reset_index()
    risk_dist.columns = ['Risk_Tier', 'Count']
    
    color_map = {'Low': '#2ECC71', 'Medium': '#F39C12', 'High': '#E67E22', 'Critical': '#E74C3C'}
    
    fig = px.pie(risk_dist, values='Count', names='Risk_Tier', 
                 title='Customer Risk Distribution',
                 color='Risk_Tier', color_discrete_map=color_map)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0'
    )
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.markdown("""
    <div style="background-color: #0f3460; padding: 20px; border-radius: 12px; border-left: 4px solid #00d2ff;">
        <h4 style="color: #00d2ff; margin-top: 0;">🎯 Risk Tiers</h4>
        <p style="color: #e0e0e0; font-size: 14px;">
        <span class="risk-high">CRITICAL</span> 80-100: Immediate action<br><br>
        <span style="background-color: rgba(230, 126, 34, 0.2); color: #e67e22; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px;">HIGH</span> 60-79: Priority outreach<br><br>
        <span class="risk-medium">MEDIUM</span> 40-59: Monitor closely<br><br>
        <span class="risk-low">LOW</span> 0-39: Standard retention
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Top At-Risk Customers Table
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">🏆 Top 50 At-Risk Customers</h3>', unsafe_allow_html=True)

top_50 = active_df.nlargest(50, 'risk_score')[['customerID', 'Contract', 'tenure', 'MonthlyCharges', 'risk_score', 'risk_tier']].copy()
top_50['annual_revenue_at_risk'] = top_50['MonthlyCharges'] * 12

# Format risk tier with colors
def format_tier(tier):
    if tier == 'Critical':
        return '<span class="risk-high">CRITICAL</span>'
    elif tier == 'High':
        return '<span style="background-color: rgba(230, 126, 34, 0.2); color: #e67e22; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px;">HIGH</span>'
    elif tier == 'Medium':
        return '<span class="risk-medium">MEDIUM</span>'
    else:
        return '<span class="risk-low">LOW</span>'

top_50_display = top_50.head(10).copy()
top_50_display['risk_tier'] = top_50_display['risk_tier'].apply(format_tier)

st.markdown("""
<style>
    .dataframe {
        background-color: #0f3460;
        color: #e0e0e0;
        border-radius: 12px;
        border: 1px solid #1a4a7a;
    }
    .dataframe th {
        background-color: #162447;
        color: #00d2ff;
        font-weight: bold;
        padding: 12px;
        border-bottom: 2px solid #00d2ff;
    }
    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid #1a4a7a;
    }
</style>
""", unsafe_allow_html=True)

st.dataframe(
    top_50[['customerID', 'Contract', 'tenure', 'MonthlyCharges', 'risk_score', 'risk_tier', 'annual_revenue_at_risk']].head(20),
    use_container_width=True,
    hide_index=True
)

# Download button
csv = top_50.to_csv(index=False)
st.download_button(
    label="📥 Download Top 50 At-Risk Customers (CSV)",
    data=csv,
    file_name="top_50_at_risk_customers.csv",
    mime="text/csv",
    use_container_width=True
)

# Recommendation Card
st.markdown("---")

st.markdown("""
<div class="recommendation-box">
<h4>💡 Strategic Recommendation</h4>
<p><strong>Target:</strong> Focus on Critical and High-risk customers first (top 20% by risk score)</p>
<p><strong>Action:</strong> Personalized outreach within 48 hours for Critical tier; weekly for High tier</p>
<p><strong>Expected Impact:</strong> 15-20% save rate on Critical tier, 10-15% on High tier</p>
<p><strong>Investment:</strong> ~$75/customer for Critical | <strong>Annual Return:</strong> ~$900/customer retained</p>
</div>
""", unsafe_allow_html=True)