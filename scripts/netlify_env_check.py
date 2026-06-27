import json, urllib.request, os

token = ""
with open(os.path.expanduser("~/AppData/Local/hermes/.env")) as f:
    for line in f:
        line = line.strip()
        if "NETLIFY_AUTH_TOKEN" in line:
            parts = line.split("=", 1)
            if len(parts) > 1:
                token = parts[1].strip()
            break

api_key = ""
with open(os.path.expanduser("~/rakyathub/.env")) as f:
    for line in f:
        line = line.strip()
        if "ELECTION_API_KEY" in line:
            parts = line.split("=", 1)
            if len(parts) > 1:
                api_key = parts[1].strip()
            break

print(f"Token: {len(token)} chars, API key: {len(api_key)} chars")

headers = {"Authorization": f"Bearer {token}"}
site_id = "6a5f68a4-d25a-4c02-880a-77a154e73472"

def api(method, path, data=None):
    url = f"https://api.netlify.com/api/v1{path}"
    req = urllib.request.Request(url, headers=headers, method=method)
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"  {method} {path} -> {e.code}: {body}")
        return None
    except Exception as e:
        print(f"  {method} {path} -> {e}")
        return None

# Try POST with different formats
print("\n1. POST /sites/{id}/env (simple)")
r = api("POST", f"/sites/{site_id}/env", {
    "key": "ELECTION_API_KEY",
    "values": [{"context": "all", "value": api_key}]
})

# Try with site_id as query param
print("\n2. POST /sites/{id}/env?site_id=...")
r2 = api("POST", f"/sites/{site_id}/env?site_id={site_id}", {
    "key": "ELECTION_API_KEY",
    "values": [{"context": "all", "value": api_key}]
})

# List accounts
print("\n3. GET /accounts")
accts = api("GET", "/accounts")
if accts and isinstance(accts, list):
    for a in accts:
        aid = a.get("slug") or a.get("id", "")
        print(f"  Account: {a.get('name')} slug={a.get('slug')} id={a.get('id')}")
else:
    print(f"  Response type: {type(accts).__name__} = {str(accts)[:200]}")

# Try build hooks endpoint  
print("\n4. GET /hooks")
hooks = api("GET", "/hooks")
if hooks and isinstance(hooks, list):
    for h in hooks:
        print(f"  Hook: {h.get('title')} site_id={h.get('site_id')}")
else:
    print(f"  Response: {str(hooks)[:200]}")

# Check if there's a deploy context setting
print("\n5. GET /sites/{id} build_settings")
site = api("GET", f"/sites/{site_id}")
if site:
    bs = site.get("build_settings", {})
    print(f"  Repo: {bs.get('repo_url', '-')}")
    print(f"  Cmd: {bs.get('cmd', '-')}")
    print(f"  Dir: {bs.get('dir', '-')}")
    env_in_bs = bs.get("env", {})
    print(f"  Env keys: {list(env_in_bs.keys()) if env_in_bs else 'none'}")
