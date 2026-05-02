"""
app.py
======
Home page / Landing page for the Churn Intelligence Dashboard.
Soft Lavender + White + Pastel Pink theme with Nunito font.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="Churn Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');

/* ── GLOBAL RESET ── */
*, *::before, *::after {
    font-family: 'Nunito', sans-serif !important;
    box-sizing: border-box;
}

/* ── PAGE BACKGROUND ── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #F5F3FF !important;
}

[data-testid="stMain"], .main, section.main {
    background-color: #F5F3FF !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #EDE9FE !important;
}

[data-testid="stSidebar"] * {
    color: #4C3D8A !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #EDE9FE !important;
}

/* ── HEADINGS ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 900 !important;
    color: #1E1B4B !important;
    letter-spacing: -0.3px;
}

/* ── BODY TEXT ── */
p, span, div, label, li {
    font-family: 'Nunito', sans-serif !important;
}

/* ── DIVIDER ── */
hr {
    border-color: #EDE9FE !important;
    margin: 1.2rem 0 !important;
}

/* ── STREAMLIT INFO BOX ── */
[data-testid="stAlert"] {
    background-color: #FAF5FF !important;
    border: 1px solid #DDD6FE !important;
    border-radius: 14px !important;
    color: #4C3D8A !important;
    font-weight: 600 !important;
}

/* ── MAIN TITLE BLOCK ── */
.main-title {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 40px;
    color: #1E1B4B;
    text-align: center;
    letter-spacing: -0.8px;
    margin-bottom: 6px;
}

.subtitle {
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: #7C6FAB;
    text-align: center;
    margin-bottom: 30px;
}

/* ── PROJECT CARDS ── */
.project-card {
    background-color: #FFFFFF;
    padding: 22px 24px;
    border-radius: 18px;
    border-left: 5px solid #A78BFA;
    margin: 12px 0;
    border: 1px solid #EDE9FE;
    border-left: 5px solid #A78BFA;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.project-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(167, 139, 250, 0.18);
    border-left-color: #7C3AED;
}

.project-title {
    font-family: 'Nunito', sans-serif;
    color: #7C3AED;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.2px;
}

.project-desc {
    font-family: 'Nunito', sans-serif;
    color: #6B6494;
    font-size: 13px;
    line-height: 1.65;
    font-weight: 500;
}

/* ── DATASET INFO BLOCK ── */
.dataset-info {
    background-color: #FFFFFF;
    padding: 22px 26px;
    border-radius: 18px;
    border: 1px solid #EDE9FE;
    border-top: 4px solid #C4B5FD;
    margin-top: 28px;
}

.dataset-title {
    font-family: 'Nunito', sans-serif;
    color: #7C3AED;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -0.2px;
}

.dataset-text {
    font-family: 'Nunito', sans-serif;
    color: #5C5380;
    font-size: 14px;
    line-height: 1.8;
    font-weight: 500;
}

/* ── SECTION HEADER ── */
.section-header {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 24px;
    color: #1E1B4B;
    margin-bottom: 20px;
    letter-spacing: -0.4px;
}

/* ── PREVIEW NAVIGATION CARDS ── */
.nav-card-purple {
    background-color: #FFFFFF;
    padding: 20px 22px;
    border-radius: 16px;
    border: 1px solid #EDE9FE;
    border-left: 4px solid #A78BFA;
    margin-bottom: 14px;
    transition: transform 0.2s ease;
}

.nav-card-purple:hover { transform: translateY(-2px); }

.nav-card-pink {
    background-color: #FFFFFF;
    padding: 20px 22px;
    border-radius: 16px;
    border: 1px solid #FCE4EC;
    border-left: 4px solid #F9A8D4;
    margin-bottom: 14px;
    transition: transform 0.2s ease;
}

.nav-card-pink:hover { transform: translateY(-2px); }

.nav-title-purple {
    font-family: 'Nunito', sans-serif;
    color: #7C3AED;
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 4px;
}

.nav-title-pink {
    font-family: 'Nunito', sans-serif;
    color: #BE185D;
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 4px;
}

.nav-desc {
    font-family: 'Nunito', sans-serif;
    color: #7C6FAB;
    font-size: 12px;
    font-weight: 500;
    line-height: 1.5;
}

/* ── FOOTER ── */
.footer-text {
    font-family: 'Nunito', sans-serif;
    text-align: center;
    color: #A8A5C0;
    font-size: 12px;
    font-weight: 600;
    margin-top: 10px;
}

/* ── STREAMLIT BLOCK CONTAINER PADDING ── */
[data-testid="stVerticalBlock"] {
    gap: 0rem;
}

/* ── METRIC OVERRIDES (for pages that use st.metric) ── */
[data-testid="metric-container"] {
    background-color: #FFFFFF !important;
    border: 1px solid #EDE9FE !important;
    border-radius: 16px !important;
    padding: 18px !important;
}

[data-testid="metric-container"] label,
[data-testid="stMetricLabel"] {
    font-family: 'Nunito', sans-serif !important;
    font-size: 10px !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    color: #A78BFA !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Nunito', sans-serif !important;
    font-size: 26px !important;
    font-weight: 900 !important;
    color: #A78BFA !important;
    letter-spacing: -0.5px !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Nunito', sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #7C6FAB !important;
}

/* ── PLOTLY CHART CONTAINERS ── */
[data-testid="stPlotlyChart"] {
    border-radius: 16px !important;
    overflow: hidden;
    border: 1px solid #EDE9FE !important;
    background: #FFFFFF !important;
}

/* ── DATAFRAME / TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden;
    border: 1px solid #EDE9FE !important;
}

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    background-color: #7C3AED !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.01em;
    transition: background 0.2s ease;
}

.stButton > button:hover {
    background-color: #6D28D9 !important;
}

/* ── SELECT / INPUT ── */
.stSelectbox > div, .stTextInput > div {
    border-radius: 12px !important;
    border-color: #DDD6FE !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F5F3FF; }
::-webkit-scrollbar-thumb { background: #C4B5FD; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #A78BFA; }

</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📊 Customer Churn Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">End-to-end analytics system for revenue protection & customer retention</div>', unsafe_allow_html=True)
st.markdown("---")


# ── PROJECT ARCHITECTURE ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏗️ Project Architecture</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <div class="project-title">📁 churn-data-pipeline/</div>
        <div class="project-desc">Data ingestion, cleaning & synthetic data generation. Handles missing values, outliers, and feature engineering.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="project-card">
        <div class="project-title">📁 churn-sql-analytics/</div>
        <div class="project-desc">SQL queries with CTEs, window functions, and cohort analysis. Interview-ready database operations.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="project-card">
        <div class="project-title">📁 churn-python-analysis/</div>
        <div class="project-desc">EDA, Kaplan-Meier survival curves, risk scoring models, and feature engineering pipelines.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <div class="project-title">📁 churn-dashboard-streamlit/</div>
        <div class="project-desc">This interactive web dashboard with real-time KPIs, risk tables, and ROI calculator.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="project-card">
        <div class="project-title">📁 churn-powerbi-guide/</div>
        <div class="project-desc">Power BI implementation guide with DAX measures, layout instructions, and data model docs.</div>
    </div>
    """, unsafe_allow_html=True)


