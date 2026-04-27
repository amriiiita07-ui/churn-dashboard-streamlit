import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Risk Analysis", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #070d1a; }
    section[data-testid="stSidebar"] { background-color: #0a1628; border-right: 1px solid #1a4a7a; }
    .metric-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0f3460 100%);
        padding: 20px; border-radius: 12px;
        border: 1px solid #1a4a7a;
        border-left: 4px solid #00d2ff;
        text-align: center; margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,210,255,0.08);
    }
    .metric-value { color: #00d2ff; font-size: 28px; font-weight: 700; font-family: 'Roboto Mono', monospace; }
    .metric-label { color: #6b8ab8; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
    .metric-delta { color: #f39c12; font-size: 12px; margin-top: 4px; }
    .section-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0f2a50 100%);
        border: 1px solid #1a4a7a; border-radius: 14px;
        padding: 24px; margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .section-title { color: #00d2ff; font-size: 16px; font-weight: 600; margin-bottom: 4px; }
    .section-subtitle { color: #6b8ab8; font-size: 12px; margin-bottom: 16px; }
    .insight-bar {
        background: linear-gradient(90deg, #0f3460, #0d1f3c);
        border: 1px solid #f39c12; border-left: 4px solid #f39c12;
        border-radius: 8px; padding: 16px; margin-bottom: 20px;
    }
    .insight-bar p { color: #e0e0e0; margin: 0; font-size: 13px; }
    .insight-bar strong { color: #f39c12; }
    .badge-critical {
        background: #7b1c1c; color: #ff6b6b;
        padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600;
    }
    .badge-warning {
        background: #5c3d00; color: #f39c12;
        padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600;
    }
    .page-header {
        border-bottom: 1px solid #1a4a7a;
        padding-bottom: 12px; margin-bottom: 24px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .page-title { color: #ffffff; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
    .page-meta { color: #6b8ab8; font-size: 11px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <span class="page-title">⚠ CHURN INTELLIGENCE CONSOLE</span>
    <span class="page-meta">Last Compute: LIVE</span>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    except Exception as e:
        st.error(f"Could not load data: {e}")
        st.stop()

df = load_data()

df['risk_score'] = (
    (df['MonthlyCharges'] / df['MonthlyCharges'].max()) * 0.5 +
    (1 - df['tenure'] / df['tenure'].max()) * 0.5
) * 100

df['risk_category'] = pd.cut(
    df['risk_score'],
    bins=[0, 20, 40, 60, 80, 100],
    labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
)

high_risk = df[df['risk_score'] >= 60]
avg_risk = df['risk_score'].mean()
high_risk_churned = df[(df['risk_score'] >= 60) & (df['Churn'] == 'Yes')]
pct = len(high_risk) / len(df) * 100

# KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{avg_risk:.1f}%</div>
        <div class="metric-label">System Aggregate Risk</div>
        <div class="metric-delta">▲ HIGH RISK WARNING</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(high_risk):,}</div>
        <div class="metric-label">High Risk Customers</div>
        <div class="metric-delta">{pct:.1f}% of total base</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(high_risk_churned):,}</div>
        <div class="metric-label">Already Churned</div>
        <div class="metric-delta">From high risk pool</div>
    </div>""", unsafe_allow_html=True)
with col4:
    revenue_at_risk = high_risk['MonthlyCharges'].sum()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">${revenue_at_risk:,.0f}</div>
        <div class="metric-label">MRR at Risk</div>
        <div class="metric-delta">Monthly exposure</div>
    </div>""", unsafe_allow_html=True)

# AI Insight Bar
st.markdown("""
<div class="insight-bar">
    💡 <strong>AI Insight:</strong> High-risk cluster detected in Month-to-Month customers with tenure &lt; 12 months.
    High correlation with MonthlyCharges &gt; $70. <strong>Recommended action: Trigger retention protocol immediately.</strong>
</div>
""", unsafe_allow_html=True)

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">System Aggregate Risk Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Real-time churn probability assessment</div>', unsafe_allow_html=True)

    risk_counts = df['risk_category'].value_counts().sort_index().reset_index()
    risk_counts.columns = ['Risk Category', 'Count']
    colors = ['#00d2ff', '#0099cc', '#006699', '#f39c12', '#e74c3c']
    fig1 = go.Figure(go.Bar(
        x=risk_counts['Risk Category'],
        y=risk_counts['Count'],
        marker_color=colors,
        marker_line_width=0
    ))
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=0, t=10, b=0),
        height=260
    )
    fig1.update_xaxes(gridcolor='#1a4a7a', showline=False)
    fig1.update_yaxes(gridcolor='#1a4a7a', showline=False)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Risk vs. Revenue Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Identifying high-value churn targets</div>', unsafe_allow_html=True)

    sample = df.sample(min(300, len(df)), random_state=42)
    fig2 = px.scatter(
        sample,
        x='MonthlyCharges',
        y='risk_score',
        color='risk_score',
        color_continuous_scale=[[0, '#00d2ff'], [0.5, '#f39c12'], [1, '#e74c3c']],
        size='MonthlyCharges',
        size_max=12,
        labels={'MonthlyCharges': 'Revenue Potential', 'risk_score': 'Churn Probability'}
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=0, t=10, b=0),
        height=260,
        coloraxis_showscale=False
    )
    fig2.update_xaxes(gridcolor='#1a4a7a', showline=False)
    fig2.update_yaxes(gridcolor='#1a4a7a', showline=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# High Risk Table
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔴 High-Risk Customer Registry</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Priority list for immediate intervention</div>', unsafe_allow_html=True)

cols = [c for c in ['customerID', 'Contract', 'tenure', 'MonthlyCharges', 'risk_score', 'Churn'] if c in df.columns]
top_customers = df.nlargest(20, 'risk_score')[cols].reset_index(drop=True)
top_customers['risk_score'] = top_customers['risk_score'].round(1)
st.dataframe(top_customers, use_container_width=True, height=280)
st.markdown('</div>', unsafe_allow_html=True)
