#!/usr/bin/env python3
"""
GSC data fetcher for Timbre SEO audit.

Usage:
  python3 scripts/gsc.py --project motquacam --mode analytics
  python3 scripts/gsc.py --project motquacam --mode inspect --url https://motquacam.com/sua-hat/
  python3 scripts/gsc.py --project motquacam --mode sitemaps
  python3 scripts/gsc.py --project motquacam --mode analytics --page https://motquacam.com/sua-hat/ --days 28
"""

import argparse
import json
import os
import sys
import warnings
warnings.filterwarnings("ignore")
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
]


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


def get_service(key_path: str):
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def fetch_analytics(service, site_url: str, page: str = None, days: int = 28):
    end = date.today() - timedelta(days=2)  # GSC has ~2 day lag
    start = end - timedelta(days=days - 1)

    dimensions = ["query", "page"] if not page else ["query"]
    request = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": dimensions,
        "rowLimit": 100,
        "startRow": 0,
    }
    if page:
        request["dimensionFilterGroups"] = [{
            "filters": [{"dimension": "page", "operator": "equals", "expression": page}]
        }]

    result = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    rows = result.get("rows", [])

    output = []
    for row in rows:
        keys = row.get("keys", [])
        entry = {
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        }
        if not page:
            entry["query"] = keys[0] if len(keys) > 0 else ""
            entry["page"] = keys[1] if len(keys) > 1 else ""
        else:
            entry["query"] = keys[0] if keys else ""
        output.append(entry)

    return {"mode": "analytics", "site": site_url, "period_days": days, "rows": output}


def fetch_inspect(service, site_url: str, url: str):
    result = service.urlInspection().index().inspect(body={
        "inspectionUrl": url,
        "siteUrl": site_url,
    }).execute()

    result_data = result.get("inspectionResult", {})
    index_result = result_data.get("indexStatusResult", {})
    mobile_result = result_data.get("mobileUsabilityResult", {})
    rich_results = result_data.get("richResultsResult", {})

    # Parse detailed rich results issues per type
    rich_details = []
    for detected in rich_results.get("detectedItems", []):
        rtype = detected.get("richResultType", "")
        for item in detected.get("items", []):
            issues = [
                {"message": i.get("issueMessage", ""), "severity": i.get("severity", "")}
                for i in item.get("issues", [])
            ]
            rich_details.append({
                "type": rtype,
                "name": item.get("name", ""),
                "issues": issues,
            })

    return {
        "mode": "inspect",
        "url": url,
        "verdict": index_result.get("verdict", "UNKNOWN"),
        "coverage_state": index_result.get("coverageState", ""),
        "last_crawl_time": index_result.get("lastCrawlTime", ""),
        "crawled_as": index_result.get("crawledAs", ""),
        "canonical": {
            "google": index_result.get("googleCanonical", ""),
            "user_declared": index_result.get("userCanonical", ""),
        },
        "mobile_usability": mobile_result.get("verdict", "UNKNOWN"),
        "mobile_issues": [i.get("issueType", "") for i in mobile_result.get("issues", [])],
        "rich_results_verdict": rich_results.get("verdict", ""),
        "rich_results": rich_details,
    }


def fetch_sitemaps(service, site_url: str):
    result = service.sitemaps().list(siteUrl=site_url).execute()
    sitemaps = result.get("sitemap", [])

    output = []
    for sm in sitemaps:
        output.append({
            "path": sm.get("path", ""),
            "last_submitted": sm.get("lastSubmitted", ""),
            "last_downloaded": sm.get("lastDownloaded", ""),
            "is_pending": sm.get("isPending", False),
            "is_sitemaps_index": sm.get("isSitemapsIndex", False),
            "contents": [
                {"type": c.get("type", ""), "submitted": c.get("submitted", 0), "indexed": c.get("indexed", 0)}
                for c in sm.get("contents", [])
            ],
            "errors": sm.get("errors", 0),
            "warnings": sm.get("warnings", 0),
        })

    return {"mode": "sitemaps", "site": site_url, "sitemaps": output}


def fetch_low_ctr_pages(service, site_url: str, days: int = 28):
    """Pages with impressions > 100 but CTR < 3% — title/meta optimization candidates."""
    end = date.today() - timedelta(days=2)
    start = end - timedelta(days=days - 1)

    result = service.searchanalytics().query(siteUrl=site_url, body={
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": ["page"],
        "rowLimit": 100,
    }).execute()

    rows = result.get("rows", [])
    candidates = []
    for row in rows:
        impressions = row.get("impressions", 0)
        ctr = row.get("ctr", 0) * 100
        if impressions >= 100 and ctr < 3.0:
            candidates.append({
                "page": row["keys"][0],
                "impressions": impressions,
                "clicks": row.get("clicks", 0),
                "ctr": round(ctr, 2),
                "position": round(row.get("position", 0), 1),
            })

    candidates.sort(key=lambda x: x["impressions"], reverse=True)
    return {"mode": "low_ctr", "site": site_url, "period_days": days, "pages": candidates}


def main():
    parser = argparse.ArgumentParser(description="Fetch GSC data for Timbre SEO audit")
    parser.add_argument("--project", required=True, help="Project name (e.g. motquacam)")
    parser.add_argument("--mode", required=True,
                        choices=["analytics", "inspect", "sitemaps", "low_ctr"],
                        help="Data mode")
    parser.add_argument("--url", help="URL to inspect (required for --mode inspect)")
    parser.add_argument("--page", help="Filter analytics to a specific page URL")
    parser.add_argument("--days", type=int, default=28, help="Days of analytics data (default 28)")
    args = parser.parse_args()

    config = load_config(args.project)
    site_url = config.get("GSC_SITE_URL")
    key_path = config.get("GSC_KEY_PATH")

    if not site_url or not key_path:
        sys.exit("Missing GSC_SITE_URL or GSC_KEY_PATH in config.env")
    if not Path(key_path).exists():
        sys.exit(f"Service account key not found at {key_path}\nSee projects/{args.project}/credentials/")

    service = get_service(key_path)

    if args.mode == "analytics":
        result = fetch_analytics(service, site_url, page=args.page, days=args.days)
    elif args.mode == "inspect":
        if not args.url:
            sys.exit("--url is required for --mode inspect")
        result = fetch_inspect(service, site_url, args.url)
    elif args.mode == "sitemaps":
        result = fetch_sitemaps(service, site_url)
    elif args.mode == "low_ctr":
        result = fetch_low_ctr_pages(service, site_url, days=args.days)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
