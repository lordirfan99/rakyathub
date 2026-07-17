import requests, re, json

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

# 1. Extract BCL payment embed JS
print('=== BCL Payment Embed JS ===')
r = s.get('https://bcl.my/js/bc-encrypted-payment-embed.js', timeout=15)
js = r.text
print(f'Size: {len(js)} bytes')
print(js[:3000])

# 2. Extract ALL tracking/pixel IDs
print('\n=== PIXEL/TRACKING IDs ===')
for pattern in [r'facebook[^}]+}', r'tiktok[^}]+}', r'google[^}]+}', r'pixel[^}]+}', r'merchant[^}]+}']:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for m in matches[:5]:
        print(f'  {m[:200]}')

# 3. Check what API endpoints the JS calls
print('\n=== API Endpoints in JS ===')
urls = re.findall(r'https?://[^"\'\\\\;)\s,<>\]]+', js)
for u in set(urls):
    print(f'  {u}')

# 4. Extract iframe URL pattern
iframe_url = re.search(r'data-url[^"]*"([^"]+)"', js)
print(f'\nIframe URL pattern: {iframe_url.group(1) if iframe_url else "N/A"}')

# 5. Try to access the iframe URL directly
api_pattern = re.search(r'https?://[^"\'\\\\;]+api[^"\'\\\\;]+', js)
print(f'API URL: {api_pattern.group(0) if api_pattern else "N/A"}')
