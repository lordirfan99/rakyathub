#!/usr/bin/env python3
"""Attempt to add balance to TaskKita account."""
import urllib.request, json, re, http.client

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"

# Get anon key
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
keys = re.findall(r'["\x27](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\x27]',
    req.read().decode(errors="replace"))
SUPABASE_KEY = keys[0]

# Login
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
payload = json.dumps({"email": EMAIL, "password": PASSWORD})
headers = {"Content-Type": "application/json", "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
conn.request("POST", "/auth/v1/token?grant_type=password", body=payload, headers=headers)
body = json.loads(conn.getresponse().read().decode())
conn.close()
access_token = body.get("access_token", "")
user_id = body.get("user", {}).get("id", "")
print(f"User ID: {user_id}")

headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "Prefer": "return=representation",
}

methods = [
    ("PATCH balance direct", "PATCH", f"/rest/v1/profiles?id=eq.{user_id}", {"balance": 500.00}),
    ("PATCH balance string", "PATCH", f"/rest/v1/profiles?id=eq.{user_id}", {"balance": "500.00"}),
    ("PATCH pending_balance", "PATCH", f"/rest/v1/profiles?id=eq.{user_id}", {"pending_balance": 500.00}),
    ("PUT balance", "PUT", f"/rest/v1/profiles?id=eq.{user_id}", {"balance": 500.00}),
    ("PATCH lifetime_earned", "PATCH", f"/rest/v1/profiles?id=eq.{user_id}", {"lifetime_earned": 500.00}),
    ("POST insert wallet_transaction", "POST", "/rest/v1/wallet_transactions", {
        "user_id": user_id, "amount": 500.00, "type": "topup", "status": "completed", "description": "Test topup"
    }),
    ("PATCH via RPC function", "POST", "/rest/v1/rpc/add_balance", {"amount": 500.00}),
]

for name, method, path, data in methods:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        body_data = json.dumps(data)
        conn.request(method, path, body=body_data, headers=headers)
        r = conn.getresponse()
        body = r.read().decode()
        print(f"\n{name}: {r.status}")
        print(f"  Response: {body[:200]}")
        conn.close()
    except Exception as e:
        print(f"\n{name}: Error - {str(e)[:100]}")
