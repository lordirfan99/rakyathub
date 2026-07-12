"""Netlify deploy v2 — upload files, wait for processing, then promote."""
import hashlib, os, subprocess, json, sys, tempfile, time

DIST = r"C:\Users\irfan\rakyathub\betting-dashboard\dist"
TOKEN = "nfp_fGAN5ehwsHaD87oZmJ24AF2Gvi473ZnQ216c"
SITE = "3d225a22-04e0-40fa-9629-0fb0f9cb8d40"

def curl(*args, data=None, timeout=30):
    cmd = ["curl", "-s", "--max-time", str(timeout)]
    if data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tf:
            tf.write(data)
            tf_path = tf.name
        cmd += ["--data-binary", f"@{tf_path}"]
    cmd.extend(a for a in args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+5)
        return result
    finally:
        if data is not None:
            try:
                os.unlink(tf_path)
            except:
                pass

# Build file manifest
file_map = {}
for root, dirs, fnames in os.walk(DIST):
    for fname in fnames:
        fpath = os.path.join(root, fname)
        relpath = os.path.relpath(fpath, DIST).replace("\\", "/")
        with open(fpath, "rb") as f:
            content = f.read()
        sha256 = hashlib.sha256(content).hexdigest()
        file_map[relpath] = (content, sha256)

manifest = {k: v[1] for k, v in file_map.items()}
print(f"Files: {list(manifest.keys())}")

# Create deploy WITHOUT locking
manifest_json = json.dumps({"files": manifest})
result = subprocess.run(
    ["curl", "-s", "--max-time", "30", "-X", "POST",
     "-H", f"Authorization: Bearer {TOKEN}",
     "-H", "Content-Type: application/json",
     f"https://api.netlify.com/api/v1/sites/{SITE}/deploys",
     "-d", manifest_json],
    capture_output=True, text=True, timeout=30,
)
d = json.loads(result.stdout)
deploy_id = d.get("id")
state = d.get("state")
required = d.get("required", [])
print(f"Deploy ID: {deploy_id}")
print(f"State: {state}")
print(f"Required: {len(required)} files")

if not deploy_id:
    print(f"Error: {result.stdout}")
    sys.exit(1)

# Upload all required files
if required:
    sha_to_path = {v[1]: k for k, v in file_map.items()}
    for sha in required:
        relpath = sha_to_path.get(sha)
        if not relpath:
            continue
        content = file_map[relpath][0]
        res = curl(
            "-X", "PUT",
            "-H", f"Authorization: Bearer {TOKEN}",
            "-H", "Content-Type: application/octet-stream",
            f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{sha}",
            data=content,
        )
        ok = res.stdout.strip() not in ("", '{"error":"upload error"}') and "error" not in res.stdout.lower()
        print(f"  {'OK' if ok else 'FAIL'} {relpath}")

# Check state after upload
time.sleep(3)
result2 = subprocess.run(
    ["curl", "-s", "--max-time", "10",
     "-H", f"Authorization: Bearer {TOKEN}",
     f"https://api.netlify.com/api/v1/deploys/{deploy_id}"],
    capture_output=True, text=True, timeout=10,
)
d2 = json.loads(result2.stdout)
print(f"\nAfter upload state: {d2.get('state')}")
print(f"Required: {d2.get('required')}")

# If still uploading, try notifying
if d2.get("state") == "uploading":
    # Trigger a re-check by doing a GET with live check
    print("Triggering deploy process...")
    for attempt in range(10):
        time.sleep(3)
        r = subprocess.run(
            ["curl", "-s", "--max-time", "10",
             "-H", f"Authorization: Bearer {TOKEN}",
             f"https://api.netlify.com/api/v1/deploys/{deploy_id}"],
            capture_output=True, text=True, timeout=10,
        )
        d3 = json.loads(r.stdout)
        s = d3.get("state")
        pub = d3.get("published_at")
        err = d3.get("error_message")
        req = d3.get("required", [])
        print(f"  [{attempt+1}] state={s} req={len(req)}" + (f" pub={pub}" if pub else "") + (f" err={err}" if err else ""))
        if s == "ready" and pub:
            print("\n✅ DEPLOYED!")
            break
        if s in ("error",) or err:
            print(f"\n❌ Error: {err}")
            break
        # If files are still required, upload them
        if req:
            sha_to_path2 = {v[1]: k for k, v in file_map.items()}
            for sha2 in req:
                rp = sha_to_path2.get(sha2)
                if not rp:
                    continue
                print(f"  Re-uploading {rp}...")
                upload_file(rp, file_map[rp][0], deploy_id)

print(f"\nLive URL: https://sportmania-betting.netlify.app")
