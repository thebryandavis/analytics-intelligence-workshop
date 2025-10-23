# GitHub Setup Instructions

Your clean public repo is ready! Here's how to push it to GitHub.

## Current Status ✅

- ✅ Clean repo created in: `/Users/brdavis/Documents/npa-workshop-public/`
- ✅ Git initialized
- ✅ Initial commit created
- ✅ Only public materials included (no presenter notes!)

## What's Included

**Documentation (6 files):**
- README.md - Main overview
- ATTENDEE-HANDOUT.md - Take-home guide
- WORKSHOP-LINKS.md - Quick notebook access
- QUICKSTART.md - 5-minute setup guide
- CONTRIBUTING.md - How to contribute
- LICENSE - MIT License

**Code & Config (5 files):**
- src/analytics_intelligence.py - Core Python module
- config/checks.yaml - 20+ check templates
- data/generate_sample_data.py - Sample data generator
- data/load_to_bigquery.py - BigQuery loader
- data/bigquery_schema.json - Table schema

**Notebooks (3 Colab notebooks):**
- COLAB_01_setup_and_first_query.ipynb
- COLAB_02_ai_generated_sql_checks.ipynb
- COLAB_03_anomaly_detection_and_alerts.ipynb

**Other (3 files):**
- requirements.txt - Python dependencies
- docs/playbook.md - Deployment guide
- .gitignore - Excludes presenter materials

**Total: 18 files, ~5,000 lines of code/docs**

---

## Next Steps: Push to GitHub

### 1. Create GitHub Repository

Go to https://github.com/new and create a new repo:

**Repository name:** `analytics-intelligence-workshop` (or your choice)

**Description:**
```
Build an automated analytics intelligence system that monitors event data 24/7 and alerts you to problems and opportunities using BigQuery + AI. Workshop materials from NPA Summit 2025.
```

**Settings:**
- ✅ Public
- ❌ Don't initialize with README (you already have one)
- ❌ Don't add .gitignore (you already have one)
- ❌ Don't add license (you already have one)

Click **Create repository**

### 2. Push Your Code

GitHub will show you commands. Use these:

```bash
cd /Users/brdavis/Documents/npa-workshop-public

# Add remote
git remote add origin https://github.com/thebryandavis/analytics-intelligence-workshop.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR-USERNAME` with your GitHub username!**

### 3. Verify Upload

Go to: `https://github.com/YOUR-USERNAME/analytics-intelligence-workshop`

You should see:
- ✅ README.md displays on homepage
- ✅ All 18 files present
- ✅ Folders: notebooks/, src/, config/, data/, docs/

### 4. Update README Links

Once uploaded, update these placeholders in README.md:

**Find and replace:**
- `[your-username]` → Your actual GitHub username
- `[repo link - will share]` → Your actual repo URL
- `[bit.ly/npa-workshop-feedback]` → Your actual survey URL

**Commit changes:**
```bash
git add README.md
git commit -m "Update GitHub username and links"
git push
```

---

## Create Short Links (Recommended)

Use https://bitly.com to create memorable links:

### For Notebooks (share these at workshop):
1. Open: `https://github.com/YOUR-USERNAME/analytics-intelligence-workshop/blob/main/notebooks/COLAB_01_setup_and_first_query.ipynb`
2. Add to Colab: Replace `github.com` with `colab.research.google.com/github`
3. Create bit.ly: `bit.ly/npa-setup`

**Repeat for all 3 notebooks:**
- Notebook 1: `bit.ly/npa-setup`
- Notebook 2: `bit.ly/npa-ai-sql`
- Notebook 3: `bit.ly/npa-alerts`

### For Main Repo:
Create: `bit.ly/npa-workshop` → Links to your repo

### Update WORKSHOP-LINKS.md
Replace placeholder links with your bit.ly links.

---

## Enable GitHub Pages (Optional)

Host your documentation as a website:

1. Go to repo **Settings → Pages**
2. Source: **Deploy from branch**
3. Branch: **main**, folder: **/ (root)**
4. Click **Save**

Your site will be at: `https://YOUR-USERNAME.github.io/analytics-intelligence-workshop/`

---

## Test Colab Links

**Important:** Test that your Colab links work!

1. Open in incognito window (to see what attendees see)
2. Click your bit.ly/npa-setup link
3. Should open in Colab with "Copy to Drive" button
4. Verify all 3 notebooks work

**Colab URL format:**
```
https://colab.research.google.com/github/YOUR-USERNAME/analytics-intelligence-workshop/blob/main/notebooks/COLAB_01_setup_and_first_query.ipynb
```

---

## Share at Workshop

### Write on Whiteboard:
```
NPA ANALYTICS INTELLIGENCE

📓 Notebooks:
   bit.ly/npa-setup
   bit.ly/npa-ai-sql
   bit.ly/npa-alerts

📚 All Materials:
   bit.ly/npa-workshop

PROJECT: npa-workshop-2025
```

### Post in Slack/Chat:
```
🎓 NPA Analytics Intelligence Workshop - Links

📓 Notebooks (click to open in Colab):
• Setup: bit.ly/npa-setup
• AI SQL: bit.ly/npa-ai-sql
• Alerts: bit.ly/npa-alerts

📚 All materials: bit.ly/npa-workshop

No setup required! Just click "Copy to Drive" and run cells with ▶️
```

---

## After Workshop

### 1. Update README with Stats
Add workshop attendance, feedback highlights, etc.

### 2. Monitor Issues
Attendees may open issues with questions - respond helpfully!

### 3. Accept PRs
Community members may contribute check templates - review and merge!

### 4. Star Repo
⭐ Star your own repo so it shows in your profile!

---

## Troubleshooting

**"Permission denied" when pushing:**
- Set up SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Or use GitHub CLI: `gh auth login`

**"Repository not found":**
- Check remote URL: `git remote -v`
- Update if needed: `git remote set-url origin https://github.com/YOUR-USERNAME/REPO-NAME.git`

**Notebooks not opening in Colab:**
- Verify URL format
- Make sure repo is public
- Try opening directly first (not via bit.ly)

---

## Summary Checklist

Before workshop:
- [ ] Create GitHub repo (public)
- [ ] Push code to GitHub
- [ ] Update README with your username
- [ ] Create bit.ly short links for notebooks
- [ ] Test Colab links in incognito
- [ ] Update WORKSHOP-LINKS.md with bit.ly URLs
- [ ] Write links on whiteboard
- [ ] Post links in Slack/chat

During workshop:
- [ ] Share bit.ly links verbally
- [ ] Show how to "Copy to Drive" in Colab

After workshop:
- [ ] Share repo link via email
- [ ] Monitor for issues/questions
- [ ] Update README with workshop results

---

**Your repo is ready to go!** 🚀

Just push to GitHub and create those bit.ly links.

Questions? You've got this!
