#!/usr/bin/env python3
"""
Full Deploy Pipeline for RakyatHub
===================================
1. Git add + commit + push (sync source to GitHub)
2. npm run build (local build)
3. Zip deploy to Netlify (zero build minutes)
4. Clean up dist/ to save disk space

Usage:
    python scripts/full-deploy.py                              # auto-detect message
    python scripts/full-deploy.py "feat: update harga minyak"   # custom message
    python scripts/full-deploy.py --no-push                     # skip git push
    python scripts/full-deploy.py --no-clean                    # keep dist/ after deploy
    python scripts/full-deploy.py --build-only                  # build only, no deploy
    python scripts/full-deploy.py --deploy-only                 # deploy only (skip git+clean)
"""

import os, sys, subprocess, json, urllib.request, zipfile, io, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
DIST_DIR = PROJECT_DIR / 'dist'


def run(cmd, cwd=None, check=True, timeout=300):
    """Run a shell command and return output."""
    print(f"\n$ {cmd}")
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or str(PROJECT_DIR),
        capture_output=True, text=True, timeout=timeout
    )
    for line in result.stdout.splitlines():
        print(f"  {line}")
    if result.stderr:
        for line in result.stderr.splitlines():
            print(f"  ! {line}", file=sys.stderr)
    if check and result.returncode != 0:
        print(f"  ❌ Failed (exit code {result.returncode})")
        sys.exit(result.returncode)
    return result


def git_status():
    """Check if there are uncommitted changes."""
    result = run("git status --short", check=False)
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    if not lines:
        print("  ℹ️  No changes to commit.")
        return None
    return lines


def git_commit_push(message):
    """Add, commit, and push to GitHub."""
    files = git_status()
    if files is None:
        return False

    print(f"\n📦 Changes to commit ({len(files)} files):")
    for f in files:
        print(f"     {f}")

    run("git add -A")
    run(f'git commit -m "{message} [skip netlify]"')
    run("git push")
    return True


def npm_build():
    """Build the Astro site."""
    print("\n🏗️  Building...")
    run("npm run build", timeout=600)
    return DIST_DIR.exists()


def zip_deploy():
    """Deploy dist/ to Netlify via zip upload."""
    if not DIST_DIR.exists():
        print("  ❌ dist/ not found. Build first.")
        return False

    print("\n📤 Deploying to Netlify...")

    # Get token
    token = os.environ.get('NETLIFY_AUTH_TOKEN', '')
    env_path = os.path.expanduser('~/AppData/Local/hermes/.env')
    if not token and os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith('NETLIFY_AUTH_TOKEN='):
                    token = line.strip().split('=', 1)[1]
                    break

    if not token:
        print("  ❌ NETLIFY_AUTH_TOKEN not found")
        return False

    site_id = '6a5f68a4-d25a-4c02-880a-77a154e73472'

    # Zip dist/ to memory
    print("  Zipping...")
    zip_buffer = io.BytesIO()
    total_files = 0
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, filenames in os.walk(str(DIST_DIR)):
            for fn in filenames:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, str(DIST_DIR)).replace(os.sep, '/')
                zf.write(full, rel)
                total_files += 1

    data = zip_buffer.getvalue()
    print(f"  📦 {total_files} files, {len(data)/1024:.0f} KB")

    # Upload
    url = f'https://api.netlify.com/api/v1/sites/{site_id}/deploys'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/zip'
    }, data=data, method='POST')

    with urllib.request.urlopen(req, timeout=600) as resp:
        deploy = json.loads(resp.read().decode())

    did = deploy['id']
    print(f"  🔗 Deploy ID: {did}")

    # Poll until ready, then publish
    for i in range(30):
        time.sleep(3)
        d_req = urllib.request.Request(
            f'https://api.netlify.com/api/v1/sites/{site_id}/deploys/{did}',
            headers={'Authorization': f'Bearer {token}'}
        )
        with urllib.request.urlopen(d_req, timeout=30) as d_resp:
            d = json.loads(d_resp.read().decode())
            state = d.get('state', '?')
            print(f"     state={state}", end='\r')
            if state == 'ready':
                # Publish (restore to make it live)
                r_req = urllib.request.Request(
                    f'https://api.netlify.com/api/v1/sites/{site_id}/deploys/{did}/restore',
                    headers={'Authorization': f'Bearer {token}'},
                    method='POST'
                )
                with urllib.request.urlopen(r_req, timeout=60) as r_resp:
                    r = json.loads(r_resp.read().decode())
                    print(f"\n  ✅ Published at {r.get('published_at', 'N/A')}")
                    print(f"  🌐 {r.get('ssl_url', r.get('url', 'N/A'))}")
                break
        if i == 29:
            print("\n  ⏰ Timed out waiting for deploy")
    
    return True


def clean_dist():
    """Remove dist/ to save ~350MB disk space."""
    if DIST_DIR.exists():
        import shutil
        shutil.rmtree(str(DIST_DIR))
        print(f"\n🧹 dist/ cleaned (saved ~350 MB)")


def main():
    # Parse args
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = set(a for a in sys.argv[1:] if a.startswith('--'))

    custom_message = args[0] if args else None
    skip_push = '--no-push' in flags or '--deploy-only' in flags
    no_clean = '--no-clean' in flags
    build_only = '--build-only' in flags
    deploy_only = '--deploy-only' in flags

    print("=" * 60)
    print("🚀 RakyatHub Full Deploy Pipeline")
    print("=" * 60)

    # Step 1: Git sync
    if not deploy_only:
        message = custom_message or "feat: update articles + deploy"
        print(f"\n📌 Commit message: {message}")
        committed = git_commit_push(message)
        
        if committed:
            print("  ✅ Source synced to GitHub")
        else:
            print("  ℹ️  No changes to commit")

    # Step 2: Build
    if not deploy_only:
        print(f"\n🔨 Building locally...")
        if not npm_build():
            print("  ❌ Build failed")
            sys.exit(1)
        print("  ✅ Build successful")

    # Step 3: Deploy
    if not build_only:
        if not zip_deploy():
            print("  ❌ Deploy failed")
            sys.exit(1)

    # Step 4: Cleanup
    if not no_clean and not build_only:
        clean_dist()

    print("\n" + "=" * 60)
    print("✅ Pipeline complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
