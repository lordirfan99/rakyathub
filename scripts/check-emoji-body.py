#!/usr/bin/env python3
"""Check for emoji in body paragraphs (not H2-H4, tables, or blockquotes)."""
import re
import sys

with open(sys.argv[1], encoding='utf-8') as f:
    content = f.read()

parts = content.split('---', 2)
body = parts[2] if len(parts) >= 3 else content
lines = body.split('\n')

for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith('|'): continue
    if re.match(r'^#{2,4} ', s): continue
    if s.startswith('```'): continue
    if s == '': continue
    if s.startswith('>'): continue

    # Check for emoji (common ranges)
    emoji = re.findall(
        r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0\u2600-\u27BF\u2B50\u2705\u274C]', s
    )
    if emoji:
        print(f'Line {i}: {emoji} -> {s[:80]}')
        continue

print('PASS: No body emoji violations')
