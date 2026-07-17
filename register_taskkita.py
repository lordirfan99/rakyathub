#!/usr/bin/env python3
"""Register on TaskKita and explore dashboard."""
import urllib.request, json, re, sys

BASE = "https://taskkita.com"
EMAIL = "taskkita.test.7788@web-library.net"
USERNAME = "taskkita_test"
PASSWORD = "TestPass789!"

# Create a session
import http.cookiejar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [
    ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"),
    ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
]

# 1. Get the auth page first
print("=== 1. GET AUTH PAGE ===")
req = urllib.request.Request(f"{BASE}/auth")
resp = opener.open(req, timeout=15)
cookies = list(cj)
for c in cookies:
    print(f"  Cookie: {c.name}={c.value}")

# 2. Try to register - find the API endpoint from the page
html = resp.read().decode("utf-8", errors="replace")

# Look for action patterns in HTML
actions = re.findall(r'action=[\"\']([^\"\']+)', html)
print(f"\n  Actions found: {actions}")

# Look for fetch/server function patterns
fns = re.findall(r'["\'](/~?\w[\w/.-]*)["\']', html)
unique = sorted(set(fns))
print(f"\n  Routes found in page:")
for u in unique:
    if any(x in u for x in ["api", "auth", "register", "login", "user", "sign"]):
        print(f"    {u}")

# 3. Try various registration endpoints
endpoints_to_try = [
    f"{BASE}/~api/auth/register",
    f"{BASE}/api/auth/register",
    f"{BASE}/auth/register",
    f"{BASE}/api/register",
    f"{BASE}/register",
]

for ep in endpoints_to_try:
    try:
        data = json.dumps({
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "confirmPassword": PASSWORD,
        }).encode()
        req = urllib.request.Request(ep, data=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST")
        resp = opener.open(req, timeout=15)
        body = resp.read().decode()
        print(f"\n  [{resp.status}] {ep}: {body[:200]}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"\n  [{e.code}] {ep}: {body}")
    except Exception as e:
        print(f"\n  [ERR] {ep}: {e}")
