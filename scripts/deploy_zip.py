import os, json, urllib.request, zipfile, io, time

# Get token
token = os.environ.get('NETLIFY_AUTH_TOKEN', '')
with open(os.path.expanduser('~/AppData/Local/hermes/.env')) as f:
    for line in f:
        if line.startswith('NETLIFY_AUTH_TOKEN='):
            token = line.strip().split('=', 1)[1]
            break

print(f'Token length: {len(token)}')
site_id = '6a5f68a4-d25a-4c02-880a-77a154e73472'
dist_path = os.path.expanduser('~/rakyathub/dist')

print('Zipping...')
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, filenames in os.walk(dist_path):
        for fn in filenames:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, dist_path).replace(os.sep, '/')
            zf.write(full, rel)

data = zip_buffer.getvalue()
print(f'Zipped {len(data)/1024:.0f} KB')

url = f'https://api.netlify.com/api/v1/sites/{site_id}/deploys'
req = urllib.request.Request(url, headers={
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/zip'
}, data=data, method='POST')

with urllib.request.urlopen(req, timeout=300) as resp:
    deploy = json.loads(resp.read().decode())

did = deploy['id']
print(f'Deploy ID: {did}')

for i in range(30):
    time.sleep(3)
    d_req = urllib.request.Request(
        f'https://api.netlify.com/api/v1/sites/{site_id}/deploys/{did}',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(d_req, timeout=30) as d_resp:
        d = json.loads(d_resp.read().decode())
        if d['state'] == 'ready':
            r_req = urllib.request.Request(
                f'https://api.netlify.com/api/v1/sites/{site_id}/deploys/{did}/restore',
                headers={'Authorization': f'Bearer {token}'},
                method='POST'
            )
            with urllib.request.urlopen(r_req, timeout=60) as r_resp:
                r = json.loads(r_resp.read().decode())
                print(f'✅ Published at {r.get("published_at", "N/A")}')
            break
    if i == 29:
        print('⚠️ Timed out waiting for ready')
