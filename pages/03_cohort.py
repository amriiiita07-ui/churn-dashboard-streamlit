"""
03_cohort.py
============
Cohort Analysis page - track customer retention over time.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Cohort Analysis", layout="wide")

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

st.title("👥 Cohort Analysis")
st.markdown('<p style="color: #a0a0a0; margin-bottom: 25px;">Track customer retention patterns and identify churn trends by acquisition cohort</p>', unsafe_allow_html=True)

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
        'TotalCharges': np.random.uniform(100, 8000, 1000)
    })

df = load_data()

# Calculate cohort metrics
df['cohort_month'] = pd.cut(df['tenure'], bins=[0, 6, 12, 24, 36, 48, 72], 
                            labels=['0-6m', '7-12m', '13-24m', '25-36m', '37-48m', '49m+'])

# KPI Cards
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📈 Cohort Overview</h3>', unsafe_allow_html=True)

avg_tenure_churned = df[df['Churn'] == 'Yes']['tenure'].mean()
avg_tenure_active = df[df['Churn'] == 'No']['tenure'].mean()
early_churners = len(df[(df['Churn'] == 'Yes') & (df['tenure'] < 12)])
retention_rate = (len(df[df['Churn'] == 'No']) / len(df)) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_tenure_churned:.1f}m</div>
        <div class="metric-label">Avg Tenure (Churned)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_tenure_active:.1f}m</div>
        <div class="metric-label">Avg Tenure (Active)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{early_churners}</div>
        <div class="metric-label">Early Churners (< 12m)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{retention_rate:.1f}%</div>
        <div class="metric-label">Overall Retention Rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Cohort Retention Heatmap
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📊 Cohort Retention Heatmap</h3>', unsafe_allow_html=True)

# Create cohort table
cohort_data = []
for contract in df['Contract'].unique():
    contract_df = df[df['Contract'] == contract]
    for cohort in df['cohort_month'].cat.categories:
        cohort_df = contract_df[contract_df['cohort_month'] == cohort]
        if len(cohort_df) > 0:
            retention = (len(cohort_df[cohort_df['Churn'] == 'No']) / len(cohort_df)) * 100
            cohort_data.append({
                'Contract': contract,
                'Cohort': cohort,
                'Retention_Rate': retention,
                'Total_Customers': len(cohort_df)
            })

cohort_table = pd.DataFrame(cohort_data)
cohort_pivot = cohort_table.pivot(index='Contract', columns='Cohort', values='Retention_Rate')

fig = px.imshow(
    cohort_pivot,
    text_auto='.1f',
    aspect='auto',
    color_continuous_scale='Blues',
    title='Retention Rate (%) by Contract Type & Tenure Cohort'
)
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#e0e0e0',
    xaxis_title='Tenure Cohort',
    yaxis_title='Contract Type'
)
fig.update_xaxes(gridcolor='#1a4a7a')
fig.update_yaxes(gridcolor='#1a4a7a')

st.plotly_chart(fig, use_container_width=True)

# Cohort Details Table
st.markdown("---")
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📋 Cohort Details</h3>', unsafe_allow_html=True)

cohort_summary = df.groupby(['Contract', 'cohort_month']).agg({
    'Churn': lambda x: (x == 'Yes').mean() * 100,
    'MonthlyCharges': 'mean',
    'customerID': 'count'
}).reset_index()

cohort_summary.columns = ['Contract', 'Cohort', 'Churn_Rate_%', 'Avg_Monthly_Charges', 'Total_Customers']
cohort_summary['Churn_Rate_%'] = cohort_summary['Churn_Rate_%'].round(1)
cohort_summary['Avg_Monthly_Charges'] = cohort_summary['Avg_Monthly_Charges'].round(2)

st.dataframe(cohort_summary, use_container_width=True, hide_index=True)

# Churn by Tenure Chart
st.markdown("---")
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📈 Churn Rate by Tenure</h3>', unsafe_allow_html=True)

tenure_churn = df.groupby('tenure').agg({
    'Churn': lambda x: (x == 'Yes').mean() * 100
}).reset_index()
tenure_churn.columns = ['Tenure', 'Churn_Rate']

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=tenure_churn['Tenure'],
    y=tenure_churn['Churn_Rate'],
    mode='lines+markers',
    line=dict(color='#00d2ff', width=3),
    marker=dict(size=6, color='#00d2ff'),
    name='Churn Rate'
))
fig_line.add_hline(y=df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0).mean() * 100, 
                   line_dash="dash", line_color="#E74C3C", 
                   annotation_text="Overall Avg", annotation_position="right")
fig_line.update_layout(
    title='Churn Rate by Tenure (Months)',
    xaxis_title='Tenure (Months)',
    yaxis_title='Churn Rate (%)',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#e0e0e0',
    showlegend=False
)
fig_line.update_xaxes(gridcolor='#1a4a7a')
fig_line.update_yaxes(gridcolor='#1a4a7a')

st.plotly_chart(fig_line, use_container_width=True)

# Recommendation Card
st.markdown("---")

st.markdown("""
<div class="recommendation-box">
<h4>💡 Strategic Recommendation</h4>
<p><strong>Finding:</strong> Churn is highest in the first 12 months, especially for month-to-month contracts.</p>
<p><strong>Action:</strong> Implement "First Year Care" program with proactive check-ins at months 3, 6, and 9.</p>
<p><strong>Expected Impact:</strong> Reduce first-year churn by 15-20% through early intervention.</p>
<p><strong>Priority:</strong> MEDIUM-HIGH - Critical for long-term customer lifetime value.</p>
</div>
""", unsafe_allow_html=True)
