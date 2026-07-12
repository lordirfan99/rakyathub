"""Upload to Netlify deploy using curl via subprocess."""
import hashlib, os, subprocess, json, sys, tempfile, time

DIST = r"C:\Users\irfan\rakyathub\betting-dashboard\dist"
TOKEN = "nfp_fGAN5ehwsHaD87oZmJ24AF2Gvi473ZnQ216c"
SITE = "3d225a22-04e0-40fa-9629-0fb0f9cb8d40"

def run_curl(args, data=None):
    """Run curl with optional binary data via temp file."""
    if data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tf:
            tf.write(data)
            tf_path = tf.name
        # Use the temp file as data source
        curl_args = [
            "curl", "-s", "--max-time", "30", "-X", "PUT",
            "-H", f"Authorization: Bearer {TOKEN}",
            "-H", "Content-Type: application/octet-stream",
            "--data-binary", f"@{tf_path}",
        ] + args
        try:
            result = subprocess.run(curl_args, capture_output=True, text=True, timeout=30)
            return result
        finally:
            os.unlink(tf_path)
    else:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "15"] + args,
            capture_output=True, text=True, timeout=15,
        )
        return result

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
print(f"Files: {list(manifest.keys())}")

# Create deploy with manifest
manifest_json = json.dumps({"files": manifest})
result = subprocess.run(
    [
        "curl", "-s", "--max-time", "30", "-X", "POST",
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Content-Type: application/json",
        f"https://api.netlify.com/api/v1/sites/{SITE}/deploys",
        "-d", manifest_json,
    ],
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

upload_ok = 0
if required:
    sha_to_path = {v[1]: k for k, v in file_map.items()}
    for sha in required:
        relpath = sha_to_path.get(sha)
        if not relpath:
            print(f"  SKIP unknown sha: {sha[:16]}...")
            continue
        content = file_map[relpath][0]
        print(f"  Uploading {relpath} ({len(content)} bytes)...", end=" ", flush=True)
        
        # Try by SHA
        res = run_curl(
            [f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{sha}"],
            data=content,
        )
        out = res.stdout.strip()
        if "error_message" not in out.lower() and len(out) < 100:
            print(f"SHA OK")
            upload_ok += 1
        else:
            # Try by path
            res2 = run_curl(
                [f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{relpath}"],
                data=content,
            )
            out2 = res2.stdout.strip()
            if "error_message" not in out2.lower() and len(out2) < 100:
                print(f"PATH OK")
                upload_ok += 1
            else:
                resp_text = out if len(out) < 60 else out[:60]
                print(f"FAIL ({resp_text})")
else:
    print("No files need uploading (all cached).")

print(f"\nUploaded: {upload_ok}/{len(required)}")

# Lock
print("Locking deploy...")
lock = subprocess.run(
    [
        "curl", "-s", "--max-time", "15", "-X", "POST",
        "-H", f"Authorization: Bearer {TOKEN}",
        f"https://api.netlify.com/api/v1/deploys/{deploy_id}/lock",
    ],
    capture_output=True, text=True, timeout=15,
)
print(f"  Lock response: {lock.stdout[:80]}")

# Poll
print("Waiting for deploy...")
for i in range(20):
    time.sleep(4)
    poll = subprocess.run(
        [
            "curl", "-s", "--max-time", "10",
            "-H", f"Authorization: Bearer {TOKEN}",
            f"https://api.netlify.com/api/v1/deploys/{deploy_id}",
        ],
        capture_output=True, text=True, timeout=10,
    )
    pd = json.loads(poll.stdout)
    s = pd.get("state", "")
    pub = pd.get("published_at")
    err = pd.get("error_message")
    print(f"  [{i+1}] state={s}" + (f" pub={pub}" if pub else "") + (f" err={err}" if err else ""))
    if s == "ready" and pub:
        print("\n✅ DEPLOYED!")
        break
    if err:
        print(f"\n❌ Error: {err}")
        break

print(f"\nLive URL: https://sportmania-betting.netlify.app")
