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
        return None
    except Exception as e:
        return None

account_slug = "azwariirfan"
site_id = "6a5f68a4-d25a-4c02-880a-77a154e73472"

# Try account-level env endpoint
print(f"\n1. POST /accounts/{account_slug}/env")
r = api("POST", f"/accounts/{account_slug}/env", {
    "key": "ELECTION_API_KEY",
    "values": [{"context": "all", "value": api_key}],
    "secret": False
})

# Try site env with different context format
print(f"\n2. POST /sites/{site_id}/env")
r2 = api("POST", f"/sites/{site_id}/env", {
    "key": "ELECTION_API_KEY",
    "values": [{"context": "dev", "value": api_key}]
})

# Try with secret
print(f"\n3. POST /sites/{site_id}/env (secret)")
r3 = api("POST", f"/sites/{site_id}/env", {
    "key": "ELECTION_API_KEY",
    "values": [{"context": "all", "value": api_key}],
    "secret": True
})

# If nothing works, use the builds API to set env via deploy settings
print(f"\n4. PATCH /sites/{site_id}")
site = api("GET", f"/sites/{site_id}")
if site:
    # Check existing processing settings or build settings 
    bs = site.get("build_settings", {})
    env = bs.get("env", {})
    env["ELECTION_API_KEY"] = api_key
    r4 = api("PATCH", f"/sites/{site_id}", {
        "build_settings": {
            "env": env
        }
    })
    if r4:
        print("  Updated build_settings.env!")
    else:
        print("  Could not update build_settings.env")

print("\n--- Summary ---")
print("If none of the above worked, set the env var manually at:")
print("https://app.netlify.com/sites/rakyathub/settings/env#vars")
