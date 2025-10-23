"""
Generate sample news analytics data for NPA workshop.

Creates realistic GA4-style event data with planted problems and opportunities:

PROBLEMS:
1. iOS scroll_depth events stop after 2pm on Day 3
2. 15% of events missing consent_state (GDPR issue)
3. PII (email addresses) in page_location URLs
4. Duplicate events (same user + timestamp)

OPPORTUNITIES:
1. Newsletter signups jump 45% on Day 4
2. Weekend mobile readers stay 2x longer
3. New referral source (reddit.com) with high engagement
4. Push notification clicks spike Tuesday mornings
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import json

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
START_DATE = datetime(2025, 10, 4)  # Start 7 days before workshop
DAYS = 7
EVENTS_PER_DAY = 500_000
TOTAL_EVENTS = DAYS * EVENTS_PER_DAY

print(f"Generating {TOTAL_EVENTS:,} events over {DAYS} days...")

# Helper functions
def generate_user_id():
    """Generate GA4-style user pseudo ID."""
    return ''.join(random.choices(string.digits, k=10)) + '.' + ''.join(random.choices(string.digits, k=10))

def generate_session_id():
    """Generate session ID."""
    return ''.join(random.choices(string.digits, k=10))

def random_timestamp(date, hour_weights=None):
    """Generate random timestamp within a day, optionally weighted by hour."""
    if hour_weights is not None:
        hour = np.random.choice(24, p=hour_weights)
    else:
        hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    microsecond = random.randint(0, 999999)
    return datetime.combine(date, datetime.min.time()) + timedelta(hours=hour, minutes=minute, seconds=second, microseconds=microsecond)

# Base data distributions
EVENT_TYPES = {
    'page_view': 0.50,
    'scroll_depth': 0.20,
    'click': 0.15,
    'newsletter_signup': 0.02,
    'push_notification_click': 0.03,
    'video_play': 0.05,
    'search': 0.05
}

PLATFORMS = {
    'web': 0.50,
    'ios': 0.25,
    'android': 0.25
}

COUNTRIES = {
    'US': 0.60,
    'GB': 0.15,
    'CA': 0.10,
    'AU': 0.08,
    'Other': 0.07
}

DEVICE_CATEGORIES = {
    'mobile': 0.55,
    'desktop': 0.35,
    'tablet': 0.10
}

SECTIONS = [
    'politics', 'sports', 'business', 'technology',
    'entertainment', 'health', 'world', 'local'
]

REFERRERS = {
    'google.com': 0.40,
    'facebook.com': 0.20,
    'twitter.com': 0.15,
    'direct': 0.20,
    'other': 0.05
}

# Generate base user pool (simulating returning users)
NUM_USERS = 150_000
USER_POOL = [generate_user_id() for _ in range(NUM_USERS)]

# Hour weights (news consumption patterns - peaks morning/lunch/evening)
HOUR_WEIGHTS = np.array([
    0.01, 0.01, 0.01, 0.01, 0.01, 0.02,  # 12am-5am (low)
    0.04, 0.06, 0.08, 0.07, 0.05, 0.06,  # 6am-11am (morning peak)
    0.07, 0.06, 0.05, 0.04, 0.05, 0.06,  # 12pm-5pm (lunch/afternoon)
    0.07, 0.08, 0.06, 0.04, 0.03, 0.02   # 6pm-11pm (evening peak)
])
HOUR_WEIGHTS = HOUR_WEIGHTS / HOUR_WEIGHTS.sum()

# Storage for all events
all_events = []

print("\nGenerating events by day...")

for day_offset in range(DAYS):
    current_date = START_DATE + timedelta(days=day_offset)
    day_num = day_offset + 1
    is_weekend = current_date.weekday() >= 5  # Saturday=5, Sunday=6

    print(f"Day {day_num} ({current_date.strftime('%Y-%m-%d')} - {'Weekend' if is_weekend else 'Weekday'}): ", end='')

    events_today = EVENTS_PER_DAY

    # OPPORTUNITY 1: Newsletter signups jump 45% on Day 4
    newsletter_boost = 1.45 if day_num == 4 else 1.0

    for i in range(events_today):
        # Select event type
        event_weights = list(EVENT_TYPES.values()).copy()
        if newsletter_boost > 1.0:
            # Increase newsletter_signup weight
            signup_idx = list(EVENT_TYPES.keys()).index('newsletter_signup')
            event_weights[signup_idx] *= newsletter_boost
            # Renormalize
            total = sum(event_weights)
            event_weights = [w/total for w in event_weights]

        event_name = np.random.choice(list(EVENT_TYPES.keys()), p=event_weights)

        # Select platform
        platform = np.random.choice(list(PLATFORMS.keys()), p=list(PLATFORMS.values()))

        # PROBLEM 1: iOS scroll_depth events stop after 2pm (14:00) on Day 3
        timestamp = random_timestamp(current_date, HOUR_WEIGHTS)
        if day_num >= 3 and platform == 'ios' and event_name == 'scroll_depth' and timestamp.hour >= 14:
            continue  # Skip this event (simulating tracking break)

        # User and session
        user_id = random.choice(USER_POOL)
        session_id = generate_session_id()

        # Geography and device
        country = np.random.choice(list(COUNTRIES.keys()), p=list(COUNTRIES.values()))
        device_category = np.random.choice(list(DEVICE_CATEGORIES.keys()), p=list(DEVICE_CATEGORIES.values()))

        # Content
        article_id = f"article_{random.randint(1000, 9999)}"
        section = random.choice(SECTIONS)

        # Referrer - OPPORTUNITY 3: Add reddit.com as new referral source on Day 5+
        referrer_weights = list(REFERRERS.values()).copy()
        referrer_keys = list(REFERRERS.keys()).copy()
        if day_num >= 5:
            # Add reddit with 10% share, reduce others proportionally
            referrer_keys.append('reddit.com')
            referrer_weights = [w * 0.9 for w in referrer_weights]
            referrer_weights.append(0.10)
            # Renormalize
            total = sum(referrer_weights)
            referrer_weights = [w/total for w in referrer_weights]

        referrer = np.random.choice(referrer_keys, p=referrer_weights)

        # Page location
        page_location = f"https://news-site.com/{section}/{article_id}"

        # PROBLEM 3: PII in URLs (5% of events)
        if random.random() < 0.05:
            fake_email = f"user{random.randint(1, 999)}@example.com"
            page_location += f"?email={fake_email}"

        # PROBLEM 2: 15% missing consent_state
        consent_state = None if random.random() < 0.15 else random.choice(['granted', 'denied'])

        # OPPORTUNITY 2: Weekend mobile readers stay 2x longer
        engagement_time = random.randint(5, 60)  # seconds
        if is_weekend and device_category == 'mobile':
            engagement_time *= 2

        # OPPORTUNITY 4: Push notification clicks spike Tuesday mornings (6am-10am)
        if event_name == 'push_notification_click' and current_date.weekday() == 1 and 6 <= timestamp.hour < 10:
            # Generate 3x more push click events during this window
            if random.random() > 0.67:
                continue  # Skip to reduce count back to normal elsewhere

        # Create event
        event = {
            'event_timestamp': int(timestamp.timestamp() * 1_000_000),  # microseconds
            'event_date': current_date.strftime('%Y%m%d'),
            'event_name': event_name,
            'user_pseudo_id': user_id,
            'platform': platform,
            'geo_country': country,
            'device_category': device_category,
            'page_location': page_location,
            'article_id': article_id,
            'section': section,
            'referrer': referrer,
            'consent_state': consent_state,
            'session_id': session_id,
            'engagement_time_msec': engagement_time * 1000
        }

        all_events.append(event)

        # PROBLEM 4: Create duplicates (1% of events)
        if random.random() < 0.01:
            duplicate = event.copy()
            all_events.append(duplicate)

    print(f"{len([e for e in all_events if e['event_date'] == current_date.strftime('%Y%m%d')]):,} events generated")

# Create DataFrame
print(f"\nCreating DataFrame with {len(all_events):,} total events...")
df = pd.DataFrame(all_events)

# Sort by timestamp
df = df.sort_values('event_timestamp').reset_index(drop=True)

# Convert timestamp to datetime for CSV readability
df['event_datetime'] = pd.to_datetime(df['event_timestamp'], unit='us')

# Reorder columns
columns = [
    'event_timestamp', 'event_datetime', 'event_date', 'event_name',
    'user_pseudo_id', 'session_id', 'platform', 'device_category',
    'geo_country', 'referrer', 'page_location', 'article_id', 'section',
    'consent_state', 'engagement_time_msec'
]
df = df[columns]

# Save to CSV
output_file = 'news_analytics_sample_data.csv'
print(f"\nSaving to {output_file}...")
df.to_csv(output_file, index=False)

print(f"\n✅ Generated {len(df):,} events")
print(f"✅ Date range: {df['event_datetime'].min()} to {df['event_datetime'].max()}")
print(f"✅ File size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")

# Generate summary statistics
print("\n" + "="*60)
print("DATA SUMMARY")
print("="*60)

print(f"\nEvent Distribution:")
print(df['event_name'].value_counts().to_string())

print(f"\nPlatform Distribution:")
print(df['platform'].value_counts().to_string())

print(f"\nConsent State (PROBLEM 2 - Should see ~15% null):")
print(df['consent_state'].value_counts(dropna=False).to_string())

print(f"\nPII Leaks (PROBLEM 3 - Should see ~5% with email param):")
pii_count = df['page_location'].str.contains('email=', na=False).sum()
print(f"Events with email in URL: {pii_count:,} ({pii_count/len(df)*100:.1f}%)")

print(f"\nDuplicates (PROBLEM 4 - Should see ~1%):")
duplicate_count = df.duplicated(subset=['user_pseudo_id', 'event_timestamp']).sum()
print(f"Duplicate events: {duplicate_count:,} ({duplicate_count/len(df)*100:.1f}%)")

print(f"\nReferrer Distribution (OPPORTUNITY 3 - reddit appears Day 5+):")
print(df.groupby('event_date')['referrer'].value_counts().unstack(fill_value=0).to_string())

print("\n" + "="*60)
print("PLANTED ISSUES SUMMARY")
print("="*60)
print("""
PROBLEMS:
✓ iOS scroll_depth stops after 2pm on Day 3
✓ ~15% of events missing consent_state
✓ ~5% events have PII (email) in page_location
✓ ~1% duplicate events

OPPORTUNITIES:
✓ Newsletter signups spike 45% on Day 4
✓ Weekend mobile engagement_time is 2x higher
✓ reddit.com appears as new referrer starting Day 5
✓ Push notification clicks spike Tuesday 6-10am
""")

print("\n✅ Sample data generation complete!")
print(f"Next step: Load {output_file} into BigQuery")
