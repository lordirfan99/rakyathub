#!/usr/bin/env python3
"""Dump all TaskKita Supabase data."""
import urllib.request, json, re, http.client

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"

# Get supabase anon key
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")
keys = re.findall(r'["\x27](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\x27]', data)
SUPABASE_KEY = keys[0] if keys else ""
print(f"Supabase KEY: {SUPABASE_KEY[:30]}...")

# Login
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
payload = json.dumps({"email": EMAIL, "password": PASSWORD})
headers = {"Content-Type": "application/json", "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
conn.request("POST", "/auth/v1/token?grant_type=password", body=payload, headers=headers)
body = json.loads(conn.getresponse().read().decode())
conn.close()
access_token = body.get("access_token", "")
print(f"Logged in: {EMAIL}")

# Headers for data access
headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
}

# Discover tables via schema introspection
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn.request("GET", "/rest/v1/?apikey=" + SUPABASE_KEY, headers=headers)
r = conn.getresponse()
schema = r.read().decode()
conn.close()
print(f"\nSchema response ({r.status}): {schema[:300]}")

# Known tables
tables = [
    "profiles", "campaigns", "orders", "wallet_transactions",
    "user_roles", "tasks", "pricing_tiers", "referrals",
    "withdrawals", "notifications", "reviews", "categories",
    "services", "products", "admins", "settings",
]

for table in tables:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        conn.request("GET", f"/rest/v1/{table}?select=*&limit=30", headers=headers)
        r = conn.getresponse()
        body = r.read().decode()
        conn.close()
        
        if r.status == 200:
            records = json.loads(body) if body.strip() else []
            if isinstance(records, list) and len(records) > 0:
                print(f"\n{'='*60}")
                print(f"TABLE: {table} ({len(records)} records)")
                print(f"{'='*60}")
                for rec in records[:5]:
                    print(f"  {json.dumps(rec, indent=2, default=str)[:400]}")
                    print()
            elif isinstance(records, list):
                print(f"\nTABLE: {table} (empty)")
            else:
                print(f"\nTABLE: {table}: {json.dumps(records, indent=2)[:200]}")
        elif r.status == 404:
            pass  # Skip
        elif r.status == 403:
            print(f"\nTABLE: {table} (403 Forbidden)")
        elif r.status == 401:
            print(f"\nTABLE: {table} (401 Unauthorized)")
        else:
            print(f"\nTABLE: {table} ({r.status}): {body[:100]}")
    except Exception as e:
        print(f"\nTABLE: {table}: Error - {str(e)[:100]}")