# ── DATASET INFO ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="dataset-info">
    <div class="dataset-title">📊 Dataset: IBM Telco Customer Churn</div>
    <div class="dataset-text">
        <strong>Records:</strong> 7,043 customers &nbsp;|&nbsp;
        <strong>Features:</strong> 21 columns<br>
        <strong>Source:</strong> Kaggle (blastchar/telco-customer-churn)<br>
        <strong>Last Updated:</strong> Auto-refreshed on load<br>
        <strong>Key Metrics:</strong> Churn rate, tenure, monthly charges, contract type, services
    </div>
</div>
""", unsafe_allow_html=True)


# ── NAVIGATION ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header" style="text-align:center; font-size:20px;">🚀 Navigate Using the Sidebar</div>', unsafe_allow_html=True)
st.info("👈 Click the pages in the left sidebar to navigate: Executive Summary, Risk Scoring, Cohort Analysis, Revenue Impact.")

preview_col1, preview_col2 = st.columns(2)

with preview_col1:
    st.markdown("""
    <div class="nav-card-purple">
        <div class="nav-title-purple">📊 Executive Summary</div>
        <div class="nav-desc">KPIs, churn overview, and key metrics dashboard</div>
    </div>
    <div class="nav-card-purple">
        <div class="nav-title-purple">👥 Cohort Analysis</div>
        <div class="nav-desc">Retention curves and cohort behavior over time</div>
    </div>
    """, unsafe_allow_html=True)

with preview_col2:
    st.markdown("""
    <div class="nav-card-pink">
        <div class="nav-title-pink">🎯 Risk Scoring</div>
        <div class="nav-desc">Customer risk segmentation and prediction models</div>
    </div>
    <div class="nav-card-pink">
        <div class="nav-title-pink">💰 Revenue Impact</div>
        <div class="nav-desc">Revenue at risk and financial impact calculations</div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class="footer-text">
    Built with Python &nbsp;|&nbsp; SQL &nbsp;|&nbsp; Streamlit &nbsp;|&nbsp; Plotly &nbsp;|&nbsp; Kaplan-Meier Survival Analysis
</div>
""", unsafe_allow_html=True)
