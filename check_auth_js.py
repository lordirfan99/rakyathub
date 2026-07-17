#!/usr/bin/env python3
"""Extract routes and server function calls from JS."""
import urllib.request, re, json

js_files = [
    "auth-Cz2Xkjtl.js",
    "index-CdJ2nOzM.js",
]

for js in js_files:
    url = f"https://taskkita.com/assets/{js}"
    print(f"\n=== {js} ===")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        data = resp.read().decode(errors="replace")
        
        # Find all quote-enclosed paths
        routes = re.findall(r"[\"'](/[a-zA-Z0-9_/.~-]+)[\"']", data)
        for r in sorted(set(routes)):
            if any(x in r for x in ["api", "auth", "register", "login", "user",
                                     "campaign", "wallet", "withdraw", "order",
                                     "server", "action", "fn", "submit"]):
                print(f"  {r}")
        
        # Find server function definitions
        sfn = re.findall(r'["\']([a-zA-Z]+(?:Fn|Action|Handler|Submit))["\']', data)
        for s in sorted(set(sfn)):
            print(f"  FN: {s}")
            
    except Exception as e:
        print(f"  Error: {e}")
