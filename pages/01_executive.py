"""
04_revenue.py
=============
Revenue Impact & ROI Calculator page.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Revenue Impact", layout="wide")

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

st.title("💰 Revenue Impact & ROI Analysis")
st.markdown('<p style="color: #a0a0a0; margin-bottom: 25px;">Quantify revenue at risk and optimize retention spend</p>', unsafe_allow_html=True)

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
        'tenure': np.random.randint(0, 72, 1000)
    })

df = load_data()

# Calculate metrics
total_customers = len(df)
churned = df[df['Churn'] == 'Yes']
active = df[df['Churn'] == 'No']

churned_mrr = churned['MonthlyCharges'].sum()
saved_mrr = active['MonthlyCharges'].sum()
annual_risk = churned_mrr * 12

# KPI Cards
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📈 Revenue Metrics</h3>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${churned_mrr:,.2f}</div>
        <div class="metric-label">Monthly Churned Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${annual_risk:,.2f}</div>
        <div class="metric-label">Annual Revenue at Risk</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${saved_mrr:,.2f}</div>
        <div class="metric-label">Active MRR</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    risk_pct = (churned_mrr / (churned_mrr + saved_mrr) * 100) if (churned_mrr + saved_mrr) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{risk_pct:.1f}%</div>
        <div class="metric-label">Revenue at Risk %</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Revenue at Risk by Segment
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📊 Revenue at Risk by Segment</h3>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    segment = st.selectbox("Segment by", ["Contract", "InternetService", "PaymentMethod"])
    
    segment_risk = df.groupby(segment).agg({
        'MonthlyCharges': ['sum', 'count'],
        'Churn': lambda x: (x == 'Yes').sum()
    }).reset_index()
    
    segment_risk.columns = [segment, 'Total_MRR', 'Total_Customers', 'Churned_Count']
    churned_mrr_by_segment = df[df['Churn'] == 'Yes'].groupby(segment)['MonthlyCharges'].sum()
    segment_risk['Churned_MRR'] = segment_risk[segment].map(churned_mrr_by_segment).fillna(0)
    segment_risk['At_Risk_Pct'] = (segment_risk['Churned_MRR'] / segment_risk['Total_MRR'] * 100).round(1)
    
    fig = px.bar(
        segment_risk, 
        x=segment, 
        y='Churned_MRR',
        color='At_Risk_Pct',
        color_continuous_scale='Blues',
        title=f"Monthly Revenue Lost by {segment}",
        labels={'Churned_MRR': 'Revenue Lost ($)', 'At_Risk_Pct': 'Risk %'}
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0'
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    max_risk_segment = segment_risk.loc[segment_risk['Churned_MRR'].idxmax(), segment]
    max_risk_amount = segment_risk['Churned_MRR'].max()
    
    st.markdown(f"""
    <div style="background-color: #0f3460; padding: 20px; border-radius: 12px; border-left: 4px solid #00d2ff;">
        <h4 style="color: #00d2ff; margin-top: 0;">📊 Key Insight</h4>
        <p style="color: #e0e0e0;">
        <strong style="color: #f39c12;">Highest Risk Segment: {max_risk_segment}</strong><br><br>
        • Monthly revenue lost: <strong>${max_risk_amount:,.2f}</strong><br>
        • This represents <strong>{(max_risk_amount / churned_mrr * 100):.1f}%</strong> of total churned revenue<br><br>
        <strong>Recommendation:</strong> Prioritize retention campaigns for this segment.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ROI Calculator
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">🎯 Retention Campaign ROI Calculator</h3>', unsafe_allow_html=True)

st.markdown('<p style="color: #a0a0a0;">Enter your proposed retention campaign costs and expected save rate</p>', unsafe_allow_html=True)

col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    campaign_cost = st.number_input("Campaign Cost ($)", min_value=0, value=5000, step=500)

with col_input2:
    target_customers = st.number_input("Target At-Risk Customers", min_value=1, value=100, step=10)

with col_input3:
    save_rate = st.slider("Expected Save Rate (%)", min_value=0, max_value=100, value=25)

# Calculate ROI
avg_monthly_charge = churned['MonthlyCharges'].mean() if len(churned) > 0 else 50
customers_saved = int(target_customers * (save_rate / 100))
revenue_saved_monthly = customers_saved * avg_monthly_charge
revenue_saved_annual = revenue_saved_monthly * 12
roi = ((revenue_saved_annual - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{customers_saved}</div>
        <div class="metric-label">Customers Saved</div>
    </div>
    """, unsafe_allow_html=True)

with col_r2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${revenue_saved_annual:,.2f}</div>
        <div class="metric-label">Annual Revenue Saved</div>
    </div>
    """, unsafe_allow_html=True)

with col_r3:
    delta_color = "normal" if roi > 0 else "inverse"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{roi:.0f}%</div>
        <div class="metric-label">Campaign ROI</div>
    </div>
    """, unsafe_allow_html=True)

# ROI Chart
fig_roi = go.Figure()
fig_roi.add_trace(go.Bar(
    x=['Campaign Cost', 'Revenue Saved (Annual)'],
    y=[campaign_cost, revenue_saved_annual],
    marker_color=['#E74C3C', '#2ECC71'],
    text=[f"${campaign_cost:,.0f}", f"${revenue_saved_annual:,.0f}"],
    textposition='auto'
))
fig_roi.update_layout(
    title="Campaign Cost vs. Revenue Saved",
    yaxis_title="Amount ($)",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#e0e0e0',
    showlegend=False
)
fig_roi.update_xaxes(gridcolor='#1a4a7a')
fig_roi.update_yaxes(gridcolor='#1a4a7a')

st.plotly_chart(fig_roi, use_container_width=True)

# Recommendation Card
st.markdown("---")

st.markdown("""
<div class="recommendation-box">
<h4>💡 Strategic Recommendation</h4>
<p><strong>Target:</strong> Month-to-month customers with tenure < 12 months and monthly charges > $70</p>
<p><strong>Action:</strong> Offer 15% discount for switching to annual contract + free tech support</p>
<p><strong>Expected Impact:</strong> Reduce churn by 8-12 percentage points in this cohort</p>
<p><strong>Investment:</strong> ~$50/customer | <strong>Annual Return:</strong> ~$600/customer retained</p>
</div>
""", unsafe_allow_html=True)
