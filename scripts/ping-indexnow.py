#!/usr/bin/env python3
"""
IndexNow URL submission for RakyatHub.
Submits new URLs to Bing, Yandex, Seznam (IndexNow protocol).

Usage:
    python scripts/ping-indexnow.py [url]
    
If no URL provided, submits the sitemap and latest article.
"""

import secrets
import string
import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

SITE = "https://rakyathub.my"
SITEMAP = f"{SITE}/sitemap-index.xml"

# IndexNow key file path
KEY_FILE = Path(__file__).parent / "indexnow-key.txt"
PUBLIC_KEY_PATH = Path(__file__).parent.parent / "public"

def get_or_create_key():
    """Get existing key from public/ folder or generate a new one."""
    # Check if any .txt file in public/ looks like an indexnow key (32 hex chars)
    pub_dir = PUBLIC_KEY_PATH
    for f in os.listdir(pub_dir):
        if f.endswith(".txt"):
            key_candidate = f.replace(".txt", "")
            if len(key_candidate) == 32 and all(c in string.hexdigits for c in key_candidate):
                KEY_FILE.write_text(key_candidate)
                return key_candidate
    # Generate a new key
    key = secrets.token_hex(16)
    KEY_FILE.write_text(key)
    print(f"[IndexNow] ✅ New key generated: {key}")
    return key

def host_key_file(key):
    """Ensure the key file is hosted at SITE/{key}.txt for verification."""
    key_path = PUBLIC_KEY_PATH / f"{key}.txt"
    if not key_path.exists():
        key_path.write_text(key)
        print(f"[IndexNow] 📄 Created public key file: public/{key}.txt")
        return True
    return False

def submit_url(url, key, host=None):
    """Submit a URL to IndexNow."""
    if host is None:
        host = SITE.replace("https://", "")
    
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{SITE}/{key}.txt",
        "urlList": [url]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            code = resp.getcode()
            if code == 200:
                print(f"[IndexNow] ✅ Submitted: {url}")
                return True
            else:
                print(f"[IndexNow] ⚠️ {code}: {url}")
                return False
    except urllib.error.HTTPError as e:
        print(f"[IndexNow] ❌ HTTP {e.code}: {url}")
        if e.code == 422:
            print("   (Key not verified yet - takes a few minutes after hosting)")
        return False
    except Exception as e:
        print(f"[IndexNow] ❌ Error: {e}")
        return False

def get_latest_article_url():
    """Get URL of the most recently committed article."""
    repo_dir = Path(__file__).parent.parent
    try:
        result = subprocess.run(
            ["git", "log", "--name-only", "--diff-filter=A", "-1", "--pretty=format:", "--", "src/data/post/"],
            capture_output=True, text=True, timeout=10,
            cwd=repo_dir
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        if files:
            filename = files[-1].replace("src/data/post/", "").replace(".md", "")
            return f"{SITE}/{filename}/"
    except:
        pass
    return None

def main():
    print("=" * 50)
    print("🚀 RakyatHub — IndexNow Pinger")
    print("=" * 50)
    
    key = get_or_create_key()
    hosted = host_key_file(key)
    
    if hosted:
        print("[IndexNow] ⏳ Key file created. Will be active after next deploy.")
        print(f"   Key: {key}")
        print(f"   URL: {SITE}/{key}.txt")
    
    # Get URL from command line or use latest article
    url = sys.argv[1] if len(sys.argv) > 1 else get_latest_article_url()
    
    if url:
        submit_url(url, key)
        print()
    
    # Also submit the sitemap
    print("[IndexNow] Submitting sitemap as bulk signal...")
    submit_url(SITEMAP, key)
    
    print(f"\n✅ Done! Search engines notified.")
    print(f"📄 Latest: {url or 'sitemap only'}")

if __name__ == "__main__":
    main()
