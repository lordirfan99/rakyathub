"""Upload to Netlify deploy using curl via subprocess."""
import hashlib, os, subprocess, json, sys

DIST = r"C:\Users\irfan\rakyathub\betting-dashboard\dist"
TOKEN = "nfp_fGAN5ehwsHaD87oZmJ24AF2Gvi473ZnQ216c"
SITE = "3d225a22-04e0-40fa-9629-0fb0f9cb8d40"

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

if required:
    sha_to_path = {v[1]: k for k, v in file_map.items()}
    for sha in required:
        relpath = sha_to_path.get(sha)
        if not relpath:
            print(f"  SKIP unknown sha: {sha[:16]}...")
            continue
        content = file_map[relpath][0]
        print(f"  Uploading {relpath} ({len(content)} bytes)...")
        
        # Try by SHA
        proc = subprocess.run(
            [
                "curl", "-s", "--max-time", "30", "-X", "PUT",
                "-H", f"Authorization: Bearer {TOKEN}",
                "-H", "Content-Type: application/octet-stream",
                f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{sha}",
                "--data-binary", "@-",
            ],
            input=content, capture_output=True, text=True, timeout=30,
        )
        sha_result = proc.stdout.strip()
        
        if sha_result and "error" not in sha_result.lower() and "422" not in str(proc.stderr):
            print(f"    SHA OK: {sha_result[:80]}")
        else:
            print(f"    SHA failed: {sha_result[:100]}")
            # Try by path
            proc2 = subprocess.run(
                [
                    "curl", "-s", "--max-time", "30", "-X", "PUT",
                    "-H", f"Authorization: Bearer {TOKEN}",
                    "-H", "Content-Type: application/octet-stream",
                    f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{relpath}",
                    "--data-binary", "@-",
                ],
                input=content, capture_output=True, text=True, timeout=30,
            )
            path_result = proc2.stdout.strip()
            if path_result and "error" not in path_result.lower() and "422" not in str(proc2.stderr):
                print(f"    Path OK: {path_result[:80]}")
            else:
                print(f"    Path failed: {path_result[:100]}")

# Lock
print("\nLocking deploy...")
lock = subprocess.run(
    [
        "curl", "-s", "--max-time", "15", "-X", "POST",
        "-H", f"Authorization: Bearer {TOKEN}",
        f"https://api.netlify.com/api/v1/deploys/{deploy_id}/lock",
    ],
    capture_output=True, text=True, timeout=15,
)
print(f"  Locked: {lock.stdout[:80]}")

# Poll
print("\nWaiting for deploy...")
for i in range(15):
    import time
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
        print(f"\n❌ Deploy error: {err}")
        break

print(f"\nURL: https://sportmania-betting.netlify.app")
