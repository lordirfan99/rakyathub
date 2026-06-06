#!/usr/bin/env python3
"""Extract distinct job applications from the email data."""
import re

with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_00_dSfd0T08J5ekGZdGNXs11812.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Find all submission messages
matches = re.findall(r'your application for (.+?) was successfully submitted to (.+?)(?:\.|\n)', text, re.IGNORECASE)
print(f'Total matches: {len(matches)}')
seen = set()
for pos, comp in matches:
    pos = pos.replace('\\r', '').replace('\\n', '').strip()
    comp = comp.replace('\\r', '').replace('\\n', '').strip()
    # Clean escaped backslashes
    pos = pos.replace('\\\\', '')
    comp = comp.replace('\\\\', '')
    key = f'{pos} @ {comp}'
    if key not in seen:
        seen.add(key)
        print(f'  {key}')

# Also check the verify key info file
print('\n--- From verify key info file ---')
with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_01_WTGAEDNhDMRRABsCS26i6705.txt', 'r', encoding='utf-8', errors='replace') as f:
    text2 = f.read()
matches2 = re.findall(r'your application for (.+?) was successfully submitted to (.+?)(?:\.|\n)', text2, re.IGNORECASE)
for pos, comp in matches2:
    pos = pos.replace('\\r', '').replace('\\n', '').strip()
    comp = comp.replace('\\r', '').replace('\\n', '').strip()
    pos = pos.replace('\\\\', '')
    comp = comp.replace('\\\\', '')
    print(f'  {pos} @ {comp}')
