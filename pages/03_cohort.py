import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Cohort Analysis", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #070d1a; }
    section[data-testid="stSidebar"] { background-color: #0a1628; border-right: 1px solid #1a4a7a; }
    .metric-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0f3460 100%);
        padding: 20px; border-radius: 12px;
        border: 1px solid #1a4a7a; border-left: 4px solid #00d2ff;
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
    .page-header {
        border-bottom: 1px solid #1a4a7a;
        padding-bottom: 12px; margin-bottom: 24px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .page-title { color: #ffffff; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
    .page-meta { color: #6b8ab8; font-size: 11px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <span class="page-title">📊 CHURN INTELLIGENCE CONSOLE</span>
    <span class="page-meta">Q3 2024 ANALYSIS</span>
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

df['signup_date'] = datetime.now() - pd.to_timedelta(df['tenure'] * 30, unit='D')
df['cohort_month'] = df['signup_date'].dt.to_period('M').astype(str)
df['tenure_group'] = pd.cut(
    df['tenure'],
    bins=[0, 12, 24, 36, 48, 72],
    labels=['0-12 mo', '13-24 mo', '25-36 mo', '37-48 mo', '49+ mo']
)

total = len(df)
churn_rate = (df['Churn'] == 'Yes').mean() * 100
avg_tenure = df['tenure'].mean()
early_churn = df[df['tenure'] <= 6]
early_churn_rate = (early_churn['Churn'] == 'Yes').mean() * 100

# Filters row
col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
with col_f1:
    cohort_range = st.selectbox("COHORT RANGE", ["Last 12 Months (Default)", "Last 6 Months", "All Time"])
with col_f2:
    segment = st.selectbox("CUSTOMER SEGMENT", ["All Enterprise Clients", "Month-to-Month", "One Year", "Two Year"])
with col_f3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔄 RECALCULATE", use_container_width=True)

st.markdown("""
<div class="insight-bar">
    💡 <strong>AI Insight - Retention Anomaly:</strong> Early churn cohort (0-6 months) shows
    significantly higher churn rate. Correlates with onboarding friction events.
    <strong>Recommended: Strengthen Month 1-3 engagement protocols.</strong>
</div>
""", unsafe_allow_html=True)

# Cohort Heatmap
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Customer Retention Heatmap</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Monthly cohort retention by customer age</div>', unsafe_allow_html=True)

cohort_data = df.groupby(['cohort_month', 'tenure_group']).size().unstack(fill_value=0)
cohort_pct = cohort_data.div(cohort_data.sum(axis=1), axis=0) * 100
cohort_display = cohort_pct.tail(6)

fig_heat = go.Figure(data=go.Heatmap(
    z=cohort_display.values,
    x=[str(c) for c in cohort_display.columns],
    y=cohort_display.index.astype(str),
    colorscale=[[0, '#0d1f3c'], [0.3, '#0099cc'], [0.7, '#00d2ff'], [1, '#e74c3c']],
    text=cohort_display.values.round(0).astype(int),
    texttemplate="%{text}%",
    textfont={"size": 11, "color": "white"},
    showscale=False
))
fig_heat.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#6b8ab8',
    margin=dict(l=0, r=0, t=10, b=0),
    height=220
)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Two charts side by side
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Churn by Contract Type</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Churn correlation per agreement tier</div>', unsafe_allow_html=True)

    contract_churn = df.groupby('Contract')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    contract_churn.columns = ['Contract', 'Churn Rate']
    colors_map = {'Month-to-month': '#e74c3c', 'One year': '#f39c12', 'Two year': '#00d2ff'}
    fig3 = go.Figure(go.Bar(
        x=contract_churn['Churn Rate'],
        y=contract_churn['Contract'],
        orientation='h',
        marker_color=[colors_map.get(c, '#00d2ff') for c in contract_churn['Contract']],
        text=[f"{v:.1f}% Churn" for v in contract_churn['Churn Rate']],
        textposition='outside',
        textfont=dict(color='#6b8ab8', size=11)
    ))
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=60, t=10, b=0),
        height=220,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(gridcolor='#1a4a7a')
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tenure Hazard Zones</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Churn probability by customer age</div>', unsafe_allow_html=True)

    tenure_churn = df.groupby('tenure_group')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    tenure_churn.columns = ['Tenure Group', 'Churn Rate']
    fig4 = go.Figure(go.Scatter(
        x=tenure_churn['Tenure Group'].astype(str),
        y=tenure_churn['Churn Rate'],
        mode='lines+markers',
        line=dict(color='#00d2ff', width=2),
        marker=dict(color='#f39c12', size=8),
        fill='tozeroy',
        fillcolor='rgba(0,210,255,0.08)'
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=0, t=10, b=0),
        height=220
    )
    fig4.update_xaxes(gridcolor='#1a4a7a')
    fig4.update_yaxes(gridcolor='#1a4a7a')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Bottom KPI cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_charges = df['MonthlyCharges'].mean()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">${avg_charges*12:,.0f}</div>
        <div class="metric-label">Avg Cohort Value</div>
        <div class="metric-delta">Annual LTV estimate</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{avg_tenure:.0f} mo</div>
        <div class="metric-label">Average LTV</div>
        <div class="metric-delta">Avg customer lifespan</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{early_churn_rate:.1f}%</div>
        <div class="metric-label">Early Churn (M0-M6)</div>
        <div class="metric-delta">▲ High — needs action</div>
    </div>""", unsafe_allow_html=True)
with col4:
    retained = 100 - churn_rate
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{retained:.1f}%</div>
        <div class="metric-label">Retention Rate</div>
        <div class="metric-delta">Overall base health</div>
    </div>""", unsafe_allow_html=True)
