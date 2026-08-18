# Analytics Intelligence Workshop

A reference implementation for turning event data into evidence-backed product investigations.

Built for product, analytics, and growth teams. My role covered the product concept, data model, checks, workflow, and workshop.

## Product question

Can an analytics system do more than report numbers? This project tests whether it can identify a problem or opportunity, explain why it matters, and suggest a reasonable next check.

## What I built

The workflow combines BigQuery, Python, notebooks, configurable checks, and an optional language-model step. Sample data includes planted tracking breaks and growth changes so the workflow can run end to end.

The system looks for failures in instrumentation, consent, and data quality, as well as unusual changes worth investigating. Findings include context and a suggested next check instead of asking a team to trust an unexplained alert.

## What this shows

- Product judgment about which findings deserve attention
- Data-quality checks tied to a real investigation workflow
- A bounded AI step that supports analysis without replacing it
- Evaluation questions for false positives, privacy, and missing consent

## What remains unproven

The sample data is intentionally small and contains planted changes. This repository does not claim production impact. A production team would need to tune thresholds against its own traffic, test false positives, and establish privacy and consent controls.

## Quick start

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

The three workshop notebooks can be run with sample data:

- [Setup and first query](notebooks/COLAB_01_setup_and_first_query.ipynb)
- [AI-generated SQL checks](notebooks/COLAB_02_ai_generated_sql_checks.ipynb)
- [Anomaly detection and alerts](notebooks/COLAB_03_anomaly_detection_and_alerts.ipynb)

For deployment context, see the [attendee handout](ATTENDEE-HANDOUT.md) and [playbook](docs/playbook.md).

## Repository structure

```text
notebooks/       Interactive workshop notebooks
src/             BigQuery, SQL generation, classification, and alerting code
config/          Check definitions
data/            Sample-data generation, loading, and schema files
docs/            Deployment and operating notes
```

## Next test

Add evaluation cases for false positives, PII checks, and missing-consent data before asking a team to run the workflow continuously.

## Background

I presented the workshop at the News Product Alliance Summit in 2025. The repository is a reference implementation, not a claim that a team should deploy it unchanged.
