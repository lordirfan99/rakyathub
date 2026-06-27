import json, urllib.request, os

token = ""
with open(os.path.expanduser("~/AppData/Local/hermes/.env")) as f:
    for line in f:
        line = line.strip()
        if "NETLIFY_AUTH_TOKEN=" in line:
            parts = line.split("=", 1)
            if len(parts) > 1:
                token = parts[1]
            break

api_key = ""
with open(os.path.expanduser("~/rakyathub/.env")) as f:
    for line in f:
        line = line.strip()
        if "ELECTION_API_KEY=" in line:
            parts = line.split("=", 1)
            if len(parts) > 1:
                api_key = parts[1]
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
        body = e.read().decode()
        print(f"  HTTP {e.code}: {body[:200]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

payload = {
    "key": "ELECTION_API_KEY",
    "scopes": ["builds"],
    "values": [{"context": "all", "value": api_key}]
}
print("\nCreating env var on Netlify...")
r = api("POST", f"/sites/{site_id}/env", payload)
if r:
    print("OK:", r.get("key"), "-", [v.get("context") for v in r.get("values", [])])
else:
    # Try alternative: PATCH
    print("POST failed, trying PATCH...")
    r2 = api("PATCH", f"/sites/{site_id}/env/ELECTION_API_KEY", payload)
    if r2:
        print("OK:", r2.get("key"))

# Final verification
result = api("GET", f"/sites/{site_id}/env")
if result and isinstance(result, list):
    print("\nFinal env vars:", [e.get("key") for e in result])
elif result and isinstance(result, dict):
    print("\nFinal env vars:", result.get("key"))
