#!/usr/bin/env python3
"""Analyze admin JS for server function details."""
import urllib.request, re

url = "https://taskkita.com/assets/admin-BBGPv-GW.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")

# Search for admin-related server fn calls
print("=== ADMIN PASSWORD CHECK ===")
for m in re.finditer(r'ADMIN_PASSWORD|admin.?password|check_admin|verify_admin|adminLogin|admin_login', data, re.IGNORECASE):
    start = max(0, m.start()-150)
    end = min(len(data), m.end()+300)
    print(f"\n  Context: {data[start:end]}")
    print()

print("\n=== SERVER FN CALLS ===")
# Find server function handler patterns
for m in re.finditer(r'handler\(\s*["\x27]([^"\x27]+)["\x27]', data):
    print(f"  Handler: {m.group(1)}")

print("\n=== API ROUTES ===")
routes = re.findall(r'["\x27](/[a-zA-Z0-9_/-]+)["\x27]', data)
for r in sorted(set(routes)):
    if any(x in r for x in ["admin", "api", "fn", "server"]):
        print(f"  {r}")
