#!/usr/bin/env python3
"""Deploy dist/ + functions to Netlify via CLI (zero build minutes).

Usage:
    python3 scripts/deploy_zip.py
"""
import os, subprocess, sys

def deploy():
    token = os.environ.get('NETLIFY_AUTH_TOKEN', '')
    env_path = os.path.expanduser('~/AppData/Local/hermes/.env')
    if not token and os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith('NETLIFY_AUTH_TOKEN='):
                    token = line.strip().split('=', 1)[1]
                    break
    if not token:
        print("❌ NETLIFY_AUTH_TOKEN not found")
        sys.exit(1)

    print("🚀 Deploying dist/ + functions via Netlify CLI (direct deploy)...")
    result = subprocess.run(
        'npx netlify deploy --prod --dir=dist --functions=netlify/functions --message "Direct deploy: auto"',
        shell=True, capture_output=True, text=True, timeout=600,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    out = result.stdout + result.stderr
    print(out)
    if 'Website URL' in out or 'published' in out.lower():
        print("✅ Deploy successful (0 build minutes)")
    else:
        print("⚠️  Check output above")

if __name__ == '__main__':
    deploy()
