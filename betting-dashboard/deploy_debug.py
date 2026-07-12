"""Debug the Netlify deploy — find out why uploads fail with 422."""
import hashlib, os, subprocess, json, sys, tempfile, time

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
print(f"Files in manifest: {len(manifest)}")
for p, s in manifest.items():
    print(f"  {p}: {s[:16]}...")

# Create deploy
manifest_json = json.dumps({"files": manifest})
print(f"\nManifest JSON length: {len(manifest_json)}")
print(f"Creating deploy...")

result = subprocess.run(
    ["curl", "-s", "--max-time", "30", "-X", "POST",
     "-H", f"Authorization: Bearer {TOKEN}",
     "-H", "Content-Type: application/json",
     f"https://api.netlify.com/api/v1/sites/{SITE}/deploys",
     "-d", manifest_json],
    capture_output=True, text=True, timeout=30,
)

try:
    d = json.loads(result.stdout)
except Exception as e:
    print(f"JSON parse error: {e}")
    print(f"Raw response: {result.stdout[:500]}")
    sys.exit(1)

deploy_id = d.get("id")
state = d.get("state")
required = d.get("required", [])
print(f"\nDeploy ID: {deploy_id}")
print(f"State: {state}")
print(f"Required: {required}")

if not deploy_id:
    print(f"Error creating deploy: {result.stdout[:500]}")
    sys.exit(1)

# Upload ONE file to test
if required:
    sha = required[0]
    # Find path for this SHA
    path_for_sha = None
    for p, s in file_map.items():
        if s == sha:
            path_for_sha = p
            break
    
    if path_for_sha:
        content = file_map[path_for_sha][0]
        content_sha = hashlib.sha256(content).hexdigest()
        print(f"\nTrying upload: {path_for_sha}")
        print(f"  Content SHA: {content_sha}")
        print(f"  Required SHA: {sha}")
        print(f"  Match: {content_sha == sha}")
        
        # Upload by SHA
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tf:
            tf.write(content)
            tf_path = tf.name
        
        try:
            res = subprocess.run(
                ["curl", "-s", "--max-time", "15", "-X", "PUT",
                 "-H", f"Authorization: Bearer {TOKEN}",
                 "-H", "Content-Type: application/octet-stream",
                 "--data-binary", f"@{tf_path}",
                 f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{sha}"],
                capture_output=True, text=True, timeout=15,
            )
            print(f"  SHA upload response ({res.returncode}): {res.stdout[:200]}")
            print(f"  Stderr: {res.stderr[:200]}")
        finally:
            os.unlink(tf_path)
else:
    print("\nNo required files (all cached)")
    
# Check deploy state
print("\nCurrent deploy state:")
state_res = subprocess.run(
    ["curl", "-s", "--max-time", "10",
     "-H", f"Authorization: Bearer {TOKEN}",
     f"https://api.netlify.com/api/v1/deploys/{deploy_id}"],
    capture_output=True, text=True, timeout=10,
)
try:
    sd = json.loads(state_res.stdout)
    print(f"  State: {sd.get('state')}")
    print(f"  Required: {sd.get('required')}")
    print(f"  Summary: {sd.get('summary')}")
    print(f"  Published: {sd.get('published_at')}")
except Exception as e:
    print(f"  Parse error: {e}")
    print(f"  Raw: {state_res.stdout[:300]}")
