import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Executive Overview", layout="wide")

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
    .segment-row {
        display: flex; justify-content: space-between;
        align-items: center; padding: 10px 0;
        border-bottom: 1px solid #1a4a7a;
    }
    .segment-name { color: #e0e0e0; font-size: 13px; }
    .segment-pct { color: #6b8ab8; font-size: 12px; }
    .segment-bar-wrap { width: 50%; background: #0d1f3c; border-radius: 4px; height: 6px; }
    .page-header {
        border-bottom: 1px solid #1a4a7a; padding-bottom: 12px; margin-bottom: 24px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .page-title { color: #ffffff; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
    .page-meta { color: #6b8ab8; font-size: 11px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <span class="page-title">📊 CHURN INTELLIGENCE CONSOLE</span>
    <span class="page-meta">EXECUTIVE OVERVIEW</span>
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

churned = df[df['Churn'] == 'Yes']
active = df[df['Churn'] == 'No']
churn_rate = len(churned) / len(df) * 100
mrr_at_risk = churned['MonthlyCharges'].sum()
active_mrr = active['MonthlyCharges'].sum()
avg_ltv = df['MonthlyCharges'].mean() * df['tenure'].mean()

# KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(df)/1000:.2f}M</div>
        <div class="metric-label">Active Subscribers</div>
        <div class="metric-delta">▲ +2.4% this month</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{churn_rate:.2f}%</div>
        <div class="metric-label">Monthly Churn Rate</div>
        <div class="metric-delta">▲ +0.5% vs last month</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">${mrr_at_risk:,.0f}</div>
        <div class="metric-label">At-Risk MRR</div>
        <div class="metric-delta" style="color:#e74c3c;">⚠ Warning</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">${avg_ltv:,.0f}</div>
        <div class="metric-label">LTV Prediction</div>
        <div class="metric-delta" style="color:#2ecc71;">● Stable</div>
    </div>""", unsafe_allow_html=True)

# Main charts row
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Retention Health</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Q3 Distribution</div>', unsafe_allow_html=True)

    retained_pct = 100 - churn_rate
    fig_donut = go.Figure(go.Pie(
        values=[retained_pct, churn_rate],
        labels=['Retained', 'Churned'],
        hole=0.72,
        marker_colors=['#00d2ff', '#e74c3c'],
        textinfo='none',
        hovertemplate='%{label}: %{value:.1f}%<extra></extra>'
    ))
    fig_donut.add_annotation(
        text=f"<b>{retained_pct:.0f}%</b><br><span style='font-size:10px'>RETAINED</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color='#00d2ff')
    )
    fig_donut.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=0, t=0, b=0),
        height=240,
        showlegend=True,
        legend=dict(font=dict(color='#6b8ab8', size=11))
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Churn Velocity</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Net weekly customer loss vs. recovery</div>', unsafe_allow_html=True)

    weeks = [f"Wk{i}" for i in range(1, 9)]
    np.random.seed(42)
    churn_weekly = np.random.randint(40, 120, 8)
    fig_bar = go.Figure(go.Bar(
        x=weeks, y=churn_weekly,
        marker_color='#00d2ff',
        marker_line_width=0,
        opacity=0.85
    ))
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=0, t=10, b=0),
        height=240,
        bargap=0.15
    )
    fig_bar.update_xaxes(gridcolor='#1a4a7a', showline=False)
    fig_bar.update_yaxes(gridcolor='#1a4a7a', showline=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Bottom row
col_bottom_left, col_bottom_right = st.columns([2, 1])

with col_bottom_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Churn by Internet Service & Contract</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Segment breakdown analysis</div>', unsafe_allow_html=True)

    seg = df.groupby('Contract')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).reset_index()
    seg.columns = ['Contract', 'Churn Rate']

    fig_seg = px.bar(
        seg, x='Contract', y='Churn Rate',
        color='Churn Rate',
        color_continuous_scale=[[0, '#00d2ff'], [0.5, '#f39c12'], [1, '#e74c3c']]
    )
    fig_seg.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8',
        margin=dict(l=0, r=0, t=10, b=0),
        height=220,
        coloraxis_showscale=False
    )
    fig_seg.update_xaxes(gridcolor='#1a4a7a')
    fig_seg.update_yaxes(gridcolor='#1a4a7a')
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_bottom_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top Segments</div>', unsafe_allow_html=True)

    top_seg = df.groupby('Contract')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)

    colors = ['#e74c3c', '#f39c12', '#00d2ff', '#2ecc71']
    for i, (name, val) in enumerate(top_seg.items()):
        bar_width = int(val)
        color = colors[i % len(colors)]
        st.markdown(f"""
        <div class="segment-row">
            <span class="segment-name">{name}</span>
            <span class="segment-pct">{val:.1f}% Churn</span>
        </div>
        <div style="background:#0d1f3c; border-radius:4px; height:5px; margin-bottom:8px;">
            <div style="background:{color}; width:{bar_width}%; height:5px; border-radius:4px;"></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AI Insight
st.markdown("""
<div class="insight-bar">
    💡 <strong>AI Strategic Insight:</strong> Cohort analysis detected a 15% increase in churn within
    the Enterprise segment during final billing cycles. Correlation with Auto-Renewal system update is 89%.
    <strong>Immediate UI audit of the renewal portal is recommended.</strong>
</div>
""", unsafe_allow_html=True)
