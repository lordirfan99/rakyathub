#!/usr/bin/env python3
"""Extract API endpoints from JS bundles."""
import sys, re, urllib.request

js_files = [
    "admin.functions-B4AYdLqc.js",
    "index-CdJ2nOzM.js",
    "index-CQcW8Nq3.js",
]

for js in js_files:
    url = f"https://taskkita.com/assets/{js}"
    print(f"\n=== {js} ===")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        data = resp.read().decode(errors="replace")
        
        # Find API routes
        routes = re.findall(r'["\'](/\w[\w/-]*\w)["\']', data)
        for r in sorted(set(routes)):
            if any(x in r for x in ["api", "auth", "admin", "login", "register", 
                                     "campaign", "wallet", "withdraw", "user", 
                                     "order", "payment", "service", "task"]):
                print(f"  {r}")
        
        # Find fetch/axios calls
        fetches = re.findall(r'fetch\(["\']([^"\']+)["\']', data)
        for f in sorted(set(fetches)):
            if not f.startswith("http"):
                print(f"  FETCH: {f}")
                
    except Exception as e:
        print(f"  Error: {e}")
