# Analytics Intelligence Workshop
### News Product Alliance Summit 2025

Build an automated analytics intelligence system that monitors your event data 24/7 and alerts you to both problems and opportunities using BigQuery + AI.

**Presented by:** Bryan Davis, Director of Product (Data & Analytics), The Associated Press
**Cost to run:** < $15/month | **Setup time:** 1-2 hours | **Skills needed:** Copy/paste

---

## 🚀 Quick Start

### For Workshop Attendees

**3 Google Colab Notebooks** (no setup required, runs in browser):

1. **[Setup & First Query](https://tinyurl.com/nycpizza1)** - Connect to BigQuery, explore data
2. **[AI-Generated SQL Checks](https://tinyurl.com/nycpizza2)** - Generate SQL with GPT, find issues
3. **[Anomaly Detection & Alerts](https://tinyurl.com/nycpizza3)** - Classify findings, send Slack alerts

**📖 Take-Home Guide:** [ATTENDEE-HANDOUT.md](ATTENDEE-HANDOUT.md) - Everything you need to deploy this at your org

---

## 📂 Repository Structure

```
├── README.md                          # You are here
├── ATTENDEE-HANDOUT.md                # 10-page take-home guide
│
├── notebooks/                         # Interactive workshop notebooks
│   ├── COLAB_01_setup_and_first_query.ipynb
│   ├── COLAB_02_ai_generated_sql_checks.ipynb
│   └── COLAB_03_anomaly_detection_and_alerts.ipynb
│
├── src/                               # Core Python module
│   └── analytics_intelligence.py      # BigQuery, SQL gen, classification, alerts
│
├── config/                            # Configuration
│   └── checks.yaml                    # Check definitions (20+ templates)
│
├── data/                              # Data generation & loading
│   ├── generate_sample_data.py        # Creates sample events with planted issues
│   ├── load_to_bigquery.py            # Loads CSV to BigQuery
│   └── bigquery_schema.json           # Table schema
│
├── docs/                              # Additional documentation
│   └── playbook.md                    # Deployment guide & best practices
│
└── requirements.txt                   # Python dependencies
```

---

## 💡 What This Does

**Finds Problems:**
- 🚨 Tracking breaks (iOS/Android/web)
- 🔒 PII leaks in your data
- ⚠️ Missing consent flags (GDPR compliance)
- 🐛 Data quality issues
- 📉 Event volume drops

**Discovers Opportunities:**
- 🎉 Traffic spikes worth investigating
- 🔗 New high-value referral sources
- 📈 Engagement pattern changes
- ⭐ Content performing exceptionally well

**Sends Smart Alerts:**
- Slack messages with context and recommendations
- Classified by severity (critical, high, medium, low)
- Categorized (problem vs opportunity)

---

## 🎯 What You'll Build

A system that sends you Slack messages like:

> 🚨 **Critical: iOS Scroll Tracking Stopped**
>
> scroll_depth events dropped to zero after 2pm on Day 3. This indicates a tracking implementation failure on iOS.
>
> **Recommendation:** Check iOS tracking code immediately. Review recent app deployments.

> 🎉 **Opportunity: Newsletter Signup Spike**
>
> Newsletter signups increased 45% on Day 4 compared to baseline. Worth investigating the cause.
>
> **Recommendation:** Review content, email campaigns, or referral sources from that day. Consider replicating success factors.

---

## 📚 How to Use This Repository

### Option 1: Workshop Follow-Along (No Setup)
1. Click a Colab notebook link above
2. Click "Copy to Drive" at the top
3. Follow along or just watch
4. All notebooks use shared sample data

### Option 2: Deploy to Production (1-2 hours)
1. Read [ATTENDEE-HANDOUT.md](ATTENDEE-HANDOUT.md) for full setup guide
2. Load your data to BigQuery
3. Customize `config/checks.yaml` for your tracking plan
4. Deploy (GitHub Actions, Cloud Functions, or cron job)
5. Start receiving alerts!

### Option 3: Try Locally First (30 min)
```bash
# Clone repo
git clone https://github.com/[your-username]/npa-analytics-intelligence
cd npa-analytics-intelligence

# Install dependencies
pip install -r requirements.txt

# Set up environment
export OPENAI_API_KEY="sk-..."
export GCP_PROJECT="your-project-id"

# Run notebooks locally
jupyter notebook notebooks/
```

---

## 🛠️ Prerequisites

### Required
- **Google Cloud account** (free tier works)
- **OpenAI API key** ([get one here](https://platform.openai.com/api-keys))
- **Python 3.8+** (for running locally)

### Optional
- **Slack workspace** (for alerts - can also use email/PagerDuty/etc.)
- **GitHub account** (for GitHub Actions deployment)

---

## 💰 Cost Breakdown

### Workshop (today)
- BigQuery: **$0** (free tier)
- OpenAI: **~$0.50** (GPT-4, ~15 queries)
- **Total: < $1**

### Production (monthly, running every 6 hours)
- BigQuery: **~$5** (depends on data volume)
- OpenAI: **~$3-10** (GPT-3.5-turbo recommended)
- Compute: **$0** (GitHub Actions free tier)
- **Total: < $15/month**

**ROI:** Catch one tracking break early → saves weeks of lost data

---

## 🚦 Getting Started After the Workshop

### This Week
- [ ] Re-run the Colab notebooks (they use sample data, no setup needed)
- [ ] Review the [ATTENDEE-HANDOUT.md](ATTENDEE-HANDOUT.md)
- [ ] Draft 5-10 custom checks specific to your tracking plan
- [ ] Get OpenAI API key
- [ ] Get BigQuery access at your org

### Next Week
- [ ] Load your analytics data to BigQuery
- [ ] Customize `config/checks.yaml`
- [ ] Test locally with your data

### Week 3-4
- [ ] Deploy to GitHub Actions (recommended) or Cloud Functions
- [ ] Configure Slack webhook
- [ ] Receive your first alert!
- [ ] Share results with team

---

## 📖 Key Resources

### In This Repo
- **[ATTENDEE-HANDOUT.md](ATTENDEE-HANDOUT.md)** - Complete take-home guide (10 pages)
- **[docs/playbook.md](docs/playbook.md)** - Deployment guide with 5 deployment options
- **[config/checks.yaml](config/checks.yaml)** - 20+ check templates you can customize

### External Resources
- [BigQuery SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Slack Webhooks Setup](https://api.slack.com/messaging/webhooks)
- [GitHub Actions Documentation](https://docs.github.com/actions)

---

## 🤝 Support & Community

### Get Help
- **Email:** brdavis@ap.org
- **GitHub Issues:** [Report bugs or request features](https://github.com/[your-username]/npa-analytics-intelligence/issues)
- **NPA Slack:** #analytics-intelligence

### Share Your Success
When you deploy this and catch your first tracking break or discover your first opportunity, let me know! Those are my favorite emails. 📧

### Contribute
Found a great check template? Improved the deployment process? PRs welcome!

---

## 📊 Real-World Results (The Associated Press)

**Before this system:**
- Tracking breaks discovered 2-3 weeks late
- 4 hours/week on manual data quality checks
- Opportunities only found in retrospect

**After this system:**
- Alerts within 6 hours of issue
- 0 hours/week on manual checking
- 5+ opportunities discovered per quarter

**Example win:** Newsletter signup spike detected same day → investigated → found optimal send time (6am) → replicated → **+25% sustained lift**

**ROI:** System paid for itself in first month

---

## 📋 What's Included

### Notebooks (3)
- Interactive Google Colab notebooks
- Work with sample data (no setup required)
- Can run locally with Jupyter

### Core Module (1 file)
- `src/analytics_intelligence.py` - Production-ready Python module
- Includes: BigQueryConnector, SQLGenerator, AnomalyClassifier, SlackAlerter, CheckRunner

### Configuration (1 file)
- `config/checks.yaml` - 20+ check templates
- Easy to customize with plain English descriptions

### Data Tools (3 files)
- Sample data generator (creates 3.5M events with planted issues)
- BigQuery loader script
- Schema definition

### Documentation (3 files)
- This README
- Attendee handout (10-page guide)
- Deployment playbook

---

## 🎓 Workshop Topics Covered

1. **Setup & Exploration** - Connect to BigQuery, understand baselines
2. **SQL Generation** - Use GPT to generate SQL from natural language
3. **Problem Detection** - Find tracking breaks, PII leaks, data quality issues
4. **Opportunity Discovery** - Detect traffic spikes, new referrers, behavior changes
5. **Classification** - Use OpenAI function calling to categorize findings
6. **Alerting** - Send smart Slack messages with recommendations
7. **Deployment** - Choose from 5 deployment options
8. **Customization** - Write checks in plain English via YAML config

---

## ⚡ Quick Deploy Example (GitHub Actions)

Once you have your data in BigQuery:

1. **Fork this repo**
2. **Add secrets** (Settings → Secrets):
   - `OPENAI_API_KEY`
   - `SLACK_WEBHOOK`
   - `GCP_SA_KEY`
3. **Enable GitHub Actions**
4. **That's it!** Checks run every 6 hours automatically

See [docs/playbook.md](docs/playbook.md) for complete deployment guide.

---

## 🙋 FAQ

**Q: What if I don't have BigQuery?**
A: Works with any SQL database (Snowflake, Redshift, PostgreSQL). Just swap the connector.

**Q: Can I use Claude or Gemini instead of OpenAI?**
A: Yes! Any LLM with function calling support. Easy to adapt.

**Q: What about false positives?**
A: You'll tune thresholds over the first 2 weeks. Start conservative (50% drops), then tighten. Tuning guide in playbook.

**Q: How do I convince my boss?**
A: Run it quietly for 2 weeks. When you catch your first tracking break early, forward the Slack alert up. System sells itself.

**Q: Can I test without a production database?**
A: Yes! Use the sample data generator in `data/generate_sample_data.py`. Creates realistic data with planted issues.

---

## 📄 License

This workshop material is provided for educational purposes. Feel free to adapt for your organization.

---

## 🙏 Acknowledgments

Created for the News Product Alliance Summit 2025.

Special thanks to the NPA community for inspiring this work.

---

**Ready to catch your first tracking break before anyone notices?** 🚀

**Let's build it:** Start with [Notebook 1](notebooks/COLAB_01_setup_and_first_query.ipynb)

---

**Questions?** Email brdavis@ap.org or open an issue.

**Found this useful?** Star ⭐ the repo and share with your team!
