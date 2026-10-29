#!/usr/bin/env python3
"""
Export CSV files to a Google Sheet (one tab per CSV), owned by your own account.

Uses OAuth (not service account — Google removed service account Drive quota
in 2025, so service accounts can no longer own files).

One-time setup:
  1. GCP console > OAuth consent screen: External, add your email as test user
  2. Credentials > Create OAuth client ID > Desktop app
  3. Download JSON to projects/_shared/oauth-client.json
First run opens a browser to authorize; token is cached for later runs.

Usage:
  python3 scripts/export-sheet.py --title "My Report" data1.csv data2.csv

Each CSV becomes a tab named after its filename (without .csv).
Prints the spreadsheet URL on success.
"""

import argparse
import csv
import sys
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
SHARED_DIR = Path(__file__).parent.parent / "projects" / "_shared"
CLIENT_PATH = SHARED_DIR / "oauth-client.json"
TOKEN_PATH = SHARED_DIR / "oauth-token.json"


def get_creds():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not CLIENT_PATH.exists():
            sys.exit(f"OAuth client not found at {CLIENT_PATH}\n"
                     "Create a Desktop OAuth client in GCP console and download the JSON there.")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json())
    TOKEN_PATH.chmod(0o600)
    return creds


def read_csv_rows(path: Path):
    with open(path, encoding="utf-8") as f:
        return [row for row in csv.reader(f)]


def main():
    parser = argparse.ArgumentParser(description="Export CSVs to a Google Sheet")
    parser.add_argument("--title", required=True, help="Spreadsheet title")
    parser.add_argument("csv_files", nargs="+", help="CSV files, one tab each")
    args = parser.parse_args()

    tabs = []
    for f in args.csv_files:
        p = Path(f)
        if not p.exists():
            sys.exit(f"File not found: {f}")
        tabs.append((p.stem, read_csv_rows(p)))

    creds = get_creds()
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)

    spreadsheet = sheets.spreadsheets().create(body={
        "properties": {"title": args.title},
        "sheets": [{"properties": {"title": name}} for name, _ in tabs],
    }).execute()
    sid = spreadsheet["spreadsheetId"]

    sheets.spreadsheets().values().batchUpdate(spreadsheetId=sid, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"'{name}'!A1", "values": rows}
            for name, rows in tabs
        ],
    }).execute()

    print(f"https://docs.google.com/spreadsheets/d/{sid}/edit")


if __name__ == "__main__":
    main()
