"""
Analytics Intelligence Module

Core utilities for the NPA workshop system:
- BigQuery connection and query execution
- AI-powered SQL generation
- Anomaly detection and classification
- Slack alerting
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import yaml

from google.cloud import bigquery
import openai


class BigQueryConnector:
    """Handle BigQuery connections and query execution."""

    def __init__(self, project_id: str, dataset_id: str, table_id: str):
        """
        Initialize BigQuery connector.

        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset name
            table_id: BigQuery table name
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.{table_id}"

    def query(self, sql: str) -> List[Dict]:
        """
        Execute SQL query and return results as list of dicts.

        Args:
            sql: SQL query string

        Returns:
            List of row dictionaries
        """
        query_job = self.client.query(sql)
        results = query_job.result()

        # Convert to list of dicts
        rows = []
        for row in results:
            rows.append(dict(row.items()))

        return rows

    def get_table_info(self) -> Dict[str, Any]:
        """Get table metadata and sample data."""
        table = self.client.get_table(self.table_ref)

        return {
            'num_rows': table.num_rows,
            'size_mb': table.num_bytes / 1024 / 1024,
            'schema': [{'name': field.name, 'type': field.field_type} for field in table.schema],
            'created': table.created,
            'modified': table.modified
        }

    def get_date_range(self) -> Dict[str, str]:
        """Get min/max dates in the table."""
        sql = f"""
        SELECT
            MIN(event_date) as min_date,
            MAX(event_date) as max_date
        FROM `{self.table_ref}`
        """
        result = self.query(sql)[0]
        return result

    def get_event_volume(self, lookback_days: int = 7) -> List[Dict]:
        """Get event volume by date for recent days."""
        sql = f"""
        SELECT
            event_date,
            COUNT(*) as event_count,
            COUNT(DISTINCT user_pseudo_id) as unique_users
        FROM `{self.table_ref}`
        WHERE event_date >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {lookback_days} DAY))
        GROUP BY event_date
        ORDER BY event_date
        """
        return self.query(sql)


class SQLGenerator:
    """Generate SQL queries using AI based on check descriptions."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize SQL generator.

        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate_sql(
        self,
        check_description: str,
        table_ref: str,
        schema: List[Dict[str, str]],
        examples: Optional[str] = None
    ) -> str:
        """
        Generate SQL query based on natural language description.

        Args:
            check_description: Natural language description of what to check
            table_ref: Fully qualified table reference (project.dataset.table)
            schema: List of column definitions [{'name': 'col', 'type': 'STRING'}, ...]
            examples: Optional example SQL queries for few-shot prompting

        Returns:
            Generated SQL query string
        """
        schema_str = "\n".join([f"  - {col['name']} ({col['type']})" for col in schema])

        prompt = f"""You are a BigQuery SQL expert. Generate a SQL query for the following data quality check.

Table: {table_ref}

Schema:
{schema_str}

Check description: {check_description}

Requirements:
1. Use standard SQL syntax (BigQuery)
2. Include only columns that exist in the schema
3. Return results that would indicate a problem or anomaly
4. Limit results to 100 rows for efficiency
5. Include relevant context columns (date, platform, event_name, etc.)
6. Use appropriate aggregations and GROUP BY when needed
7. Add comments to explain the query logic

{f"Example queries for reference:\n{examples}\n" if examples else ""}

Generate the SQL query:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a SQL expert. Generate only valid BigQuery SQL queries. Do not include explanations outside the SQL comments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # Lower temperature for more consistent SQL
        )

        sql = response.choices[0].message.content.strip()

        # Clean up markdown code blocks if present
        if sql.startswith("```sql"):
            sql = sql.replace("```sql", "").replace("```", "").strip()
        elif sql.startswith("```"):
            sql = sql.replace("```", "").strip()

        return sql


