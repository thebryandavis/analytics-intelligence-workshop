# Analytics Intelligence Playbook

## Overview

This playbook provides step-by-step guidance for deploying and maintaining your analytics intelligence system in production.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Deployment Options](#deployment-options)
3. [Configuration](#configuration)
4. [Check Patterns Library](#check-patterns-library)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)
7. [Cost Optimization](#cost-optimization)

---

## Quick Start

### From Workshop to Production (30 minutes)

**Step 1: Prepare Your Data** (10 min)

Load your actual analytics data into BigQuery:

```bash
# Create dataset
bq mk --dataset YOUR_PROJECT:analytics

# Load from Google Analytics 4 export (if applicable)
# GA4 automatically exports to BigQuery - just link your property

# Or load from CSV/JSON
bq load --source_format=CSV \
  analytics.events \
  gs://your-bucket/events.csv \
  schema.json
```

**Step 2: Customize Checks** (10 min)

Edit `config/checks.yaml`:

```yaml
checks:
  - name: "Your Custom Check"
    description: |
      Describe what to check in natural language.
      The AI will generate SQL based on this description.
    enabled: true
```

Test locally:

```bash
python -c "
from src.analytics_intelligence import CheckRunner, BigQueryConnector, SQLGenerator, AnomalyClassifier
import os

bq = BigQueryConnector('YOUR_PROJECT', 'analytics', 'events')
sql_gen = SQLGenerator(os.environ['OPENAI_API_KEY'])
classifier = AnomalyClassifier(os.environ['OPENAI_API_KEY'])
runner = CheckRunner(bq, sql_gen, classifier)

results = runner.run_all_checks('config/checks.yaml')
print(f'Ran {len(results)} checks')
"
```

**Step 3: Deploy** (10 min)

Choose deployment method (GitHub Actions recommended):

```yaml
# .github/workflows/analytics-check.yml
name: Analytics Intelligence
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      - run: |
          pip install -r requirements.txt
          python run_checks.py --config config/checks.yaml
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

Push to GitHub, enable Actions, done!

---

## Deployment Options

### Option 1: GitHub Actions (Recommended)

**Pros:**
- Free for public repos
- Easy setup (just push YAML file)
- Built-in secrets management
- Logs in GitHub UI

**Cons:**
- Requires GitHub account
- 6-hour minimum schedule interval (for free tier)

**Setup:**

1. Create `.github/workflows/analytics-check.yml` (see above)
2. Add secrets in repo settings:
   - `OPENAI_API_KEY`
   - `SLACK_WEBHOOK`
   - `GCP_SA_KEY` (service account JSON)
3. Push and enable Actions

**Cost:** Free (public) or ~$0.01/run (private)

---

### Option 2: Google Cloud Functions

**Pros:**
- Native BigQuery integration
- Serverless (scales automatically)
- Generous free tier

**Cons:**
- Requires GCP setup
- Cold start latency

**Setup:**

```bash
# Create function
gcloud functions deploy analytics-intelligence \
  --runtime python310 \
  --trigger-http \
  --entry-point run_checks \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,SLACK_WEBHOOK=$SLACK_WEBHOOK

# Schedule with Cloud Scheduler
gcloud scheduler jobs create http analytics-check \
  --schedule "0 */6 * * *" \
  --uri "https://REGION-PROJECT.cloudfunctions.net/analytics-intelligence"
```

`main.py`:
```python
import functions_framework
from src.analytics_intelligence import CheckRunner, BigQueryConnector, SQLGenerator, AnomalyClassifier, SlackAlerter
import os

@functions_framework.http
def run_checks(request):
    bq = BigQueryConnector(os.environ['GCP_PROJECT'], 'analytics', 'events')
    sql_gen = SQLGenerator(os.environ['OPENAI_API_KEY'])
    classifier = AnomalyClassifier(os.environ['OPENAI_API_KEY'])
    alerter = SlackAlerter(os.environ['SLACK_WEBHOOK'])

    runner = CheckRunner(bq, sql_gen, classifier, alerter)
    results = runner.run_all_checks('config/checks.yaml')

    return {'status': 'success', 'checks_run': len(results)}
```

**Cost:** ~$0 (free tier covers 2M invocations/month)

---

### Option 3: AWS Lambda

**Pros:**
- Serverless
- Generous free tier
- Integrates with AWS ecosystem

**Cons:**
- Requires BigQuery client authentication
- More complex than GCP for BigQuery access

**Setup:**

```bash
# Package dependencies
pip install -r requirements.txt -t package/
cp -r src package/
cd package && zip -r ../lambda.zip . && cd ..

# Deploy
aws lambda create-function \
  --function-name analytics-intelligence \
  --runtime python3.10 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution

# Schedule with EventBridge
aws events put-rule --name analytics-check --schedule-expression "rate(6 hours)"
aws events put-targets --rule analytics-check --targets "Id=1,Arn=arn:aws:lambda:REGION:ACCOUNT:function:analytics-intelligence"
```

**Cost:** ~$0 (free tier covers 1M requests/month)

---

### Option 4: Cron Job on Server

**Pros:**
- Simple
- Full control
- No external dependencies

**Cons:**
- Requires a server
- You manage uptime

**Setup:**

```bash
# Clone repo on server
git clone <repo> /opt/analytics-intelligence
cd /opt/analytics-intelligence
pip install -r requirements.txt

# Set up environment
echo "export OPENAI_API_KEY='sk-...'" >> ~/.bashrc
echo "export SLACK_WEBHOOK='https://hooks.slack.com/...'" >> ~/.bashrc
source ~/.bashrc

# Add to crontab
crontab -e
# Add: 0 */6 * * * cd /opt/analytics-intelligence && python run_checks.py --config config/checks.yaml
```

**Cost:** $0 (using existing server)

---

### Option 5: Airflow / Dagster

**Pros:**
- Complex workflow support
- Retries, dependencies, alerting
- Great for multi-step pipelines

**Cons:**
- Overkill for simple checks
- Requires Airflow/Dagster setup

**When to use:** If you already have Airflow/Dagster or need complex multi-step workflows.

---

## Configuration

### Check Configuration (`config/checks.yaml`)

```yaml
checks:
  - name: "Descriptive Name"
    description: |
      Natural language description of what to check.
      Be specific about:
      - What to look for
      - What values are suspicious
      - How to group/aggregate results
      - What columns to return
    enabled: true
    examples: |  # Optional: few-shot learning
      Example SQL style:
      ```sql
      WITH base AS (SELECT ...)
      SELECT * FROM base WHERE ...
      ```
```

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."
export GCP_PROJECT="your-project-id"

# Optional
export SLACK_WEBHOOK="https://hooks.slack.com/services/..."
export BIGQUERY_DATASET="analytics"
export BIGQUERY_TABLE="events"
export OPENAI_MODEL="gpt-3.5-turbo"  # or gpt-4
```

---

## Check Patterns Library

### Data Quality Checks

**Missing Required Fields**
```yaml
description: |
  Find events where required fields are NULL.
  Check: user_pseudo_id, event_name, event_timestamp.
  Group by event_date and show counts.
```

**Schema Changes**
```yaml
description: |
  Detect new or removed fields by comparing recent events to baseline.
  Look for fields that appear in historical data but not recent (removed)
  or fields that appear recently but not historically (added).
```

### Tracking Breaks

**Event Volume Drop**
```yaml
description: |
  Find days where total event count drops > 30% from 7-day average.
  Calculate daily totals, baseline average, percentage change.
  Flag significant drops.
```

**Platform-Specific Breaks**
```yaml
description: |
  Detect when events from a specific platform (iOS/Android/web) drop abnormally.
  Compare hourly counts by platform to baseline.
  Flag drops > 50%.
```

**Event Type Disappearance**
```yaml
description: |
  Find event_name values that appeared in past but not in last 24 hours.
  This indicates tracking code was removed or is broken.
```

### Privacy & Compliance

**PII Detection**
```yaml
description: |
  Find personally identifiable information in event fields.
  Check for email patterns, phone numbers, SSN patterns in:
  - page_location URLs
  - Custom dimensions
  - Event parameters
  Use REGEXP_CONTAINS for pattern matching.
```

**Consent Tracking**
```yaml
description: |
  Verify consent_state is present for EU users (GDPR compliance).
  Filter to EU countries: geo_country IN ('GB', 'DE', 'FR', ...).
  Flag events missing consent_state.
```

### Opportunity Detection

**Conversion Spike**
```yaml
description: |
  Find days where conversion events (signup, purchase, etc.) increased > 30%.
  Calculate daily conversion counts and compare to 7-day average.
  Flag significant increases as opportunities.
```

**New High-Value Traffic**
```yaml
description: |
  Find referrer sources with above-average engagement or conversion.
  Calculate avg engagement_time and conversion rate per referrer.
  Flag sources performing > 1.5x better than baseline.
```

**Content Performance**
```yaml
description: |
  Detect articles or content sections with unusually high engagement.
  Compare recent performance to historical average.
  Flag content with > 2x average engagement.
```

---

## Monitoring & Maintenance

### Health Checks

Monitor your monitoring system:

1. **Check runs successfully**: Set up dead-man switch (e.g., healthchecks.io)
2. **API quotas**: Monitor OpenAI and BigQuery usage
3. **Alert delivery**: Test Slack webhooks monthly
4. **False positive rate**: Review classifications for accuracy

### Weekly Review

- Review Slack alerts from past week
- Identify noisy checks (too many alerts)
- Tune thresholds or disable low-value checks
- Add new checks based on recent issues

### Monthly Maintenance

- Update check descriptions based on tracking changes
- Review cost (OpenAI + BigQuery)
- Audit check effectiveness (% finding real issues)
- Update documentation for new team members

---

## Troubleshooting

### Problem: Too Many Alerts (Alert Fatigue)

**Solution:**
1. Increase thresholds (e.g., 30% → 50% drop)
2. Disable low-value checks
3. Add "quiet hours" (don't alert nights/weekends)
4. Use severity filtering (only alert on high-severity)

```python
# In src/analytics_intelligence.py, SlackAlerter.send_alert()
if classification['severity'] == 'low':
    return  # Don't send low-severity alerts
```

### Problem: False Positives

**Solution:**
- Add context to check descriptions ("...but ignore weekends" or "...exclude bot traffic")
- Improve SQL with EXCLUDE/WHERE clauses
- Classify results as "noise" if not actionable

### Problem: Missing Real Issues

**Solution:**
- Add more checks to `checks.yaml`
- Lower thresholds (50% → 30%)
- Enable all checks temporarily to discover blind spots

### Problem: High API Costs

**Solution:**
1. Use `gpt-3.5-turbo` instead of `gpt-4`:
   ```python
   SQLGenerator(api_key, model="gpt-3.5-turbo")
   ```
2. Reduce check frequency (6 hours → 12 hours)
3. Use SQL-only checks (skip AI classification for simple checks)
4. Cache SQL queries (regenerate weekly, not daily)

### Problem: BigQuery Quota Exceeded

**Solution:**
- Add `LIMIT` clauses to queries
- Partition tables by date and query only recent data
- Use materialized views for common queries
- Request quota increase

---

## Cost Optimization

### Current Costs (Example)

**Assumptions:**
- 20 checks per run
- Running every 6 hours (4x/day)
- 30 days/month

**OpenAI (GPT-4):**
- 40 API calls/day (2 per check: SQL gen + classification)
- ~$0.06/call = $2.40/day = **$72/month**

**OpenAI (GPT-3.5-turbo):**
- 40 API calls/day
- ~$0.002/call = $0.08/day = **$2.40/month**

**BigQuery:**
- ~1 GB scanned per check = 20 GB/run
- 80 GB/day = 2.4 TB/month
- $5/TB after free tier = **~$12/month**

**Compute (GitHub Actions):**
- **$0** (free tier)

**Total (GPT-3.5):** ~$15/month
**Total (GPT-4):** ~$85/month

### Optimization Strategies

1. **Hybrid Model**: Use GPT-3.5 for SQL generation, GPT-4 for classification only
   - Savings: ~40%

2. **Smart Sampling**: Only run expensive checks once/day, cheap checks hourly
   ```yaml
   - name: "Expensive Check"
     schedule: "0 6 * * *"  # Daily at 6am
   ```

3. **Cache SQL**: Generate SQL once, reuse for 7 days
   - Saves 50% of OpenAI calls

4. **Incremental Checks**: Query only new data since last run
   ```sql
   WHERE event_timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
   ```
   - Reduces BigQuery costs by 75%

5. **Batch Classifications**: Classify multiple findings in one API call
   - Reduces API calls by up to 50%

---

## Best Practices

### Check Design

1. **Be specific**: "Find iOS scroll_depth events < 100/hour" vs "Find problems"
2. **Include context**: Mention thresholds, time ranges, expected values
3. **Group smartly**: Aggregate to reduce result rows (GROUP BY date, platform)
4. **Limit results**: Use LIMIT to control API costs and alert size

### Alert Design

1. **Actionable**: Every alert should suggest a next step
2. **Contextual**: Include comparison to baseline ("30% below average")
3. **Prioritized**: Use severity levels (critical/minor)
4. **Timely**: Alert quickly for critical issues, batch minor issues

### Team Workflow

1. **Shared responsibility**: Rotate who triages alerts weekly
2. **Document fixes**: When you fix an issue, update playbook
3. **Review false positives**: Weekly meeting to tune checks
4. **Celebrate wins**: Share opportunities discovered via system

---

## Advanced Topics

### Custom Classifiers

Override default classification logic:

```python
from src.analytics_intelligence import AnomalyClassifier

class CustomClassifier(AnomalyClassifier):
    def classify(self, check_name, check_description, results, context=None):
        # Your custom logic
        if "revenue" in check_name.lower() and len(results) > 0:
            return {
                'category': 'problem_critical',
                'severity': 'high',
                'title': 'Revenue tracking issue detected',
                # ...
            }
        return super().classify(check_name, check_description, results, context)
```

### Multi-Source Monitoring

Monitor multiple BigQuery tables or projects:

```python
sources = [
    ('project1', 'dataset1', 'events'),
    ('project2', 'dataset2', 'events'),
]

for project, dataset, table in sources:
    bq = BigQueryConnector(project, dataset, table)
    runner = CheckRunner(bq, sql_gen, classifier, alerter)
    runner.run_all_checks(f'config/checks_{project}.yaml')
```

### Integration with Other Tools

- **Datadog**: Send metrics via API
- **PagerDuty**: Critical alerts via PagerDuty API
- **Jira**: Auto-create tickets for problems
- **Grafana**: Visualize check results over time

---

## Getting Help

- **Workshop materials**: This playbook
- **Community**: NPA Slack #analytics-intelligence
- **Bryan Davis**: bryan.davis@ap.org

---

**Last updated:** 2025-01-11
**Version:** 1.0
