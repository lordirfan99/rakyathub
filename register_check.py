import re, json, requests, random, string

# Read the register page
with open('/tmp/cali_register.html', 'r') as f:
    h = f.read()

# Extract the Livewire snapshot data
parts = h.split('wire:snapshot="')
for p in parts[1:]:
    end = p.find('"')
    if end > 0:
        raw = p[:end]
        decoded = raw.replace('&quot;', '"').replace('&amp;', '&')
        try:
            data = json.loads(decoded)
            name = data.get('memo', {}).get('name', '')
            if 'Register' in name or 'register' in name.lower():
                print('Register component snapshot:')
                print(json.dumps(data, indent=2)[:3000])
                print()
                
                # Extract the form fields from the snapshot
                form_data = data.get('data', {})
                print('Form data keys:')
                for key in form_data.keys():
                    print(f'  {key}')
        except:
            pass

# CSRF
csrf = re.search(r'csrf-token" content="([^"]+)"', h)
print(f'\nCSRF Token: {csrf.group(1) if csrf else "N/A"}')

# Now try to register
s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

# Get fresh CSRF from register page
r = s.get('https://caliphempire.bcl.my/register', timeout=15)
csrf_m = re.search(r'csrf-token" content="([^"]+)"', r.text)
if csrf_m:
    print(f'Fresh CSRF: {csrf_m.group(1)[:30]}...')
    
    # Try to register via POST
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    email = f'hacker{suffix}@web-library.net'
    
    r2 = s.post('https://caliphempire.bcl.my/register',
        data={
            '_token': csrf_m.group(1),
            'email': email,
            'password': 'TestPass789!',
            'password_confirmation': 'TestPass789!',
        },
        allow_redirects=False,
        timeout=15
    )
    print(f'Register POST: {r2.status_code} -> {r2.headers.get("Location", "-")}')
    
    if r2.status_code == 302:
        r3 = s.get(r2.headers['Location'], timeout=15)
        print(f'Followed: {r3.status_code} -> {r3.url}')
        print(f'Content: {r3.text[:500]}')
    else:
        print(f'Response: {r2.text[:500]}')
    
    print(f'\nTested email: {email}')
