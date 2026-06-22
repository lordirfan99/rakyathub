#!/usr/bin/env python3
"""Submit updated sitemap to GSC."""
import json, os, requests

BASE = os.path.expanduser("~/AppData/Local/hermes")
TOKEN_FILE = os.path.join(BASE, "google_token.json")
SECRET_FILE = os.path.join(BASE, "google_client_secret.json")
DOMAIN = "rakyathub.my"
SITEMAP = "https://rakyathub.my/sitemap-index.xml"

with open(TOKEN_FILE) as f: tok = json.load(f)
with open(SECRET_FILE) as f: sec = json.load(f)
data = {
    "client_id": sec.get("installed", sec).get("client_id"),
    "client_secret": sec.get("installed", sec).get("client_secret"),
    "refresh_token": tok.get("refresh_token"),
    "grant_type": "refresh_token"
}
r = requests.post("https://oauth2.googleapis.com/token", data=data, timeout=10)
access = r.json()["access_token"]
headers = {"Authorization": f"Bearer {access}"}

# Submit sitemap
encoded = requests.utils.quote(SITEMAP, safe="")
r2 = requests.put(f"https://www.googleapis.com/webmasters/v3/sites/sc-domain:{DOMAIN}/sitemaps/{encoded}", headers=headers, timeout=15)
print(f"GSC sitemap submit: HTTP {r2.status_code}")

# Check sitemap stats
r3 = requests.get(f"https://www.googleapis.com/webmasters/v3/sites/sc-domain:{DOMAIN}/sitemaps", headers=headers, timeout=15)
if r3.status_code == 200:
    for s in r3.json().get("sitemap", []):
        c = s.get("contents", [{}])[0] if s.get("contents") else {}
        sub = int(c.get("submitted", 0))
        idx = int(c.get("indexed", 0))
        err = int(s.get("errors", 0))
        print(f"  {s.get('path','').split('/')[-1]}: submitted={sub} indexed={idx} errors={err}")
print("Done")
