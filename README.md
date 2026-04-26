# churn-dashboard-streamlit

## Business Problem
Executives and retention teams need a live, interactive view of churn risk. Static reports are outdated the moment they're exported. This dashboard updates automatically and allows drill-down exploration.

## Solution Approach
- **4 Interactive Pages**: Executive Summary, Risk Scoring, Cohort Analysis, Revenue Impact
- **"So What?" Cards**: Every page includes actionable business recommendations
- **Real-time Filtering**: Sidebar filters let users explore segments
- **CSV Export**: Download customer lists for campaigns

## Key Features
| Page | Purpose | Business Value |
|------|---------|----------------|
| Executive Summary | KPIs and high-level metrics | 30-second exec briefing |
| Risk Scoring | Ranked at-risk customer table | Weekly retention call list |
| Cohort Analysis | Retention trends over time | Product strategy insights |
| Revenue Impact | Financial exposure + ROI calculator | CFO budget justification |

## Tech Stack
- Streamlit (web framework)
- Plotly (interactive charts)
- pandas (data manipulation)

## How to Run

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Launch dashboard
streamlit run app.py
```

### Deploy Online (FREE)
1. Push this repo to GitHub
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Select this repository
5. Click Deploy

## Live Demo
Add your deployed URL here after publishing.

## Author
Built as part of a Customer Churn & Revenue Intelligence Platform portfolio project.
