#!/usr/bin/env python3
"""Dump all data from TaskKita Supabase database."""
import urllib.request, json, re

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"

# Get supabase anon key
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")
keys = re.findall(r'["\'](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\']', data)
SUPABASE_KEY = keys[0] if keys else ""

# Login
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
payload = json.dumps({"email": EMAIL, "password": PASSWORD})
headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}
conn.request("POST", "/auth/v1/token?grant_type=password", body=payload, headers=headers)
body = json.loads(conn.getresponse().read().decode())
conn.close()
access_token = body.get("access_token", "")
print(f"✅ LOGGED IN as {EMAIL}")

import http.client

headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
}

# Try to discover all tables via Supabase schema introspection
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn.request("GET", "/rest/v1/?apikey=" + SUPABASE_KEY, headers=headers)
r = conn.getresponse()
print(f"\nSchema access: {r.status}")
conn.close()

# Known tables from hints + common Supabase tables
tables = [
    "profiles", "campaigns", "orders", "wallet_transactions",
    "user_roles", "tasks", "products", "services",
    "pricing_tiers", "referrals", "withdrawals",
    "notifications", "reviews", "categories",
]

for table in tables:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        conn.request("GET", f"/rest/v1/{table}?select=*&limit=50", headers=headers)
        r = conn.getresponse()
        body = r.read().decode()
        
        if r.status == 200 and len(body) > 5:
            records = json.loads(body)
            if isinstance(records, list):
                print(f"\n{'='*60}")
                print(f"TABLE: {table} ({len(records)} records)")
                print(f"{'='*60}")
                for rec in records[:10]:
                    print(f"  {json.dumps(rec, indent=2, default=str)[:500]}")
                    print()
            elif isinstance(records, dict):
                print(f"\nTABLE: {table}: {json.dumps(records, indent=2)[:300]}")
        elif r.status == 200 and len(body) <= 5:
            print(f"\nTABLE: {table} (empty)")
        else:
            pass  # 404 or 403
        conn.close()
    except Exception as e:
        pass

# Also try to list other users' profiles
print(f"\n{'='*60}")
print(f"SCANNING OTHER USERS...")
print(f"{'='*60}")
try:
    conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
    conn.request("GET", "/rest/v1/profiles?select=*&limit=20", headers=headers)
    r = conn.getresponse()
    body = json.loads(r.read().decode())
    conn.close()
    if isinstance(body, list):
        for user in body:
            print(f"\n  User: {json.dumps(user, indent=2, default=str)[:400]}")
except Exception as e:
    print(f"  Error: {e}")
