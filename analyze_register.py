#!/usr/bin/env python3
"""Analyze auth JS for registration function format."""
import urllib.request, re

url = "https://taskkita.com/assets/auth-Cz2Xkjtl.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")

# Find register-related code sections
# Look for the server function call pattern
patterns = {
    "register": r"register\w*",
    "createServerFn": r'create\w*Server\w*Fn\s*\(',
    "useServerFn": r'use\w*Server\w*Fn\s*\(',
    "serverFn": r'server\w*Fn\s*\(',
    "formAction": r'form\w*Action',
    "submit": r'submit\w*Handler|onSubmit|handleSubmit',
    "fetch register": r'fetch\s*\(\s*["\'][^"\']*register',
}

for name, pattern in patterns.items():
    matches = list(re.finditer(pattern, data, re.IGNORECASE))
    if matches:
        print(f"\n=== {name} ({len(matches)} matches) ===")
        for m in matches[:3]:
            start = max(0, m.start() - 100)
            end = min(len(data), m.end() + 200)
            context = data[start:end]
            print(f"  ...{context}...")
            print()
