# Analytics Intelligence Workshop - Take-Home Guide

**News Product Alliance Summit 2025 | Bryan Davis, The Associated Press**

---

## What You Just Saw

A system that watches your analytics data 24/7 and sends Slack alerts for:
- 🚨 **Problems**: Tracking breaks, PII leaks, data quality issues
- 🎉 **Opportunities**: Traffic spikes, new referrers, behavior changes
- 📊 **Insights**: Pattern shifts, emerging trends

**Cost**: < $15/month | **Setup time**: 1-2 hours | **Skills needed**: Copy/paste

---

## How It Works

```
Plain English → GPT → SQL → BigQuery → AI Classification → Slack Alert
```

**Example:**
- You write: "Find iOS events where scroll_depth dropped below 1000/hour"
- GPT generates: Perfect BigQuery SQL
- System runs it: Finds the problem
- AI classifies it: "Critical tracking break"
- You get Slack: "🚨 iOS scroll tracking stopped at 2pm"

**No SQL expertise required**

---

## What We Found Today (In Sample Data)

### Problems Detected
1. ✅ iOS tracking break (after 2pm, Day 3)
2. ✅ 15% missing consent_state (GDPR risk)
3. ✅ PII in URLs (~3,200 events with emails)
4. ✅ ~1% duplicate events

### Opportunities Discovered
1. ✅ Newsletter signups +45% (Day 4)
2. ✅ New Reddit traffic (appeared Day 5)

**Time to find all 6**: 45 minutes (manually would take days/weeks)

---

## Your Take-Home Materials

### Code & Notebooks
- **3 Google Colab notebooks** (ready to run)
- **Complete Python module** (`analytics_intelligence.py`)
- **20+ check templates** (YAML configuration)
- **Sample data generator** (for testing)

### Documentation
- **README.md**: Setup guide with troubleshooting
- **playbook.md**: Deployment options and best practices

### Access
- **GitHub repo**: email Bryan

---

## Get Started Monday Morning

### Option 1: Quick Test (30 min)
1. Open the Colab notebooks (no install needed)
2. Use the sample data (already loaded)
3. Run through all 3 notebooks
4. See it find all 6 issues

**Perfect if**: You want to understand before deploying

---

### Option 2: Deploy to Production (2 hours)

#### Step 1: Get Data into BigQuery (30-60 min)
**If you have GA4:**
```bash
# Enable BigQuery export in GA4 settings
# Data appears automatically in BigQuery
```

**If you have CSV/JSON:**
```bash
# Load from local file
bq load --source_format=CSV mydataset.events data.csv schema.json

# Or load from Google Cloud Storage
bq load mydataset.events gs://bucket/data.csv schema.json
```

**If you stream events:**
- See `data/load_to_bigquery.py` for streaming example

---

#### Step 2: Customize Checks (15 min)
Edit `config/checks.yaml`:

```yaml
checks:
  - name: "Your Custom Check"
    description: |
      Describe what you want to check in plain English.
      Example: Find days where video_start events dropped >20%.
    enabled: true
```

Add checks for:
- Your specific event types
- Your tracking plan requirements
- Your compliance needs
- Your business metrics

---

#### Step 3: Deploy (30 min)

**Recommended: GitHub Actions (Free)**

1. Create `.github/workflows/analytics-checks.yml`:
```yaml
name: Analytics Intelligence Checks
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  run-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python run_checks.py
    env:
      GOOGLE_PROJECT_ID: ${{ secrets.GCP_PROJECT }}
      OPENAI_API_KEY: ${{ secrets.OPENAI_KEY }}
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

2. Add secrets in GitHub Settings → Secrets
3. Push code
4. It runs automatically!

**Alternative: Google Cloud Functions**
- See `docs/playbook.md` for detailed instructions
- Native BigQuery integration
- Serverless, auto-scaling

---

#### Step 4: Receive Alerts (< 10 min after deploy)
Slack alerts start arriving within hours!

---

## Costs (Monthly)

| Component | Workshop | Production (GPT-3.5) | Production (GPT-4) |
|-----------|----------|----------------------|--------------------|
| BigQuery | $0 | ~$5 | ~$5 |
| OpenAI API | $0.50 | ~$3 | ~$72 |
| Compute | $0 | $0 (GitHub Actions) | $0 |
| **Total** | **<$1** | **~$8/month** | **~$80/month** |

**Recommended**: Use GPT-3.5 (10x cheaper, works great)

**ROI**: Catch one tracking break early → save thousands in lost data

---

## Common Questions

**Q: What if I don't have BigQuery?**
A: Works with any SQL database - just change the connector. Examples for Snowflake, Redshift, PostgreSQL in playbook.

**Q: Can I use without AI?**
A: Yes! Write SQL by hand, skip generation. Classification and alerting still work.

**Q: What about false positives?**
A: Tune thresholds in `checks.yaml`. System learns your baselines over time.

**Q: How do I add custom checks?**
A: Just edit `checks.yaml` - describe in plain English, enable it, done.

**Q: Can I send alerts to other tools?**
A: Yes! Modify `SlackAlerter` class to send to PagerDuty, Jira, email, Teams, etc.

---

## Prerequisites

### Required
- **Google Cloud account** (free tier works)
- **OpenAI API key** (get at platform.openai.com)
- **Python 3.8+** (for running locally)

### Optional
- **Slack workspace** (or use email/PagerDuty/etc.)
- **GitHub account** (for GitHub Actions deployment)

---

## Check Categories (20+ Templates Included)

### Data Quality
- Missing required fields
- Invalid values
- Schema changes
- Unexpected nulls

### Tracking Breaks
- Event volume drops
- Platform-specific failures
- Event type disappearance
- Hourly pattern anomalies

### Privacy & Compliance
- PII detection (email, SSN patterns)
- Consent tracking (GDPR)
- Data retention violations

### Opportunities
- Traffic spikes
- New referral sources
- Conversion rate improvements
- Content performance outliers
- Engagement pattern changes

### Business Metrics
- Conversion rate changes
- Subscription trends
- Video play rates
- Newsletter signup patterns
- Search usage changes

---

## Customization Examples

### Check: Paywall Conversion Drop
```yaml
- name: "Paywall Conversion Drop"
  description: |
    Find days where paywall_conversion events dropped >15%
    from 7-day average. Indicates paywall implementation issue.
  enabled: true
