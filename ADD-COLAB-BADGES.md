# How to Add "Open in Colab" Badges to Notebooks

## The Problem
When users click GitHub links to notebooks, they see raw JSON. When you share from Google Drive, there's no easy "copy" option.

## The Solution
Add a badge/button at the top of each notebook that opens it in Colab with one click.

---

## Method 1: Add Badge to Each Notebook (Recommended)

### Step 1: Open Each Notebook Locally

Open in Jupyter or VS Code:
```bash
cd /Users/brdavis/Documents/npa-workshop-public/notebooks
jupyter notebook
```

### Step 2: Add This Cell at the Very Top

Add a new **Markdown cell** as the FIRST cell in each notebook:

**For Notebook 1:**
```markdown
<a href="https://colab.research.google.com/github/thebryandavis/analytics-intelligence-workshop/blob/main/notebooks/COLAB_01_setup_and_first_query.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Notebook 1: Setup & First Query
```

**For Notebook 2:**
```markdown
<a href="https://colab.research.google.com/github/thebryandavis/analytics-intelligence-workshop/blob/main/notebooks/COLAB_02_ai_generated_sql_checks.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Notebook 2: AI-Generated SQL Checks
```

**For Notebook 3:**
```markdown
<a href="https://colab.research.google.com/github/thebryandavis/analytics-intelligence-workshop/blob/main/notebooks/COLAB_03_anomaly_detection_and_alerts.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Notebook 3: Anomaly Detection & Alerts
```

### Step 3: Save Notebooks

Save each notebook after adding the badge.

### Step 4: Commit & Push

```bash
cd /Users/brdavis/Documents/npa-workshop-public
git add notebooks/
git commit -m "Add Open in Colab badges to all notebooks"
git push
```

---

## Method 2: Share Direct Colab Links (Easier, What We Already Did!)

Just share these URLs - they open directly in Colab:

### Notebook 1:
```
https://colab.research.google.com/github/thebryandavis/analytics-intelligence-workshop/blob/main/notebooks/COLAB_01_setup_and_first_query.ipynb
```

### Notebook 2:
```
https://colab.research.google.com/github/thebryandavis/analytics-intelligence-workshop/blob/main/notebooks/COLAB_02_ai_generated_sql_checks.ipynb
```

### Notebook 3:
```
https://colab.research.google.com/github/thebryandavis/analytics-intelligence-workshop/blob/main/notebooks/COLAB_03_anomaly_detection_and_alerts.ipynb
```

**These already work!** Just create bit.ly short links for them.

---

## Method 3: Create a Simple Landing Page (Alternative)

Create a simple HTML page or Google Doc with big buttons that link to the Colab URLs.

---

## What Happens When Users Click?

### When they click a Colab URL:
1. **Opens in Colab** (not raw JSON)
2. **See a "Copy to Drive" button** at the top
3. **Click "Copy to Drive"**
4. **Notebook copies to their Google Drive**
5. **They can run cells with ▶️**

---

## For the Workshop: Simplest Approach

### Just share the Colab URLs directly:

**Create these bit.ly links:**

1. Go to https://bitly.com
2. Create short links:
   - `bit.ly/npa-setup` → Long Colab URL for Notebook 1
   - `bit.ly/npa-ai-sql` → Long Colab URL for Notebook 2
   - `bit.ly/npa-alerts` → Long Colab URL for Notebook 3

**Write on whiteboard:**
```
NOTEBOOKS:
  bit.ly/npa-setup
  bit.ly/npa-ai-sql
  bit.ly/npa-alerts

(Click → "Copy to Drive" → Run with ▶️)
```

**Say during workshop:**
> "Click the link, you'll see a yellow banner at the top with 'Copy to Drive' - click that. Then you can run the cells. That's it!"

---

## Test Your Links

Before workshop, open each Colab URL in an incognito window:

1. Should open in Colab (not show raw JSON)
2. Should show "Copy to Drive" button
3. Should be able to click it and make a copy
4. Should be able to run cells

---

## Don't Overthink It!

**The Colab URLs we created already work perfectly.** You don't need to mess with Google Drive sharing.

**Just:**
1. Create bit.ly short links
2. Share those
3. Tell people to click "Copy to Drive"

**That's it!** ✅

---

## Summary

### ❌ Don't:
- Share from Google Drive (complicated sharing permissions)
- Share raw GitHub blob URLs (shows JSON)

### ✅ Do:
- Share Colab integration URLs (already in your README/WORKSHOP-LINKS)
- Create bit.ly short links for easy typing
- Test in incognito before workshop

### The Full Colab URLs (use these for bit.ly):

See `BITLY-LINKS.md` for the exact URLs to use.

---

**You're ready!** The links work. Just create the bit.ly shortcuts and test them.
