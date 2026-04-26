"""
utils/charts.py
===============
Reusable chart components for the Streamlit dashboard.

WHY SEPARATE FILE:
- Consistent styling across all pages
- Easy to modify colors/themes globally
- Keeps page files clean
"""

import plotly.express as px
import plotly.graph_objects as go

# Brand colors
COLORS = {
    'high_risk': '#E74C3C',
    'medium_risk': '#F39C12', 
    'low_risk': '#2ECC71',
    'primary': '#3498DB',
    'secondary': '#9B59B6',
    'neutral': '#95A5A6'
}

RISK_COLORS = {'High Risk': '#E74C3C', 'Medium Risk': '#F39C12', 'Low Risk': '#2ECC71'}


def churn_rate_gauge(value, title="Churn Rate"):
    """Create a gauge chart for churn rate."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        number={'suffix': '%', 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 50], 'tickwidth': 1},
            'bar': {'color': COLORS['high_risk'] if value > 30 else COLORS['medium_risk'] if value > 20 else COLORS['low_risk']},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': 'gray',
            'steps': [
                {'range': [0, 20], 'color': '#d5f5e3'},
                {'range': [20, 30], 'color': '#fdebd0'},
                {'range': [30, 50], 'color': '#f5b7b1'}
            ],
            'threshold': {
                'line': {'color': 'black', 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=300)
    return fig


def risk_segment_pie(df):
    """Pie chart of risk segment distribution."""
    counts = df['risk_segment'].value_counts().reset_index()
    counts.columns = ['Risk Segment', 'Count']
    fig = px.pie(counts, values='Count', names='Risk Segment', 
                 color='Risk Segment', color_discrete_map=RISK_COLORS,
                 hole=0.4, title='Customer Risk Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def revenue_at_risk_bar(df):
    """Bar chart of revenue at risk by segment."""
    df_churned = df[df['Churn'] == 'Yes']
    revenue = df_churned.groupby('risk_segment')['MonthlyCharges'].sum().reset_index()
    revenue.columns = ['Risk Segment', 'Monthly Revenue Lost']
    fig = px.bar(revenue, x='Risk Segment', y='Monthly Revenue Lost',
                 color='Risk Segment', color_discrete_map=RISK_COLORS,
                 title='Monthly Revenue Lost by Risk Segment',
                 text='Monthly Revenue Lost')
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    return fig


def cohort_retention_heatmap(df):
    """Heatmap of retention by cohort and contract."""
    cohort_data = df.groupby(['cohort', 'Contract'])['Churn'].apply(
        lambda x: (x == 'No').mean() * 100
    ).reset_index()
    cohort_data.columns = ['Cohort', 'Contract', 'Retention Rate (%)']

    fig = px.density_heatmap(cohort_data, x='Cohort', y='Contract', 
                             z='Retention Rate (%)',
                             title='Retention Rate by Cohort & Contract',
                             color_continuous_scale='RdYlGn')
    return fig
