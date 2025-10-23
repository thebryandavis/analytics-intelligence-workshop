"""
Load sample news analytics data into BigQuery.

Usage:
    python load_to_bigquery.py --project YOUR_PROJECT_ID --dataset npa_workshop

This script:
1. Creates a BigQuery dataset (if it doesn't exist)
2. Creates a table with proper schema
3. Loads the CSV data
4. Runs validation queries
"""

import argparse
from google.cloud import bigquery
import sys

def create_dataset(client, dataset_id, location='US'):
    """Create BigQuery dataset if it doesn't exist."""
    dataset_ref = f"{client.project}.{dataset_id}"

    try:
        client.get_dataset(dataset_ref)
        print(f"✓ Dataset {dataset_id} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        dataset = client.create_dataset(dataset)
        print(f"✓ Created dataset {dataset_id}")

def create_table(client, dataset_id, table_id, schema_file):
    """Create BigQuery table with schema."""
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    # Load schema from JSON file
    import json
    with open(schema_file, 'r') as f:
        schema_json = json.load(f)

    schema = []
    for field in schema_json:
        schema.append(bigquery.SchemaField(
            field['name'],
            field['type'],
            mode=field.get('mode', 'NULLABLE'),
            description=field.get('description', '')
        ))

    # Delete table if exists (for fresh reload)
    try:
        client.delete_table(table_ref)
        print(f"✓ Deleted existing table {table_id}")
    except Exception:
        pass

    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f"✓ Created table {table_id}")
    return table

