# Workshop Notebooks

## Google Colab Notebooks (Recommended)

These run in your browser, no setup required:

1. **[Setup & First Query](COLAB_01_setup_and_first_query.ipynb)**
   - Connect to BigQuery
   - Explore 3.5M sample events
   - Find your first data quality issue

2. **[AI-Generated SQL Checks](COLAB_02_ai_generated_sql_checks.ipynb)**
   - Generate SQL from plain English
   - Detect tracking breaks and PII leaks
   - Discover opportunities (traffic spikes, new referrers)

3. **[Anomaly Detection & Alerts](COLAB_03_anomaly_detection_and_alerts.ipynb)**
   - Classify findings with AI
   - Send Slack alerts automatically
   - Configure for production deployment

## How to Use

### For Colab (No Setup Required)
1. Click a notebook link above
2. Click "Copy to Drive" at the top
3. Run cells with the ▶️ button
4. That's it!

### For Local Jupyter
```bash
# Install dependencies
pip install -r ../requirements.txt

# Set environment variables
export OPENAI_API_KEY="sk-..."
export GCP_PROJECT="your-project-id"

# Launch Jupyter
jupyter notebook
```

## First Time Using Colab?

Colab is like Google Docs for code:
- Runs in your browser
- Nothing to install
- Auto-saves to your Drive
- Click play buttons to run code

## Need Help?


- **After workshop:** Email brdavis@ap.org

