# Quick Start Guide

Get up and running in 5 minutes!

## 🎯 Option 1: Workshop Attendees (No Setup)

**Just want to follow along?**

1. Open [WORKSHOP-LINKS.md](WORKSHOP-LINKS.md)
2. Click Notebook 1
3. Click "Copy to Drive"
4. Run cells with ▶️ button

Done! The notebooks use shared sample data.

## 🚀 Option 2: Deploy to Production (1-2 hours)

**Ready to deploy at your org?**

1. Read [ATTENDEE-HANDOUT.md](ATTENDEE-HANDOUT.md) - Complete setup guide
2. Get your prerequisites:
   - OpenAI API key: https://platform.openai.com/api-keys
   - BigQuery access at your org
   - Slack webhook (optional): https://api.slack.com/messaging/webhooks

3. Load your data to BigQuery
4. Customize `config/checks.yaml`
5. Deploy using [docs/playbook.md](docs/playbook.md)

## 🧪 Option 3: Try Locally (30 minutes)

**Want to test on your machine?**

```bash
# Clone repo
git clone https://github.com/[your-username]/analytics-intelligence-workshop
cd analytics-intelligence-workshop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="sk-..."
export GCP_PROJECT="your-project-id"

# Launch Jupyter
jupyter notebook notebooks/
```

## 📚 What to Read First

1. **[README.md](README.md)** - Overview and what this does
2. **[WORKSHOP-LINKS.md](WORKSHOP-LINKS.md)** - Quick access to notebooks
3. **[ATTENDEE-HANDOUT.md](ATTENDEE-HANDOUT.md)** - Complete take-home guide
4. **[docs/playbook.md](docs/playbook.md)** - Deployment options

## ❓ Need Help?

- **Email:** brdavis@ap.org
- **Issues:** Open a GitHub issue
- **NPA Slack:** #analytics-intelligence

---

**Ready?** Start with [WORKSHOP-LINKS.md](WORKSHOP-LINKS.md) 🚀
