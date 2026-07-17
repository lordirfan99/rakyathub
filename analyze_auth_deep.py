#!/usr/bin/env python3
"""Extract registration form handler from auth JS."""
import urllib.request, re

url = "https://taskkita.com/assets/auth-Cz2Xkjtl.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode(errors="replace")

# Find the submit handler for registration (search around "signup")
idx = data.find("signup")
if idx >= 0:
    # Find the form submit function
    # Search backwards for "onSubmit" and the function
    section = data[max(0,idx-500):idx+2000]
    
    # Print readable version - extract function calls
    # Look for the server function call
    print("=== SECTION AROUND signup ===")
    print(section[:1500])
    print("\n...")
    
# Also find the server function import
print("\n=== SERVER FUNCTION IMPORTS ===")
for m in re.finditer(r'import\s*\{[^}]+\}\s*from\s*["\'](?:\.\.?/)*(?:server|api|lib)[^"\']*["\']', data):
    print(f"  {m.group()[:200]}")

# Find formAction calls
print("\n=== formAction patterns ===")
for m in re.finditer(r'formAction\s*\(?\s*\{', data):
    start = max(0, m.start()-50)
    end = min(len(data), m.end()+500)
    print(f"  Context: ...{data[start:end]}...")
    print()
