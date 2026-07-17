import re, json, requests

# Read the HTML file
with open('/tmp/cali_page.html', 'r') as f:
    html = f.read()

# Find all wire:snapshot data (these are JSON-encoded in HTML attributes)
snapshots = re.findall(r'wire:snapshot="{([^"]+)}"', html)
print(f'Found {len(snapshots)} Livewire snapshots')

for i, snap in enumerate(snapshots):
    try:
        # Unescape HTML entities
        decoded = snap.replace('&quot;', '"').replace('&amp;', '&')
        data = json.loads(decoded)
        print(f'\n{"="*60}')
        print(f'Snapshot {i}: {data.get("memo",{}).get("name","unknown")}')
        print(f'{"="*60}')
        
        # Extract data field
        d = data.get('data', {})
        if isinstance(d, dict):
            # Print all keys (but truncate long values)
            for key, val in list(d.items())[:20]:
                val_str = json.dumps(val, indent=2)[:500]
                print(f'  {key}: {val_str}')
            
            # Specifically look for affiliate info
            aff = d.get('affiliateInfo', None)
            if aff:
                print(f'\n  *** AFFILIATE INFO ***')
                print(f'  {json.dumps(aff, indent=2)[:1000]}')
            
            # Look for pricing
            prices = d.get('discountedPrices', None)
            if prices:
                print(f'\n  *** PRICING ***')
                print(f'  {json.dumps(prices, indent=2)[:500]}')
                
    except Exception as e:
        print(f'Parse error in snapshot {i}: {e}')

# Find admin/filament routes
print(f'\n{"="*60}')
print('POTENTIAL ADMIN ROUTES')
print(f'{"="*60}')
# Look for Filament-related paths
paths = re.findall(r'(?:href|src|action)="([^"]*(?:admin|filament|login|dashboard|app)[^"]*)"', html, re.I)
for p in set(paths):
    print(f'  {p}')

# Check for any API endpoints
print(f'\n{"="*60}')
print('CSRF & META')
print(f'{"="*60}')
csrf = re.search(r'csrf-token" content="([^"]+)"', html)
print(f'CSRF: {csrf.group(1) if csrf else "N/A"}')
