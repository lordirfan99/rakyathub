#!/usr/bin/env python3
"""Extract full Supabase anon key and register."""
import urllib.request, re, json

# Get the full Supabase key from the JS
url = "https://taskkita.com/assets/index-CdJ2nOzM.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")

# Find the anon key - it's a JWT (eyJ...)
# Find it near the supabase URL
supabase_url = "https://xvdibouzxfynsxgrmffb.supabase.co"

# Find the createClient call with both URL and key
idx = data.find(supabase_url)
if idx >= 0:
    # Get surrounding context
    context = data[max(0,idx-200):idx+500]
    # Find the key - it's a string passed as second arg to createClient
    # Look for the anon key pattern eyJ...
    keys = re.findall(r'["\'](eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+)["\']', data)
    print(f"Supabase URL: {supabase_url}")
    print(f"Found {len(keys)} potential keys")
    for k in keys:
        print(f"  Key: {k[:50]}...{k[-20:]}")
    
    # Try to register using the first key
    SUPABASE_URL = supabase_url
    SUPABASE_KEY = keys[0] if keys else ""
    
    if SUPABASE_KEY:
        print(f"\n=== TRYING REGISTRATION ===")
        EMAIL = "taskkita.test.7788@web-library.net"
        PASSWORD = "TestPass789!"
        
        # Register via Supabase REST API
        import http.client
        import ssl
        
        conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
        payload = json.dumps({
            "email": EMAIL,
            "password": PASSWORD,
            "data": {"username": "taskkita_test"}
        })
        headers = {
            "Content-Type": "application/json",
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        conn.request("POST", "/auth/v1/signup", body=payload, headers=headers)
        resp = conn.getresponse()
        body = resp.read().decode()
        print(f"Status: {resp.status}")
        print(f"Response: {body[:500]}")
        conn.close()
        
        if resp.status == 200:
            # Save session for later
            data = json.loads(body)
            print(f"\n✅ REGISTERED!")
            print(f"User ID: {data.get('user', {}).get('id', 'N/A')}")
            print(f"Email: {data.get('user', {}).get('email', 'N/A')}")
            if 'access_token' in data:
                print(f"Access Token: {data['access_token'][:50]}...")
            if 'refresh_token' in data:
                print(f"Refresh Token: {data['refresh_token'][:30]}...")
