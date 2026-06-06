#!/usr/bin/env python3
"""Parse job tracker email results and report new activity."""
import re
import sys

with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_00_vVQRIlNfg15u2FIHSaoY8156.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Find the jobStreet messages section
# Look for pattern: "messages": [{...}]
# The text is heavily escaped. Let me find messageText blocks more simply.

# Find all messageId to subject mappings
# Subjects appear as: "subject": "Your application was..."
subjects = re.findall(r'"subject":\s*"([^"]+)"', text)

# Find unique subject lines (deduplicate since they appear twice each)
seen = set()
unique_subjects = []
for s in subjects:
    if s not in seen:
        seen.add(s)
        unique_subjects.append(s)

print("=== UNIQUE SUBJECTS ===")
for s in unique_subjects:
    print(f"  - {s}")

# Find application-related subjects
app_subjects = [s for s in unique_subjects if any(k in s.lower() for k in [
    'application was successfully submitted',
    'application submitted',
    'application update',
    'temu duga',
    'new activity',
    'application unsuccessful',
    'not shortlisted',
    'rejected'
])]

print(f"\n=== RELEVANT APPLICATION SUBJECTS ({len(app_subjects)}) ===")
for s in app_subjects:
    print(f"  - {s}")

# Count how many times each relevant subject appears
count_map = {}
for s in subjects:
    if any(k in s.lower() for k in [
        'application was successfully submitted',
        'application submitted',
        'application update',
        'temu duga',
        'new activity',
    ]):
        count_map[s] = count_map.get(s, 0) + 1

print(f"\n=== COUNTS ===")
for s, c in count_map.items():
    print(f"  [{c}] {s}")