class AnomalyClassifier:
    """Classify query results as problems or opportunities using AI."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize anomaly classifier.

        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def classify(
        self,
        check_name: str,
        check_description: str,
        results: List[Dict],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Classify query results using OpenAI function calling.

        Args:
            check_name: Name of the check
            check_description: Description of what was checked
            results: Query results (list of row dicts)
            context: Additional context (table stats, recent trends, etc.)

        Returns:
            Classification dict with severity, category, message, and recommendation
        """
        # Summarize results for the prompt
        result_summary = f"Found {len(results)} rows. "
        if results:
            result_summary += f"Sample: {results[0]}"

        functions = [
            {
                "name": "classify_finding",
                "description": "Classify an analytics finding as a problem or opportunity",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["problem_critical", "problem_minor", "opportunity", "insight", "noise"],
                            "description": "Category: problem_critical (tracking broken, PII leak), problem_minor (data quality), opportunity (positive change), insight (pattern worth noting), noise (expected variance)"
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["high", "medium", "low"],
                            "description": "Severity level"
                        },
                        "title": {
                            "type": "string",
                            "description": "Short title for Slack alert (max 100 chars)"
                        },
                        "message": {
                            "type": "string",
                            "description": "Detailed explanation of the finding"
                        },
                        "recommendation": {
                            "type": "string",
                            "description": "Recommended action to take"
                        },
                        "emoji": {
                            "type": "string",
                            "description": "Emoji for alert: 🚨 critical, ⚠️ minor, 🎉 opportunity, 📊 insight, 🔍 noise"
                        }
                    },
                    "required": ["category", "severity", "title", "message", "recommendation", "emoji"]
                }
            }
        ]

        prompt = f"""Analyze this analytics finding and classify it.

Check name: {check_name}
Description: {check_description}
Results: {result_summary}
{f"Context: {context}" if context else ""}

Determine if this is:
- problem_critical: Tracking is broken, PII leak, or major data issue
- problem_minor: Data quality issue that should be fixed but not urgent
- opportunity: Positive change worth investigating (spike in conversions, new high-value traffic source)
- insight: Interesting pattern or trend worth noting
- noise: Expected variance, not actionable

Provide classification:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            functions=functions,
            function_call={"name": "classify_finding"}
        )

        # Parse function call result
        function_call = response.choices[0].message.function_call
        import json
        classification = json.loads(function_call.arguments)

        classification['check_name'] = check_name
        classification['result_count'] = len(results)
        classification['timestamp'] = datetime.utcnow().isoformat()

        return classification


class SlackAlerter:
    """Send alerts to Slack via webhook."""

    def __init__(self, webhook_url: str):
        """
        Initialize Slack alerter.

        Args:
            webhook_url: Slack webhook URL
        """
        self.webhook_url = webhook_url

    def send_alert(self, classification: Dict[str, Any], results: Optional[List[Dict]] = None):
        """
        Send alert to Slack.

        Args:
            classification: Classification dict from AnomalyClassifier
            results: Optional query results to include in details
        """
        import requests

        emoji = classification.get('emoji', '📊')
        title = classification.get('title', 'Analytics Alert')
        message = classification.get('message', '')
        severity = classification.get('severity', 'low')
        category = classification.get('category', 'insight')
        recommendation = classification.get('recommendation', '')

        # Color based on category
        color_map = {
            'problem_critical': '#FF0000',  # Red
            'problem_minor': '#FFA500',     # Orange
            'opportunity': '#00FF00',        # Green
            'insight': '#0000FF',            # Blue
            'noise': '#808080'               # Gray
        }
        color = color_map.get(category, '#808080')

        # Build Slack message
        slack_message = {
            "text": f"{emoji} {title}",
            "attachments": [
                {
                    "color": color,
                    "fields": [
                        {
                            "title": "Category",
                            "value": category.replace('_', ' ').title(),
                            "short": True
                        },
                        {
                            "title": "Severity",
                            "value": severity.title(),
                            "short": True
                        },
                        {
                            "title": "Details",
                            "value": message,
                            "short": False
                        },
                        {
                            "title": "Recommendation",
                            "value": recommendation,
                            "short": False
                        }
                    ],
                    "footer": f"Analytics Intelligence | {classification.get('timestamp', '')}",
                    "mrkdwn_in": ["fields"]
                }
            ]
        }

        # Add sample results if provided
        if results and len(results) > 0:
            result_text = "Sample results:\n```\n"
            for row in results[:3]:  # First 3 rows
                result_text += f"{row}\n"
            result_text += "```"
            slack_message["attachments"][0]["fields"].append({
                "title": f"Sample Results ({len(results)} total)",
                "value": result_text,
                "short": False
            })

        # Send to Slack
        response = requests.post(self.webhook_url, json=slack_message)
        response.raise_for_status()

        return response.status_code == 200


class CheckRunner:
    """Run checks from YAML configuration."""

    def __init__(
        self,
        bq_connector: BigQueryConnector,
        sql_generator: SQLGenerator,
        classifier: AnomalyClassifier,
        alerter: Optional[SlackAlerter] = None
    ):
        """
        Initialize check runner.

        Args:
            bq_connector: BigQuery connector
            sql_generator: SQL generator
            classifier: Anomaly classifier
            alerter: Optional Slack alerter
        """
        self.bq = bq_connector
        self.sql_gen = sql_generator
        self.classifier = classifier
        self.alerter = alerter

    def load_checks(self, yaml_file: str) -> List[Dict]:
        """Load check definitions from YAML file."""
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('checks', [])

    def run_check(self, check: Dict) -> Dict[str, Any]:
        """
        Run a single check.

        Args:
            check: Check definition dict

        Returns:
            Check result with classification
        """
        check_name = check['name']
        check_description = check['description']

        print(f"Running check: {check_name}")

        # Generate SQL if not provided
        if 'sql' in check:
            sql = check['sql']
        else:
            table_info = self.bq.get_table_info()
            sql = self.sql_gen.generate_sql(
                check_description=check_description,
                table_ref=self.bq.table_ref,
                schema=table_info['schema'],
                examples=check.get('examples')
            )
            print(f"Generated SQL:\n{sql}\n")

        # Execute query
        results = self.bq.query(sql)
        print(f"Found {len(results)} results")

        # Classify if results found
        if len(results) > 0:
            classification = self.classifier.classify(
                check_name=check_name,
                check_description=check_description,
                results=results
            )
            print(f"Classification: {classification['category']} ({classification['severity']})")

            # Send alert if configured
            if self.alerter and classification['category'] != 'noise':
                print("Sending Slack alert...")
                self.alerter.send_alert(classification, results)

            return {
                'check': check_name,
                'sql': sql,
                'results': results,
                'classification': classification
            }
        else:
            print("No results found - check passed")
            return {
                'check': check_name,
                'sql': sql,
                'results': [],
                'classification': None
            }

    def run_all_checks(self, yaml_file: str) -> List[Dict[str, Any]]:
        """
        Run all checks from YAML file.

        Args:
            yaml_file: Path to checks YAML file

        Returns:
            List of check results
        """
        checks = self.load_checks(yaml_file)
        results = []

        print(f"Running {len(checks)} checks from {yaml_file}\n")

        for check in checks:
            try:
                result = self.run_check(check)
                results.append(result)
                print()
            except Exception as e:
                print(f"Error running check {check.get('name', 'unknown')}: {e}\n")
                results.append({
                    'check': check.get('name', 'unknown'),
                    'error': str(e)
                })

        return results
