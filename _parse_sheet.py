#!/usr/bin/env python3
import json

# Read the file
with open(r'C:\Users\irfan\AppData\Local\hermes\cache\terminal\hermes-results\call_00_0ELB7t6YERhNDfejcZg11295.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Extract the JSON string from the wrapper
prefix = '{"result": "'
suffix = '"}'
if raw.startswith(prefix) and raw.endswith(suffix):
    inner = raw[len(prefix):-len(suffix)]
    # Unescape
    inner = inner.replace('\\"', '"').replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
    inner = inner.replace('\\\\', '\\')
    parsed = json.loads(inner)
    data = parsed['result']['content'][0]['text']
    sheet_data = json.loads(data)
    rows = sheet_data['valueRanges'][0]['values']
    
    header = rows[0]
    print(f'Headers: {header}')
    print(f'Total data rows: {len(rows) - 1}')
    print()
    
    # List entries
    for i, row in enumerate(rows[1:], 1):
        num = row[0].strip() if len(row) > 0 else str(i)
        company = row[3].strip() if len(row) > 3 else ''
        position = row[4].strip() if len(row) > 4 else ''
        stage = row[10].strip() if len(row) > 10 else ''
        date = row[1].strip() if len(row) > 1 else ''
        platform = row[2].strip() if len(row) > 2 else ''
        updated = row[11].strip() if len(row) > 11 else ''
        print(f'{num:>3} | {date} | {platform:<12} | {company:<35} | {position:<45} | {stage:<15} | {updated}')