```

### Check: High-Value Article Discovery
```yaml
- name: "Viral Article Detection"
  description: |
    Find articles that got >3x normal page views in last 24 hours.
    Opportunity to promote or create similar content.
  enabled: true
```

### Check: Mobile App Crash Pattern
```yaml
- name: "App Crash Spike"
  description: |
    Find hours where app_crash events exceed baseline by >50%.
    Critical issue affecting user experience.
  enabled: true
```

**Just describe what you want - GPT figures out the SQL!**

---

## Prompt Engineering Tips

### ✅ Good Prompts (Specific, Contextual, Actionable)
```
Find iOS events where scroll_depth count < 100/hour.
Compare to 7-day average for iOS scroll_depth.
Show: event_date, hour, ios_scroll_count, expected_count.
Flag rows where percentage deviation > 50%.
```

### ❌ Bad Prompts (Vague, No Context)
```
Check the data
Find anomalies
Look for problems
```

### Pro Tips
- Be specific about thresholds
- Provide comparison context (vs average, vs yesterday)
- Name the columns you want in output
- Specify filtering logic
- Give examples of what you're looking for

---

## Next Steps

### Immediate (Today)
1. [ ] Join workshop Slack: #analytics-intelligence
2. [ ] Star the GitHub repo
3. [ ] Download/bookmark materials

### This Week
1. [ ] Run Colab notebooks with sample data
2. [ ] Review your current tracking plan
3. [ ] Draft 5-10 custom checks
4. [ ] Get OpenAI API key
5. [ ] Get BigQuery access at your org

### This Month
1. [ ] Load your data to BigQuery
2. [ ] Customize checks.yaml
3. [ ] Deploy to GitHub Actions
4. [ ] Receive first alert
5. [ ] Share results with team

### This Quarter
1. [ ] Catch 3+ issues before they impact OKRs
2. [ ] Discover 1+ opportunities worth investigating
3. [ ] Document ROI and time saved
4. [ ] Share success story with presenter!

---

## Support & Community

### Get Help
- **Workshop Slack**: #analytics-intelligence
- **GitHub Issues**: Report bugs, request features
- **Email presenter**: bryan.davis@ap.org

### Share Your Success
- Tweet with #AnalyticsIntelligence
- Write blog post about your deployment
- Present to your team
- Contribute checks back to repo

---

## Real-World Example (The Associated Press)

**Before System:**
- Tracking breaks discovered 2-3 weeks late
- 4 hours/week manual data quality checks
- Opportunities found only in retrospect

**After System:**
- Alerts within 6 hours of issue
- 0 hours/week manual checking
- 5+ opportunities/quarter discovered early

**Example Win:**
Newsletter spike detected same day → investigated → found optimal send time (6am) → replicated → **+25% signups**

**System paid for itself in 1 month**

---

## The Big Picture

### What This Solves
- **Weeks of manual detective work** → Automated
- **Reactive firefighting** → Proactive monitoring
- **Missed opportunities** → Discovered early
- **Compliance risks** → Caught before audits
- **Bad decisions from bad data** → Prevented

### What You Get
- **Peace of mind**: Data is being watched
- **Time savings**: 40+ hours/quarter
- **Risk reduction**: Catch compliance issues early
- **Revenue opportunities**: Find what's working
- **Team confidence**: Trust your analytics

---

## One-Liner Summary

**"Build a $10/month robot that tells you what's breaking AND what's working in your analytics before you discover it the hard way."**

---

## Resources

### Workshop Materials
- GitHub: [URL]
- Colab Notebooks: [URLs]
- Documentation: In repo `docs/` folder

### External References
- BigQuery SQL reference: cloud.google.com/bigquery/docs/reference/standard-sql
- OpenAI function calling: platform.openai.com/docs/guides/function-calling
- Slack webhooks: api.slack.com/messaging/webhooks
- GitHub Actions: docs.github.com/actions

### Inspiration
- Sample checks for news orgs: In `config/checks.yaml`
- Deployment templates: In `docs/playbook.md`
- Cost calculator: In `docs/cost-analysis.xlsx`

---

## Thank You!

**Questions?**
- Workshop Slack: #analytics-intelligence
- Email: bryan.davis@ap.org
- LinkedIn: /in/bryandavis-data

**Let's find what's broken AND what's working!** 🚀

---

*This handout is also available in the GitHub repo as `ATTENDEE-HANDOUT.md`*
