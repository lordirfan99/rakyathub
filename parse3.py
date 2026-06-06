#!/usr/bin/env python3
"""Parse job email texts to find new applications and updates."""
import re

with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_00_vVQRIlNfg15u2FIHSaoY8156.txt', 'r', encoding='utf-8', errors='replace') as f:
    raw = f.read()

# The data has double-escaped JSON. 
# I notice the file has raw text readable after unescaping.
# Let me find ALL occurrences of "your application for" and extract context

# First, unescape one level: replace \\\\ with \\ and \\" with " etc
# Actually, let me just search for patterns in the raw text

# Extract submission emails (application successfully submitted)
print("=== NEW APPLICATION SUBMISSIONS ===")
# Find position+company pairs in submission emails
matches = re.finditer(r'your application for\s+(.+?)\s+was successfully submitted\s+to\s+(.+?)[\\.\n\r]', raw, re.IGNORECASE)
seen = set()
for m in matches:
    position = m.group(1).strip()
    company = m.group(2).strip()
    # Clean up escaped chars
    position = position.replace('\\r', '').replace('\\n', '').strip()
    company = company.replace('\\r', '').replace('\\n', '').strip()
    key = f"{company}|{position}"
    if key not in seen:
        seen.add(key)
        print(f"  📌 {position} @ {company}")

# Extract activity emails
print("\n=== ACTIVITY UPDATES ===")
for m in re.finditer(r'new activity in jobs you applied for(.+?)(?=jobstreet)', raw, re.IGNORECASE | re.DOTALL):
    chunk = m.group(1)[:2000]
    # Find specific updates
    updates = re.findall(r'Your application for\s+(.+?)\s+(has|was)\s+(.+?)(?:\.|\\n)', chunk, re.IGNORECASE)
    for pos, _, status in updates:
        pos = pos.replace('\\r', '').replace('\\n', '').strip()
        status = status.replace('\\r', '').replace('\\n', '').strip()
        print(f"  Status: {pos} -> {status}")
    if not updates:
        print(f"  (Preview): {chunk[:500]}")

# Look for "Application submitted - verify key information" content
print("\n=== APPLICATION SUBMITTED (VERIFY KEY INFO) ===")
for m in re.finditer(r'verify key information(.+?)(?=\\\\n\\\\n|jobstreet)', raw, re.IGNORECASE | re.DOTALL):
    chunk = m.group(0)[:1000]
    # Extract position and company
    m2 = re.search(r'you applied for\s+(.+?)\s+at\s+(.+?)(?:\.|\\n)', chunk, re.IGNORECASE)
    if m2:
        pos = m2.group(1).strip().replace('\\r', '').replace('\\n', '')
        company = m2.group(2).strip().replace('\\r', '').replace('\\n', '')
        print(f"  {pos} @ {company}")
    else:
        print(f"  (Preview): {chunk[:300]}")

# Extract MYFutureJobs Temu Duga details  
print("\n=== TEMU DUGA / INTERVIEW INVITES ===")
for m in re.finditer(r'Temu Duga MYFutureJobs(.+?)(?:\\\\n|$)', raw, re.IGNORECASE):
    chunk = m.group(0).replace('\\r', '').replace('\\n', ' ').strip()
    print(f"  {chunk[:200]}")

# Also check "Jom sertai Temu Duga Terbuka"
for m in re.finditer(r'Temu Duga Terbuka(.+?)(?:\\\\n|$)', raw, re.IGNORECASE):
    chunk = m.group(0).replace('\\r', '').replace('\\n', ' ').strip()
    print(f"  {chunk[:200]}")
