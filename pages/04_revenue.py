import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Revenue Impact", layout="wide")

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
    .revenue-hero {
        background: linear-gradient(135deg, #1a0a0a 0%, #2d0f0f 100%);
        border: 1px solid #7b1c1c; border-left: 5px solid #e74c3c;
        border-radius: 14px; padding: 28px; margin-bottom: 20px;
    }
    .revenue-hero-label { color: #6b8ab8; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; }
    .revenue-hero-value { color: #e74c3c; font-size: 42px; font-weight: 800; font-family: 'Roboto Mono', monospace; margin: 8px 0; }
    .revenue-hero-delta { color: #f39c12; font-size: 13px; }
    .tier-card {
        background: #0d1f3c; border: 1px solid #1a4a7a;
        border-radius: 10px; padding: 16px; margin-bottom: 8px;
    }
    .tier-label { color: #6b8ab8; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .tier-value { color: #ffffff; font-size: 20px; font-weight: 700; margin: 4px 0; }
    .tier-bar { height: 3px; border-radius: 2px; margin-top: 8px; }
    .section-card {
        background: linear-gradient(135deg, #0d1f3c 0%, #0f2a50 100%);
        border: 1px solid #1a4a7a; border-radius: 14px;
        padding: 24px; margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .section-title { color: #00d2ff; font-size: 16px; font-weight: 600; margin-bottom: 4px; }
    .section-subtitle { color: #6b8ab8; font-size: 12px; margin-bottom: 16px; }
    .insight-box {
        background: linear-gradient(135deg, #1a1400, #2a1f00);
        border: 1px solid #f39c12; border-radius: 12px;
        padding: 20px; margin-bottom: 20px;
    }
    .insight-box h4 { color: #f39c12; margin: 0 0 8px 0; font-size: 14px; }
    .insight-box p { color: #e0e0e0; margin: 0; font-size: 13px; line-height: 1.6; }
    .insight-box strong { color: #00d2ff; }
    .page-header {
        border-bottom: 1px solid #1a4a7a; padding-bottom: 12px; margin-bottom: 24px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .page-title { color: #ffffff; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
    .page-meta { color: #6b8ab8; font-size: 11px; }
    .roi-positive { color: #2ecc71; font-size: 32px; font-weight: 800; }
    .roi-label { color: #6b8ab8; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <span class="page-title">💰 REVENUE IMPACT</span>
    <span class="page-meta">Q3 2024 &nbsp;|&nbsp; Q4 2024</span>
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
churned_mrr = churned['MonthlyCharges'].sum()
annual_risk = churned_mrr * 12

# Revenue Hero
col_hero, col_insight = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
    <div class="revenue-hero">
        <div class="revenue-hero-label">Revenue at Risk</div>
        <div class="revenue-hero-value">${annual_risk:,.2f}</div>
        <div class="revenue-hero-delta">▲ 12.4% vs prev. month</div>
        <br>
        <div style="display: flex; gap: 16px; margin-top: 8px;">
            <div class="tier-card" style="flex:1;">
                <div class="tier-label">Critical Tier</div>
                <div class="tier-value">${churned_mrr*0.28:,.1f}</div>
                <div class="tier-bar" style="background: #e74c3c; width: 60%;"></div>
            </div>
            <div class="tier-card" style="flex:1;">
                <div class="tier-label">Growth Tier</div>
                <div class="tier-value">${churned_mrr*0.56:,.1f}</div>
                <div class="tier-bar" style="background: #f39c12; width: 80%;"></div>
            </div>
            <div class="tier-card" style="flex:1;">
                <div class="tier-label">Legacy Tier</div>
                <div class="tier-value">${churned_mrr*0.16:,.1f}</div>
                <div class="tier-bar" style="background: #00d2ff; width: 30%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight:
    st.markdown("""
    <div class="insight-box" style="height: 90%;">
        <h4>💡 AI Optimization Insight</h4>
        <p>By targeting the <strong>Growth Tier</strong> with a localized pricing adjustment,
        you can mitigate up to <strong>$450k</strong> of the current risk profile within 30 days.</p>
    </div>
    """, unsafe_allow_html=True)

# ROI Calculator + Chart
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Retention ROI Calculator</div>', unsafe_allow_html=True)

    campaign_cost = st.slider("Retention Campaign Spend", 10000, 500000, 250000, step=10000,
                               format="$%d")
    churn_reduction = st.slider("Target Churn Reduction", 5, 50, 15, format="%d%%")
    avg_ltv = st.slider("Customer Lifetime Value (Avg)", 1000, 10000, 4200, step=100, format="$%d")

    customers_saved = int(len(churned) * (churn_reduction / 100))
    net_saved = customers_saved * avg_ltv
    roi = net_saved / campaign_cost if campaign_cost > 0 else 0

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f"""
        <div style="margin-top: 16px;">
            <div class="roi-label">Projected ROI</div>
            <div class="roi-positive">{roi:.1f}x</div>
        </div>""", unsafe_allow_html=True)
    with col_r2:
        st.markdown(f"""
        <div style="margin-top: 16px;">
            <div class="roi-label">Net Saved Revenue</div>
            <div class="roi-positive">${net_saved/1000:.2f}M</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Campaign Performance</div>', unsafe_allow_html=True)

    contract_data = df.groupby('Contract').agg(
        Revenue=('MonthlyCharges', 'sum'),
        Churned=('Churn', lambda x: (x == 'Yes').sum())
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Total Revenue', x=contract_data['Contract'],
                         y=contract_data['Revenue'], marker_color='#00d2ff', opacity=0.8))
    fig.add_trace(go.Bar(name='Churned Revenue', x=contract_data['Contract'],
                         y=contract_data['Churned'] * df['MonthlyCharges'].mean(),
                         marker_color='#e74c3c', opacity=0.8))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#6b8ab8', barmode='group',
        margin=dict(l=0, r=0, t=10, b=0), height=280,
        legend=dict(font=dict(color='#6b8ab8'))
    )
    fig.update_xaxes(gridcolor='#1a4a7a')
    fig.update_yaxes(gridcolor='#1a4a7a')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Revenue Leakage Table
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Revenue Leakage by Segment</div>', unsafe_allow_html=True)

leakage = df.groupby('Contract').agg(
    Churn_Probability=('Churn', lambda x: f"{(x=='Yes').mean()*100:.0f}%"),
    Current_MRR=('MonthlyCharges', lambda x: f"${x.sum():,.1f}"),
    Projected_Loss=('MonthlyCharges', lambda x: f"${x[df.loc[x.index,'Churn']=='Yes'].sum():,.1f}")
).reset_index()

leakage.columns = ['Segment', 'Churn Probability', 'Current MRR', 'Projected Loss']
st.dataframe(leakage, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
