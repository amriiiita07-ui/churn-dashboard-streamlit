"""
app.py
======
Home page / Landing page for the Churn Intelligence Dashboard.
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

# Custom CSS for dark teal theme
st.markdown("""
<style>
    .main {
        background-color: #0a1628;
    }
    .stApp {
        background-color: #0a1628;
    }
    .project-card {
        background-color: #0f3460;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #00d2ff;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .project-card:hover {
        transform: translateX(10px);
        border-left: 5px solid #ff6b6b;
    }
    .project-title {
        color: #00d2ff;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .project-desc {
        color: #e0e0e0;
        font-size: 14px;
        line-height: 1.6;
    }
    .main-title {
        color: #00d2ff;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .subtitle {
        color: #a0a0a0;
        text-align: center;
        font-size: 18px;
        margin-bottom: 40px;
    }
    .dataset-info {
        background-color: #162447;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00d2ff;
        margin-top: 30px;
    }
    .dataset-title {
        color: #00d2ff;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .dataset-text {
        color: #c0c0c0;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="main-title">📊 Customer Churn Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">End-to-end analytics system for revenue protection & customer retention</div>', unsafe_allow_html=True)

st.markdown("---")

# Project Architecture Section
st.markdown('<h2 style="color: #00d2ff; margin-bottom: 25px;">🏗️ Project Architecture</h2>', unsafe_allow_html=True)

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

# Dataset Info
st.markdown("""
<div class="dataset-info">
    <div class="dataset-title">📊 Dataset: IBM Telco Customer Churn</div>
    <div class="dataset-text">
        <strong>Records:</strong> 7,043 customers | <strong>Features:</strong> 21 columns<br>
        <strong>Source:</strong> Kaggle (blastchar/telco-customer-churn)<br>
        <strong>Last Updated:</strong> Auto-refreshed on load<br>
        <strong>Key Metrics:</strong> Churn rate, tenure, monthly charges, contract type, services
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Navigation
# Quick Navigation
st.markdown("---")
st.markdown('<h3 style="color: #00d2ff; text-align: center;">🚀 Navigate Using the Sidebar</h3>', unsafe_allow_html=True)

st.info("👈 Click the pages in the left sidebar to navigate: Executive Summary, Risk Scoring, Cohort Analysis, Revenue Impact.")

# Optional: Display page previews as static cards (no buttons, no switching)
preview_col1, preview_col2 = st.columns(2)
with preview_col1:
    st.markdown("""
    <div style="background-color: #0f3460; padding: 20px; border-radius: 10px; border-left: 4px solid #00d2ff; margin-bottom: 15px;">
        <div style="color: #00d2ff; font-weight: bold; font-size: 16px;">📊 Executive Summary</div>
        <div style="color: #c0c0c0; font-size: 13px; margin-top: 5px;">KPIs, churn overview, and key metrics dashboard</div>
    </div>
    <div style="background-color: #0f3460; padding: 20px; border-radius: 10px; border-left: 4px solid #ffd93d; margin-bottom: 15px;">
        <div style="color: #ffd93d; font-weight: bold; font-size: 16px;">👥 Cohort Analysis</div>
        <div style="color: #c0c0c0; font-size: 13px; margin-top: 5px;">Retention curves and cohort behavior over time</div>
    </div>
    """, unsafe_allow_html=True)

with preview_col2:
    st.markdown("""
    <div style="background-color: #0f3460; padding: 20px; border-radius: 10px; border-left: 4px solid #ff6b6b; margin-bottom: 15px;">
        <div style="color: #ff6b6b; font-weight: bold; font-size: 16px;">🎯 Risk Scoring</div>
        <div style="color: #c0c0c0; font-size: 13px; margin-top: 5px;">Customer risk segmentation and prediction models</div>
    </div>
    <div style="background-color: #0f3460; padding: 20px; border-radius: 10px; border-left: 4px solid #6bcb77; margin-bottom: 15px;">
        <div style="color: #6bcb77; font-weight: bold; font-size: 16px;">💰 Revenue Impact</div>
        <div style="color: #c0c0c0; font-size: 13px; margin-top: 5px;">Revenue at risk and financial impact calculations</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #666; font-size: 12px;">
    Built with Python | SQL | Streamlit | Plotly | Kaplan-Meier Survival Analysis
</p>
""", unsafe_allow_html=True)
