#!/usr/bin/env python3
"""Inspect a few representative RakyatHub URLs via GSC API."""
import json, os, requests

BASE = os.path.expanduser("~/AppData/Local/hermes")
TOKEN_FILE = os.path.join(BASE, "google_token.json")
SECRET_FILE = os.path.join(BASE, "google_client_secret.json")
DOMAIN = "rakyathub.my"

with open(TOKEN_FILE) as f:
    token = json.load(f)
with open(SECRET_FILE) as f:
    secret = json.load(f)

data = {
    "client_id": secret.get("installed", secret).get("client_id"),
    "client_secret": secret.get("installed", secret).get("client_secret"),
    "refresh_token": token.get("refresh_token"),
    "grant_type": "refresh_token"
}
r = requests.post("https://oauth2.googleapis.com/token", data=data, timeout=10)
access_token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

test_urls = [
    "https://rakyathub.my/",
    "https://rakyathub.my/blog",
    "https://rakyathub.my/scam-cinta-online-2026-red-flag-elak-ditipu",
    "https://rakyathub.my/reality-check/selangor/ict",
    "https://rakyathub.my/harga-makanan-ayam-standard",
    "https://rakyathub.my/cara-simpan-duit-gaji-rm2500",
]

for url in test_urls:
    try:
        r2 = requests.post(
            "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
            json={"inspectionUrl": url, "siteUrl": f"sc-domain:{DOMAIN}"},
            headers=headers,
            timeout=20
        )
        if r2.status_code == 200:
            insp = r2.json().get("inspectionResult", {})
            isr = insp.get("indexStatusResult", {})
            cov = isr.get("coverageState", "N/A")
            verdict = isr.get("verdict", "N/A")
            crawl = isr.get("lastCrawlTime", "N/A")
            print(f"URL: {url}")
            print(f"  Verdict: {verdict}")
            print(f"  Coverage: {cov}")
            print(f"  Last crawl: {crawl[:19] if crawl != 'N/A' else 'N/A'}")
            issues = isr.get("crawlingErrors", [])
            if issues:
                print(f"  Crawl errors: {issues}")
            print()
        else:
            print(f"URL: {url} -- HTTP {r2.status_code}")
            if r2.status_code == 429:
                print("  (rate limited)")
                break
            print()
    except Exception as e:
        print(f"URL: {url} -- Error: {e}")
        print()
