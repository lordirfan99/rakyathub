#!/usr/bin/env python3
"""Explore packages and order flow in TaskKita."""
import urllib.request, json, re, http.client

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"

# Login
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
keys = re.findall(r'["\x27](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\x27]',
    req.read().decode(errors="replace"))
SUPABASE_KEY = keys[0]

conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
payload = json.dumps({"email": EMAIL, "password": PASSWORD})
h = {"Content-Type": "application/json", "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
conn.request("POST", "/auth/v1/token?grant_type=password", body=payload, headers=h)
body = json.loads(conn.getresponse().read().decode())
conn.close()
access_token = body.get("access_token", "")
user_id = body.get("user", {}).get("id", "")

h2 = {"Content-Type": "application/json", "apikey": SUPABASE_KEY, "Authorization": f"Bearer {access_token}",
      "Accept": "application/json", "Prefer": "return=representation"}

# Explore hinted tables
print("=== PACKAGES ===")
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn.request("GET", "/rest/v1/packages?select=*&limit=30", headers=h2)
r = conn.getresponse()
data = json.loads(r.read().decode()) if r.status == 200 else []
conn.close()
if data:
    for pkg in data:
        print(f"  {json.dumps(pkg, indent=2)[:300]}\n")
else:
    print(f"  Status {r.status}")

print("=== RESELLER_FOLDERS ===")
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn.request("GET", "/rest/v1/reseller_folders?select=*&limit=30", headers=h2)
r = conn.getresponse()
data = json.loads(r.read().decode()) if r.status == 200 else []
conn.close()
if data:
    for f in data:
        print(f"  {json.dumps(f, indent=2)[:300]}\n")

# Try to discover more tables by sending intentional errors
known_tables = [
    "packages", "reseller_folders", "orders", "campaigns",
    "order_items", "package_orders", "transactions",
    "commission_logs", "admin_logs", "tasks",
    "package_purchases", "service_orders",
]

for table in known_tables:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        # Try a minimal POST to discover column structure
        conn.request("POST", f"/rest/v1/{table}", json.dumps({"test": "value"}), headers=h2)
        r = conn.getresponse()
        body = r.read().decode()
        conn.close()
        if r.status == 400 and "column" in body:
            # Extract column name from error
            col = re.search(r"column ['\"](\w+)['\"]", body)
            print(f"\n  {table}: exists (error: {body[:100]})")
        elif r.status == 404:
            print(f"\n  {table}: 404")
        elif r.status == 201 or r.status == 200:
            print(f"\n  {table}: {r.status} - ACCESSIBLE! {body[:100]}")
        elif r.status == 403:
            print(f"\n  {table}: 403 - RLS blocked")
        elif r.status == 400:
            print(f"\n  {table}: 400 - {body[:150]}")
    except Exception as e:
        pass

# Check orders schema  
print("\n=== ORDERS SCHEMA ===")
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn.request("POST", "/rest/v1/orders", json.dumps({"user_id": user_id, "status": "test"}), headers=h2)
r = conn.getresponse()
body = r.read().decode()
conn.close()
print(f"  {r.status}: {body[:200]}")
