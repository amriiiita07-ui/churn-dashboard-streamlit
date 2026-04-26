import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Risk Scoring", page_icon="🎯", layout="wide")

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

st.title("🎯 Risk Scoring & Customer Segmentation")
st.markdown('<p style="color: #a0a0a0; margin-bottom: 25px;">Identify and prioritize at-risk customers before they churn</p>', unsafe_allow_html=True)
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

# Calculate risk score
df['risk_score'] = (
    (df['MonthlyCharges'] / df['MonthlyCharges'].max()) * 0.5 +
    (1 - df['tenure'] / df['tenure'].max()) * 0.5
) * 100

df['risk_category'] = pd.cut(
    df['risk_score'],
    bins=[0, 20, 40, 60, 80, 100],
    labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
)

# KPI Cards
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📈 Risk Overview</h3>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

high_risk = df[df['risk_score'] >= 60]
avg_risk = df['risk_score'].mean()
high_risk_churned = df[(df['risk_score'] >= 60) & (df['Churn'] == 'Yes')]

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(high_risk)}</div>
        <div class="metric-label">High Risk Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_risk:.1f}</div>
        <div class="metric-label">Avg Risk Score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(high_risk_churned)}</div>
        <div class="metric-label">High Risk Already Churned</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pct = (len(high_risk) / len(df) * 100)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{pct:.1f}%</div>
        <div class="metric-label">% Customers at High Risk</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Charts
st.markdown('<h3 style="color: #00d2ff; margin-bottom: 20px;">📊 Risk Distribution</h3>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    risk_counts = df['risk_category'].value_counts().sort_index().reset_index()
    risk_counts.columns = ['Risk Category', 'Count']
    fig1 = px.bar(
        risk_counts,
        x='Risk Category',
        y='Count',
        color='Count',
        color_continuous_scale='Blues',
        title="Customers by Risk Category"
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
    fig2 = px.scatter(
        df.sample(500),
        x='tenure',
        y='MonthlyCharges',
        color='risk_score',
        color_continuous_scale='Blues',
        title="Risk Score by Tenure vs Monthly Charges",
        labels={'risk_score': 'Risk Score'}
    )
fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0'
    )
    fig2.update_xaxes(gridcolor='#1a4a7a')
    fig2.update_yaxes(gridcolor='#1a4a7a')
    st.plotly_chart(fig2, use_container_width=True)
