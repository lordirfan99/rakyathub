#!/usr/bin/env python3
"""Fetch 7-day GSC data: totals (summed) + top pages."""
import json
import urllib.request
import sys

TOKEN = "b1e7edf54fbb44107eb5ff5aac0d1fed0132bf755acada2c"
URL = "https://www.advancedgsc.com/api/mcp"

def call_mcp(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(URL, data=payload, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    })
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())

# 1) Fetch many queries to sum totals
print("=== QUERY DATA (7 DAYS) ===", file=sys.stderr)
q_raw = call_mcp("tools/call", {
    "name": "get_search_analytics",
    "arguments": {
        "site_url": "sc-domain:rakyathub.my",
        "days": 7,
        "dimensions": "query",
        "row_limit": 500
    }
})
q_text = q_raw['result']['content'][0]['text']
q_lines = q_text.strip().split('\n')
q_rows = q_lines[4:]  # skip headers
print(f"Got {len(q_rows)} query rows", file=sys.stderr)

total_clicks = 0
total_impressions = 0
weighted_position_sum = 0.0

for line in q_rows:
    if not line.strip():
        continue
    # Format: Query | Clicks | Impressions | CTR | Position
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 5:
        try:
            clicks = int(parts[1])
            impressions = int(parts[2])
            position = float(parts[4])
            total_clicks += clicks
            total_impressions += impressions
            weighted_position_sum += position * clicks
        except ValueError:
            continue

avg_position = round(weighted_position_sum / total_clicks, 1) if total_clicks > 0 else 0
ctr_val = round((total_clicks / total_impressions * 100), 2) if total_impressions > 0 else 0

totals = {
    "clicks": total_clicks,
    "impressions": total_impressions,
    "ctr": f"{ctr_val}%",
    "position": avg_position,
    "period": "2026-06-30 to 2026-07-07"
}
print(f"TOTALS: {json.dumps(totals)}", file=sys.stderr)

# 2) Fetch top pages by clicks
print("=== PAGE DATA (7 DAYS) ===", file=sys.stderr)
p_raw = call_mcp("tools/call", {
    "name": "get_search_analytics",
    "arguments": {
        "site_url": "sc-domain:rakyathub.my",
        "days": 7,
        "dimensions": "page",
        "row_limit": 10
    }
})
p_text = p_raw['result']['content'][0]['text']
p_lines = p_text.strip().split('\n')
p_rows = p_lines[4:] if len(p_lines) > 4 else []
print(f"Got {len(p_rows)} page rows", file=sys.stderr)
print(f"Raw rows: {p_rows}", file=sys.stderr)

parsed_pages = []
for line in p_rows:
    if not line.strip():
        continue
    # Format: Page | Clicks | Impressions | CTR | Position
    parts = [p.strip() for p in line.split('|')]
    print(f"Parts: {parts} (len={len(parts)})", file=sys.stderr)
    if len(parts) >= 5:
        try:
            parsed_pages.append({
                "page": parts[0],
                "clicks": int(parts[1]),
                "impressions": int(parts[2]),
                "ctr": parts[3],
                "position": float(parts[4])
            })
        except (ValueError, IndexError) as e:
            print(f"Parse error: {e} for line: {line}", file=sys.stderr)
            continue

print(f"TOP PAGES: {json.dumps(parsed_pages)}", file=sys.stderr)

# Output JSON to stdout
output = {"totals": totals, "top_pages": parsed_pages}
print(json.dumps(output))
