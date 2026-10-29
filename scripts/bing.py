#!/usr/bin/env python3
"""
Bing Webmaster Tools data fetcher for Timbre SEO audit.

Bing counterpart of gsc.py. Each project is a SEPARATE Bing account, so the
API key is per-project: store it in the repo-root .env as
BING_API_KEY_<PROJECT> (e.g. BING_API_KEY_TOKEMIST). Generate the key in that
account's Bing Webmaster Tools > Settings > API access. A plain BING_API_KEY
is used as fallback when no per-project key is set. The (non-secret) site URL
goes in projects/[project]/config.env as BING_SITE_URL, or pass --site.

Usage:
  python3 scripts/bing.py --project tokemist --mode sites    # verify key + list verified sites
  python3 scripts/bing.py --project simplize --mode queries
  python3 scripts/bing.py --project simplize --mode pages --limit 50
  python3 scripts/bing.py --project simplize --mode traffic
  python3 scripts/bing.py --site https://simplize.vn --mode sitemaps
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://ssl.bing.com/webmaster/api.svc/json"

MODE_METHOD = {
    "sites": "GetUserSites",            # apikey only
    "queries": "GetQueryStats",         # top queries: clicks/impressions/avg position
    "pages": "GetPageStats",            # per-page stats
    "traffic": "GetRankAndTrafficStats",  # clicks/impressions by day
    "sitemaps": "GetFeeds",             # submitted sitemaps/feeds
}

_DATE_RE = re.compile(r"/Date\((-?\d+)")


def load_api_key(project: str | None) -> str:
    names = []
    if project:
        names.append("BING_API_KEY_" + project.upper().replace("-", "_"))
    names.append("BING_API_KEY")
    for n in names:
        v = os.environ.get(n)
        if v:
            return v.strip()
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        env = {}
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, val = line.split("=", 1)
                env[k.strip()] = val.strip()
        for n in names:
            if env.get(n):
                return env[n]
    sys.exit(f"No Bing API key found (looked for: {', '.join(names)}).\n"
             "Set it in .env. Get the key at that account's "
             "Bing Webmaster Tools > Settings > API access.")


def load_site(project: str | None, site: str | None) -> str:
    if site:
        return site
    if not project:
        sys.exit("This mode needs a site: pass --site or --project (reads BING_SITE_URL from config.env).")
    config_path = Path(__file__).parent.parent / "projects" / project / "config.env"
    if not config_path.exists():
        sys.exit(f"No config found at {config_path}")
    for line in config_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("BING_SITE_URL=") and not line.startswith("#"):
            return line.split("=", 1)[1].strip()
    sys.exit(f"Missing BING_SITE_URL in {config_path}")


def call(method: str, api_key: str, site_url: str | None = None):
    params = {"apikey": api_key}
    if site_url:
        params["siteUrl"] = site_url
    url = f"{API_BASE}/{method}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        sys.exit(f"Bing API HTTP {e.code} for {method}: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"Bing API request failed for {method}: {e.reason}")
    return data.get("d", data)


def iso_date(value):
    """Convert WCF /Date(ms)/ to YYYY-MM-DD; pass through anything else."""
    if isinstance(value, str):
        m = _DATE_RE.search(value)
        if m:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(int(m.group(1)) / 1000, tz=timezone.utc).date().isoformat()
    return value


def fetch_sites(api_key: str):
    rows = call("GetUserSites", api_key) or []
    return {"mode": "sites", "sites": [
        {"url": r.get("Url", ""), "is_verified": r.get("IsVerified", False)}
        for r in rows
    ]}


def fetch_queries(api_key: str, site_url: str, limit: int):
    rows = call("GetQueryStats", api_key, site_url) or []
    out = [{
        "query": r.get("Query", ""),
        "clicks": r.get("Clicks", 0),
        "impressions": r.get("Impressions", 0),
        "avg_click_position": r.get("AvgClickPosition", 0),
        "avg_impression_position": r.get("AvgImpressionPosition", 0),
        "date": iso_date(r.get("Date")),
    } for r in rows]
    out.sort(key=lambda x: x["clicks"], reverse=True)
    return {"mode": "queries", "site": site_url, "rows": out[:limit]}


def fetch_pages(api_key: str, site_url: str, limit: int):
    rows = call("GetPageStats", api_key, site_url) or []
    out = [{
        "page": r.get("Query", r.get("Page", "")),
        "clicks": r.get("Clicks", 0),
        "impressions": r.get("Impressions", 0),
        "avg_click_position": r.get("AvgClickPosition", 0),
        "avg_impression_position": r.get("AvgImpressionPosition", 0),
        "date": iso_date(r.get("Date")),
    } for r in rows]
    out.sort(key=lambda x: x["clicks"], reverse=True)
    return {"mode": "pages", "site": site_url, "rows": out[:limit]}


def fetch_traffic(api_key: str, site_url: str):
    rows = call("GetRankAndTrafficStats", api_key, site_url) or []
    out = [{
        "date": iso_date(r.get("Date")),
        "clicks": r.get("Clicks", 0),
        "impressions": r.get("Impressions", 0),
    } for r in rows]
    out.sort(key=lambda x: str(x["date"]))
    return {"mode": "traffic", "site": site_url, "rows": out}


def fetch_sitemaps(api_key: str, site_url: str):
    rows = call("GetFeeds", api_key, site_url) or []
    out = [{
        "url": r.get("Url", ""),
        "submitted": iso_date(r.get("Submitted")),
        "last_crawled": iso_date(r.get("LastCrawled")),
        "url_count": r.get("UrlCount", 0),
    } for r in rows]
    return {"mode": "sitemaps", "site": site_url, "sitemaps": out}


def main():
    parser = argparse.ArgumentParser(description="Fetch Bing Webmaster Tools data for Timbre SEO audit")
    parser.add_argument("--mode", required=True, choices=list(MODE_METHOD),
                        help="Data mode")
    parser.add_argument("--project", help="Project name (reads BING_SITE_URL from projects/<p>/config.env)")
    parser.add_argument("--site", help="Verified site URL (overrides --project)")
    parser.add_argument("--limit", type=int, default=100, help="Max rows for queries/pages (default 100)")
    args = parser.parse_args()

    api_key = load_api_key(args.project)

    if args.mode == "sites":
        result = fetch_sites(api_key)
    else:
        site_url = load_site(args.project, args.site)
        if args.mode == "queries":
            result = fetch_queries(api_key, site_url, args.limit)
        elif args.mode == "pages":
            result = fetch_pages(api_key, site_url, args.limit)
        elif args.mode == "traffic":
            result = fetch_traffic(api_key, site_url)
        elif args.mode == "sitemaps":
            result = fetch_sitemaps(api_key, site_url)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
