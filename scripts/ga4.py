#!/usr/bin/env python3
"""
GA4 data fetcher for Timbre SEO audit.

Usage:
  python3 scripts/ga4.py --project motquacam --mode top_pages
  python3 scripts/ga4.py --project motquacam --mode traffic_sources
  python3 scripts/ga4.py --project motquacam --mode page_metrics --url /sua-hat/
  python3 scripts/ga4.py --project motquacam --mode bounce_rate --days 28
  python3 scripts/ga4.py --project motquacam --mode trends --days 90
"""

import argparse
import json
import sys
import warnings
warnings.filterwarnings("ignore")
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression,
    Filter, OrderBy
)

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


def load_config(project: str):
    config_path = Path(__file__).parent.parent / "projects" / project / "config.env"
    if not config_path.exists():
        sys.exit(f"No config found at {config_path}")
    config = {}
    for line in config_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            config[k.strip()] = v.strip()
    return config


def get_client(key_path: str):
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return BetaAnalyticsDataClient(credentials=creds)


def date_range(days: int):
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    return DateRange(start_date=start.isoformat(), end_date=end.isoformat())


def fetch_top_pages(client, property_id: str, days: int = 28, limit: int = 30):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[date_range(days)],
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
        ],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=limit,
    )
    response = client.run_report(request)
    rows = []
    for row in response.rows:
        rows.append({
            "page": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "pageviews": int(row.metric_values[1].value),
            "engagement_rate": round(float(row.metric_values[2].value) * 100, 1),
            "avg_session_duration_s": round(float(row.metric_values[3].value)),
        })
    return {"mode": "top_pages", "period_days": days, "rows": rows}


def fetch_traffic_sources(client, property_id: str, days: int = 28):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[date_range(days)],
        dimensions=[Dimension(name="sessionDefaultChannelGroup")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="engagementRate"),
        ],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    )
    response = client.run_report(request)
    rows = []
    for row in response.rows:
        rows.append({
            "channel": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "new_users": int(row.metric_values[1].value),
            "engagement_rate": round(float(row.metric_values[2].value) * 100, 1),
        })
    return {"mode": "traffic_sources", "period_days": days, "rows": rows}


def fetch_page_metrics(client, property_id: str, url: str, days: int = 28):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[date_range(days)],
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="newUsers"),
        ],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(value=url, match_type=Filter.StringFilter.MatchType.EXACT),
            )
        ),
    )
    response = client.run_report(request)
    if not response.rows:
        return {"mode": "page_metrics", "url": url, "period_days": days, "data": None}
    row = response.rows[0]
    return {
        "mode": "page_metrics",
        "url": url,
        "period_days": days,
        "data": {
            "sessions": int(row.metric_values[0].value),
            "pageviews": int(row.metric_values[1].value),
            "engagement_rate": round(float(row.metric_values[2].value) * 100, 1),
            "avg_session_duration_s": round(float(row.metric_values[3].value)),
            "new_users": int(row.metric_values[4].value),
        },
    }


def fetch_bounce_rate(client, property_id: str, days: int = 28, limit: int = 30):
    """Pages with low engagement rate (high bounce) sorted by sessions."""
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[date_range(days)],
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
        ],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=limit,
    )
    response = client.run_report(request)
    rows = []
    for row in response.rows:
        sessions = int(row.metric_values[0].value)
        engagement = round(float(row.metric_values[1].value) * 100, 1)
        if sessions >= 10:
            rows.append({
                "page": row.dimension_values[0].value,
                "sessions": sessions,
                "engagement_rate": engagement,
                "bounce_rate": round(100 - engagement, 1),
                "avg_session_duration_s": round(float(row.metric_values[2].value)),
            })
    rows.sort(key=lambda x: x["bounce_rate"], reverse=True)
    return {"mode": "bounce_rate", "period_days": days, "rows": rows}


def fetch_trends(client, property_id: str, days: int = 90):
    """Weekly session trends to spot growing/declining pages."""
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[date_range(days)],
        dimensions=[Dimension(name="week"), Dimension(name="pagePath")],
        metrics=[Metric(name="sessions")],
        order_bys=[
            OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="week")),
            OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True),
        ],
        limit=200,
    )
    response = client.run_report(request)
    rows = []
    for row in response.rows:
        rows.append({
            "week": row.dimension_values[0].value,
            "page": row.dimension_values[1].value,
            "sessions": int(row.metric_values[0].value),
        })
    return {"mode": "trends", "period_days": days, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description="Fetch GA4 data for Timbre SEO audit")
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", required=True,
                        choices=["top_pages", "traffic_sources", "page_metrics", "bounce_rate", "trends"])
    parser.add_argument("--url", help="Page path for --mode page_metrics (e.g. /sua-hat/)")
    parser.add_argument("--days", type=int, default=28)
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    config = load_config(args.project)
    key_path = config.get("GSC_KEY_PATH")
    property_id = config.get("GA4_PROPERTY_ID")

    if not key_path or not property_id:
        sys.exit("Missing GSC_KEY_PATH or GA4_PROPERTY_ID in config.env")
    if not Path(key_path).exists():
        sys.exit(f"Service account key not found at {key_path}")

    client = get_client(key_path)

    if args.mode == "top_pages":
        result = fetch_top_pages(client, property_id, days=args.days, limit=args.limit)
    elif args.mode == "traffic_sources":
        result = fetch_traffic_sources(client, property_id, days=args.days)
    elif args.mode == "page_metrics":
        if not args.url:
            sys.exit("--url is required for --mode page_metrics")
        result = fetch_page_metrics(client, property_id, args.url, days=args.days)
    elif args.mode == "bounce_rate":
        result = fetch_bounce_rate(client, property_id, days=args.days, limit=args.limit)
    elif args.mode == "trends":
        result = fetch_trends(client, property_id, days=args.days)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
