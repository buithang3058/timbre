#!/usr/bin/env python3
"""
IndexNow submitter for Timbre (pings Bing; shared with partner engines).

IndexNow lets you notify search engines the instant a URL is added/updated/
removed so they recrawl fast. Unlike the Webmaster API it needs no account
key: you pick a key, host it at https://<host>/<key>.txt to prove ownership,
then submit URLs. Key is PUBLIC (hosted on the site) so it lives in
projects/<project>/config.env as INDEXNOW_KEY, next to BING_SITE_URL.

Usage:
  python3 scripts/indexnow.py --project tokemist --mode genkey
      --keyfile-dir /Users/buithang/tokemist/web/public   # also drops <key>.txt
  python3 scripts/indexnow.py --project tokemist --mode verify
  python3 scripts/indexnow.py --project tokemist --mode submit \
      --url https://tokemist.com/a/ --url https://tokemist.com/b/
  python3 scripts/indexnow.py --project tokemist --mode submit --urls-file urls.txt
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://www.bing.com/indexnow"


def config_path(project: str) -> Path:
    return Path(__file__).parent.parent / "projects" / project / "config.env"


def load_config(project: str) -> dict:
    path = config_path(project)
    if not path.exists():
        sys.exit(f"No config found at {path}")
    config = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            config[k.strip()] = v.strip()
    return config


def host_of(url: str) -> str:
    return urllib.parse.urlparse(url).netloc


def do_genkey(project: str, keyfile_dir: str | None):
    key = secrets.token_hex(16)  # 32 hex chars, valid IndexNow key
    path = config_path(project)
    existing = load_config(project)
    if existing.get("INDEXNOW_KEY"):
        sys.exit(f"INDEXNOW_KEY already set in {path}. Remove it first to regenerate.")
    with path.open("a") as f:
        f.write(f"INDEXNOW_KEY={key}\n")

    result = {"mode": "genkey", "project": project, "key": key,
              "wrote_config": str(path), "keyfile_name": f"{key}.txt"}

    if keyfile_dir:
        kf = Path(keyfile_dir) / f"{key}.txt"
        kf.write_text(key)
        result["keyfile_written"] = str(kf)
        result["next"] = "Deploy the site so the key file is live, then run --mode verify."
    else:
        result["next"] = (f"Host a file named {key}.txt (content = the key) at your "
                          "site root, deploy, then run --mode verify.")
    return result


def do_verify(project: str):
    config = load_config(project)
    key = config.get("INDEXNOW_KEY")
    site = config.get("BING_SITE_URL")
    if not key or not site:
        sys.exit("Need INDEXNOW_KEY and BING_SITE_URL in config.env (run --mode genkey first).")
    key_url = f"https://{host_of(site)}/{key}.txt"
    # Some hosts/CDNs 403 the default Python-urllib UA, so send a browser-like one.
    req = urllib.request.Request(key_url, headers={"User-Agent": "Mozilla/5.0 (Timbre IndexNow)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8").strip()
            code = resp.status
    except urllib.error.HTTPError as e:
        return {"mode": "verify", "key_url": key_url, "ok": False,
                "error": f"HTTP {e.code} — key file not reachable (deploy it?)"}
    except urllib.error.URLError as e:
        return {"mode": "verify", "key_url": key_url, "ok": False, "error": str(e.reason)}
    return {"mode": "verify", "key_url": key_url, "http": code,
            "ok": body == key,
            "note": "" if body == key else f"File content != key (got: {body[:64]!r})"}


def do_submit(project: str, urls: list[str]):
    config = load_config(project)
    key = config.get("INDEXNOW_KEY")
    site = config.get("BING_SITE_URL")
    if not key or not site:
        sys.exit("Need INDEXNOW_KEY and BING_SITE_URL in config.env (run --mode genkey first).")
    host = host_of(site)
    bad = [u for u in urls if host_of(u) != host]
    if bad:
        sys.exit(f"These URLs are not on host {host}: {bad}")

    payload = json.dumps({
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=payload, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code, body = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read().decode("utf-8", "replace")
    except urllib.error.URLError as e:
        sys.exit(f"IndexNow request failed: {e.reason}")

    meaning = {200: "accepted", 202: "accepted, key validation pending",
               400: "bad request", 403: "key not valid (file missing/mismatch)",
               422: "URLs/key mismatch with host", 429: "too many requests"}
    return {"mode": "submit", "host": host, "submitted": len(urls),
            "http": code, "status": meaning.get(code, "unknown"),
            "body": body.strip()[:200]}


def main():
    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow (Bing)")
    parser.add_argument("--project", required=True, help="Project name (reads projects/<p>/config.env)")
    parser.add_argument("--mode", required=True, choices=["genkey", "verify", "submit"])
    parser.add_argument("--keyfile-dir", help="genkey: also write <key>.txt into this dir (site public root)")
    parser.add_argument("--url", action="append", default=[], help="submit: a URL (repeatable)")
    parser.add_argument("--urls-file", help="submit: file with one URL per line")
    args = parser.parse_args()

    if args.mode == "genkey":
        result = do_genkey(args.project, args.keyfile_dir)
    elif args.mode == "verify":
        result = do_verify(args.project)
    else:
        urls = list(args.url)
        if args.urls_file:
            urls += [l.strip() for l in Path(args.urls_file).read_text().splitlines() if l.strip()]
        if not urls:
            sys.exit("submit needs --url and/or --urls-file")
        result = do_submit(args.project, urls)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
