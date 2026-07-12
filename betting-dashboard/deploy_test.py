"""Test Netlify deploy with direct upload."""
import hashlib, json, requests, os, sys, time

TOKEN = "nfp_fGAN5ehwsHaD87oZmJ24AF2Gvi473ZnQ216c"
SITE_ID = "3d225a22-04e0-40fa-9629-0fb0f9cb8d40"
DIST_DIR = r"C:\Users\irfan\rakyathub\betting-dashboard\dist"

ha = {"Authorization": f"Bearer {TOKEN}"}

file_map = {}
for root, dirs, fnames in os.walk(DIST_DIR):
    for fname in fnames:
        fpath = os.path.join(root, fname)
        relpath = os.path.relpath(fpath, DIST_DIR).replace("\\", "/")
        with open(fpath, "rb") as f:
            content = f.read()
        sha256 = hashlib.sha256(content).hexdigest()
        file_map[relpath] = (content, sha256)
        print(f"  {relpath}: {sha256[:16]}... ({len(content)} bytes)")

files_manifest = {k: v[1] for k, v in file_map.items()}
print(f"\nCreating deploy...")
resp = requests.post(
    f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys",
    headers={**ha, "Content-Type": "application/json"},
    json={"files": files_manifest},
    timeout=30,
)
d = resp.json()
deploy_id = d.get("id")
print(f"Deploy ID: {deploy_id}")
print(f"State: {d.get('state')}")
print(f"Required: {d.get('required')}")
print(f"Error: {d.get('error_message', '(none)')}")

if not deploy_id:
    print("Failed to create deploy")
    sys.exit(1)

required = d.get("required", [])
if not required:
    print("\nNo files need uploading - all cached.")
else:
    print(f"\nUploading {len(required)} files...")
    sha_to_path = {v[1]: k for k, v in file_map.items()}
    for sha in required:
        relpath = sha_to_path.get(sha)
        if not relpath:
            print(f"  SKIP unknown sha: {sha[:16]}...")
            continue
        content = file_map[relpath][0]
        put_resp = requests.put(
            f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{relpath}",
            headers={**ha, "Content-Type": "application/octet-stream"},
            data=content,
            timeout=30,
        )
        if put_resp.status_code == 200:
            print(f"  OK {relpath} (by path)")
        else:
            put_resp2 = requests.put(
                f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{sha}",
                headers={**ha, "Content-Type": "application/octet-stream"},
                data=content,
                timeout=30,
            )
            if put_resp2.status_code == 200:
                print(f"  OK {relpath} (by SHA)")
            else:
                print(f"  FAIL {relpath}: path={put_resp.status_code} sha={put_resp2.status_code}")
                print(f"    path err: {put_resp.text[:100]}")
                print(f"    sha err: {put_resp2.text[:100]}")

print("\nLocking deploy...")
lock = requests.post(
    f"https://api.netlify.com/api/v1/deploys/{deploy_id}/lock",
    headers=ha,
    timeout=30,
)
print(f"  Lock: {lock.status_code}")

print("\nWaiting for deploy...")
for i in range(15):
    time.sleep(4)
    r = requests.get(f"https://api.netlify.com/api/v1/deploys/{deploy_id}", headers=ha, timeout=15)
    rd = r.json()
    s = rd.get("state", "")
    pub = rd.get("published_at")
    err = rd.get("error_message")
    print(f"  [{i+1}] {s}" + (f" pub={pub}" if pub else "") + (f" err={err}" if err else ""))
    if s == "ready" or pub:
        break
    if err:
        break

print(f"\nURL: https://sportmania-betting.netlify.app")