def load_data(client, dataset_id, table_id, csv_file):
    """Load CSV data into BigQuery table."""
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header
        autodetect=False,  # Use explicit schema
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        # Parse timestamp column
        schema=[
            bigquery.SchemaField("event_timestamp", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("event_datetime", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("event_date", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("event_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("user_pseudo_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("session_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("platform", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("device_category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("geo_country", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("referrer", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("page_location", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("article_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("section", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("consent_state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("engagement_time_msec", "INTEGER", mode="NULLABLE"),
        ]
    )

    print(f"Loading data from {csv_file}...")
    with open(csv_file, 'rb') as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    # Wait for job to complete
    job.result()

    # Get table stats
    table = client.get_table(table_ref)
    print(f"✓ Loaded {table.num_rows:,} rows into {table_id}")
    print(f"  Table size: {table.num_bytes / 1024 / 1024:.1f} MB")

def validate_data(client, dataset_id, table_id):
    """Run validation queries to confirm planted problems and opportunities."""
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    print("\n" + "="*60)
    print("VALIDATION CHECKS")
    print("="*60)

    # Check 1: Total row count
    query = f"SELECT COUNT(*) as total FROM `{table_ref}`"
    result = client.query(query).result()
    total_rows = list(result)[0]['total']
    print(f"\n✓ Total events: {total_rows:,}")

    # Check 2: Date range
    query = f"""
    SELECT
        MIN(event_date) as min_date,
        MAX(event_date) as max_date,
        COUNT(DISTINCT event_date) as num_days
    FROM `{table_ref}`
    """
    result = list(client.query(query).result())[0]
    print(f"✓ Date range: {result['min_date']} to {result['max_date']} ({result['num_days']} days)")

    # Check 3: Event distribution
    query = f"""
    SELECT event_name, COUNT(*) as count
    FROM `{table_ref}`
    GROUP BY event_name
    ORDER BY count DESC
    """
    print(f"\n✓ Event distribution:")
    for row in client.query(query).result():
        print(f"  {row['event_name']:25} {row['count']:>10,}")

    # Check 4: PROBLEM 1 - iOS scroll_depth drops
    query = f"""
    WITH hourly_counts AS (
      SELECT
        event_date,
        EXTRACT(HOUR FROM event_datetime) as hour,
        COUNT(*) as scroll_events
      FROM `{table_ref}`
      WHERE platform = 'ios' AND event_name = 'scroll_depth'
      GROUP BY event_date, hour
    )
    SELECT event_date, hour, scroll_events
    FROM hourly_counts
    WHERE event_date >= '20251006'  -- Day 3+
    AND hour >= 14
    ORDER BY event_date, hour
    LIMIT 5
    """
    result = list(client.query(query).result())
    print(f"\n✓ PROBLEM 1 - iOS scroll_depth after 2pm Day 3+ (should be 0 or very low):")
    if len(result) == 0:
        print(f"  No events found - TRACKING BROKEN! ✓")
    else:
        for row in result:
            print(f"  {row['event_date']} {row['hour']:02d}:00 - {row['scroll_events']} events")

    # Check 5: PROBLEM 2 - Missing consent
    query = f"""
    SELECT
        COUNT(*) as total,
        COUNTIF(consent_state IS NULL) as missing_consent,
        ROUND(COUNTIF(consent_state IS NULL) / COUNT(*) * 100, 1) as pct_missing
    FROM `{table_ref}`
    """
    result = list(client.query(query).result())[0]
    print(f"\n✓ PROBLEM 2 - Missing consent_state:")
    print(f"  {result['missing_consent']:,} / {result['total']:,} events ({result['pct_missing']}%) - Target: ~15%")

    # Check 6: PROBLEM 3 - PII in URLs
    query = f"""
    SELECT
        COUNT(*) as total,
        COUNTIF(REGEXP_CONTAINS(page_location, r'email=')) as with_pii,
        ROUND(COUNTIF(REGEXP_CONTAINS(page_location, r'email=')) / COUNT(*) * 100, 1) as pct_pii
    FROM `{table_ref}`
    """
    result = list(client.query(query).result())[0]
    print(f"\n✓ PROBLEM 3 - PII (email) in page_location:")
    print(f"  {result['with_pii']:,} / {result['total']:,} events ({result['pct_pii']}%) - Target: ~5%")

    # Check 7: PROBLEM 4 - Duplicates
    query = f"""
    WITH duplicates AS (
      SELECT user_pseudo_id, event_timestamp, COUNT(*) as dup_count
      FROM `{table_ref}`
      GROUP BY user_pseudo_id, event_timestamp
      HAVING COUNT(*) > 1
    )
    SELECT
        COUNT(*) as duplicate_pairs,
        SUM(dup_count - 1) as extra_events
    FROM duplicates
    """
    result = list(client.query(query).result())[0]
    print(f"\n✓ PROBLEM 4 - Duplicate events (same user + timestamp):")
    print(f"  {result['duplicate_pairs']:,} duplicate pairs, {result['extra_events']:,} extra events (~1% target)")

    # Check 8: OPPORTUNITY 1 - Newsletter spike on Day 4
    query = f"""
    SELECT
        event_date,
        COUNT(*) as signups
    FROM `{table_ref}`
    WHERE event_name = 'newsletter_signup'
    GROUP BY event_date
    ORDER BY event_date
    """
    print(f"\n✓ OPPORTUNITY 1 - Newsletter signups by day (Day 4 should spike 45%):")
    baseline = None
    for row in client.query(query).result():
        if baseline is None and row['event_date'] < '20251007':
            baseline = row['signups']
        change = ""
        if baseline and row['event_date'] == '20251007':
            pct_change = (row['signups'] - baseline) / baseline * 100
            change = f" (+{pct_change:.0f}% 🎉)"
        print(f"  {row['event_date']}: {row['signups']:,} signups{change}")

    # Check 9: OPPORTUNITY 2 - Weekend mobile engagement
    query = f"""
    WITH engagement_stats AS (
      SELECT
        CASE
          WHEN EXTRACT(DAYOFWEEK FROM event_datetime) IN (1, 7) THEN 'Weekend'
          ELSE 'Weekday'
        END as day_type,
        device_category,
        AVG(engagement_time_msec / 1000) as avg_engagement_sec
      FROM `{table_ref}`
      GROUP BY day_type, device_category
    )
    SELECT * FROM engagement_stats
    WHERE device_category = 'mobile'
    ORDER BY day_type
    """
    print(f"\n✓ OPPORTUNITY 2 - Mobile engagement time (Weekend should be 2x):")
    for row in client.query(query).result():
        print(f"  {row['day_type']:8} mobile: {row['avg_engagement_sec']:.1f} seconds")

    # Check 10: OPPORTUNITY 3 - Reddit referrer appears Day 5+
    query = f"""
    SELECT
        event_date,
        COUNTIF(referrer = 'reddit.com') as reddit_events,
        COUNT(*) as total_events,
        ROUND(COUNTIF(referrer = 'reddit.com') / COUNT(*) * 100, 2) as reddit_pct
    FROM `{table_ref}`
    GROUP BY event_date
    ORDER BY event_date
    """
    print(f"\n✓ OPPORTUNITY 3 - Reddit referrer (should appear Day 5: 20251008):")
    for row in client.query(query).result():
        reddit_marker = " 🎉 NEW REFERRER!" if row['reddit_events'] > 0 and row['event_date'] == '20251008' else ""
        if row['reddit_events'] > 0:
            print(f"  {row['event_date']}: {row['reddit_events']:,} events ({row['reddit_pct']}%){reddit_marker}")

    print("\n" + "="*60)
    print("✅ Validation complete! Data loaded successfully.")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(description='Load sample data into BigQuery')
    parser.add_argument('--project', required=True, help='GCP project ID')
    parser.add_argument('--dataset', default='npa_workshop', help='BigQuery dataset name')
    parser.add_argument('--table', default='news_events', help='BigQuery table name')
    parser.add_argument('--csv', default='news_analytics_sample_data.csv', help='CSV file path')
    parser.add_argument('--schema', default='bigquery_schema.json', help='Schema JSON file path')

    args = parser.parse_args()

    print(f"Loading data to BigQuery...")
    print(f"  Project: {args.project}")
    print(f"  Dataset: {args.dataset}")
    print(f"  Table: {args.table}")
    print(f"  CSV: {args.csv}")
    print()

    # Initialize client
    client = bigquery.Client(project=args.project)

    # Create dataset
    create_dataset(client, args.dataset)

    # Create table
    create_table(client, args.dataset, args.table, args.schema)

    # Load data
    load_data(client, args.dataset, args.table, args.csv)

    # Validate
    validate_data(client, args.dataset, args.table)

    print(f"\n✅ All done! Access your data at:")
    print(f"   {args.project}.{args.dataset}.{args.table}")

if __name__ == '__main__':
    main()
