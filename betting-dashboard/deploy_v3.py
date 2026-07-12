"""Netlify deploy - try uploading via different method."""
import hashlib, os, subprocess, json, sys, tempfile, time

DIST = r"C:\Users\irfan\rakyathub\betting-dashboard\dist"
TOKEN = "nfp_fGAN5ehwsHaD87oZmJ24AF2Gvi473ZnQ216c"
SITE = "3d225a22-04e0-40fa-9629-0fb0f9cb8d40"

def curl_put(url, data, desc="", timeout=30):
    """Upload data via curl PUT using a temp file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tf:
        tf.write(data)
        tf_path = tf.name
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout), "-X", "PUT",
             "-H", f"Authorization: Bearer {TOKEN}",
             "-H", "Content-Type: application/octet-stream",
             "--data-binary", f"@{tf_path}",
             url],
            capture_output=True, text=True, timeout=timeout+5,
        )
        return result.stdout.strip(), result.stderr.strip()
    finally:
        os.unlink(tf_path)

# Build manifest
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

# Create deploy
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
required = d.get("required", [])
print(f"Deploy: {deploy_id}")
print(f"Required: {len(required)} files")

if not deploy_id:
    print(f"Error: {result.stdout[:300]}")
    sys.exit(1)

# Upload files - try PATH method first, then SHA
uploaded = 0
failed = 0
for sha in required:
    # Find path for SHA
    path_for_sha = None
    for p, (c, s) in file_map.items():
        if s == sha:
            path_for_sha = p
            content = c
            break
    if not path_for_sha:
        continue
    
    # Try uploading by PATH
    stdout, stderr = curl_put(
        f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{path_for_sha}",
        content
    )
    if '"code":422' not in stdout and '"error"' not in stdout.lower() and len(stdout) < 100:
        print(f"  OK(path) {path_for_sha}")
        uploaded += 1
    else:
        # Try by SHA
        stdout2, stderr2 = curl_put(
            f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{sha}",
            content
        )
        if '"code":422' not in stdout2 and '"error"' not in stdout2.lower() and len(stdout2) < 100:
            print(f"  OK(sha) {path_for_sha}")
            uploaded += 1
        else:
            print(f"  FAIL {path_for_sha}: {stdout[:80]}")
            failed += 1

print(f"\nUploaded: {uploaded}, Failed: {failed}")

# If all uploaded successfully, try to trigger processing
if failed == 0 and uploaded > 0:
    print("\nAll files uploaded. Triggering lock...")
    subprocess.run(
        ["curl", "-s", "--max-time", "10", "-X", "POST",
         "-H", f"Authorization: Bearer {TOKEN}",
         f"https://api.netlify.com/api/v1/deploys/{deploy_id}/lock"],
        capture_output=True, text=True, timeout=10,
    )

# Wait for ready
print("\nWaiting for deploy...")
for i in range(20):
    time.sleep(4)
    r = subprocess.run(
        ["curl", "-s", "--max-time", "10",
         "-H", f"Authorization: Bearer {TOKEN}",
         f"https://api.netlify.com/api/v1/deploys/{deploy_id}"],
        capture_output=True, text=True, timeout=10,
    )
    try:
        sd = json.loads(r.stdout)
        s = sd.get("state")
        pub = sd.get("published_at")
        err = sd.get("error_message")
        print(f"  [{i+1}] state={s} pub={pub or '-'} err={err or '-'}")
        if s == "ready" and pub:
            print("\n✅ DEPLOYED!")
            break
        if err:
            print(f"\n❌ Error: {err}")
            break
    except:
        print(f"  [{i+1}] parse error")

print(f"\nURL: https://sportmania-betting.netlify.app")
