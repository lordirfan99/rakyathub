#!/usr/bin/env python3
"""Extract Supabase config from JS bundles."""
import urllib.request, re

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
        
        # Find supabase URL/key patterns
        supabase_patterns = [
            r'supabase[^"\']*url[^"\']*["\'][^"\']+',
            r'supabase[^"\']*key[^"\']*["\'][^"\']+',
            r'supabase[.]co["\']',
            r'https://[a-z0-9-]+[.]supabase[.]co',
            r'eyJ[a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+[.][a-zA-Z0-9_-]+',  # JWT (anon key)
        ]
        
        for pattern in supabase_patterns:
            matches = re.findall(pattern, data, re.IGNORECASE)
            for m in matches[:3]:
                print(f"  [{pattern[:30]}]: {m[:150]}")
        
        # Find createClient calls
        for m in re.finditer(r'createClient\s*\(', data):
            start = max(0, m.start()-20)
            end = min(len(data), m.end()+200)
            context = data[start:end]
            # Clean up
            clean = re.sub(r'\s+', ' ', context)
            print(f"  [createClient]: {clean[:200]}")
        
    except Exception as e:
        print(f"  Error: {e}")
