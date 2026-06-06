#!/usr/bin/env python3
"""Extract application details from job email messages."""
import re

with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_00_vVQRIlNfg15u2FIHSaoY8156.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Extract all emails with their subjects and message texts
# Each email block is like: {"attachmentList":[],"labelIds":[...],"messageId":"...","messageText":"...","subject":"..."}
# Find blocks for "Your application was successfully submitted" 

# Parse the jobStreet messages - split on individual message blocks
# The text contains JSON with escaped quotes. Let's find messageText content
# for the relevant submission emails.

# Find all messageText values that contain application info
blocks = re.findall(r'"messageText":"(.*?)"', text)

print(f"Found {len(blocks)} messageText blocks total")

# Look for submission emails - they mention "your application for [POSITION] was successfully submitted to [COMPANY]"
submission_details = []
for i, block in enumerate(blocks):
    # Check if this is a submission email
    if 'your application for' in block.lower() and 'was successfully submitted' in block.lower():
        # Extract position and company
        m = re.search(r'your application for\s+(.+?)\s+was successfully submitted\s+to\s+(.+?)(?:\.|\\n|\\r)', block, re.IGNORECASE)
        if m:
            position = m.group(1).strip()
            company = m.group(2).strip()
            submission_details.append((company, position))
            print(f"  Submission: {position} @ {company}")

# Also look for "Application submitted - verify key information"
print("\n--- Application submitted (verify key info) ---")
for block in blocks:
    if 'verify key information' in block.lower():
        # These emails have different format
        m = re.search(r'You applied for\s+(.+?)\s+at\s+(.+?)(?:\.|\\n|\\r)', block, re.IGNORECASE)
        if m:
            position = m.group(1).strip()
            company = m.group(2).strip()
            print(f"  {position} @ {company}")
        else:
            # Show first 200 chars
            print(f"  (No match, preview): {block[:200]}")

print(f"\nTotal new submissions found: {len(submission_details)}")

# Extract unique pairs
for company, position in submission_details:
    print(f"  📌 {position} @ {company}")
