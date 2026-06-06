#!/usr/bin/env python3
"""Parse deeply nested/escaped JSON output from Gmail API."""
import json
import re

with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_00_vVQRIlNfg15u2FIHSaoY8156.txt', 'r', encoding='utf-8', errors='replace') as f:
    raw = f.read()

# Extract jobStreet emails: find the escaped JSON array of messages
# Looking for: \\\"messages\\\":[{\\\\\\\"attachmentList...
m = re.search(r'\\\\"messages\\\\"\s*:\s*\[(.+?)\]', raw)
if not m:
    print("Could not find messages array")
    # Try different escaping depth
    m = re.search(r'\"messages\"\s*:\s*\[(.+?)\]', raw)
if m:
    print(f"Found messages array, first 500 chars: {m.group(0)[:500]}")
else:
    print("Still couldn't find it. Let me look for messageId in the raw text")
    ids = re.findall(r'messageId[^:]*:[^"]*"([^"]+)"', raw)
    print(f"Found {len(ids)} message IDs")
    for i in ids:
        print(f"  {i}")

# Let me just look for all messageId: values at any escaping depth
print("\n=== Quick scan for all content ===")
# Find application submission phrases
for phrase in ['your application for', 'IT Support', 'IT Executive', 'SIMPLIFIED', 'CSS Decisions', 'MIS EXECUTIVE']:
    positions = [m.start() for m in re.finditer(re.escape(phrase), raw, re.IGNORECASE)]
    if positions:
        # Show context around first occurrence
        pos = positions[0]
        context = raw[max(0,pos-100):pos+200]
        print(f"\n'{phrase}' found at offset {pos}:")
        # Unescape for display
        context = context.replace('\\\\\\', '\\').replace('\\\\', '\\').replace('\\r', '\r').replace('\\n', '\n')
        print(context[:500])
