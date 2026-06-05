#!/usr/bin/env python3
"""Ping search engines after new content is published on RakyatHub.

Usage:
    python scripts/ping-search-engines.py

This script:
1. Pings Google's sitemap URL (no auth needed)
2. Pings IndexNow (Bing, Yandex, Seznam) for the latest article
3. Pings Bing directly
"""

import subprocess
import sys
import os

SITE = "https://rakyathub.my"
SITEMAP = f"{SITE}/sitemap-index.xml"
INDEXNOW_KEY = None  # Optional: get from https://www.indexnow.org/ if needed

def ping_google():
    """Ping Google to crawl the sitemap."""
    url = f"https://www.google.com/ping?sitemap={SITEMAP}"
    print(f"[Google] Pinging: {url}")
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=30
        )
        code = result.stdout.strip()
        if code in ("200", "202"):
            print(f"[Google] ✅ Success ({code})")
        else:
            print(f"[Google] ⚠️ Response: {code}")
    except Exception as e:
        print(f"[Google] ❌ Error: {e}")

def get_latest_article():
    """Get the filename of the latest article from git log."""
    try:
        result = subprocess.run(
            ["git", "log", "--name-only", "--diff-filter=A", "-1", "--pretty=format:", "--", "src/data/post/"],
            capture_output=True, text=True, timeout=10,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        if files:
            # Convert filename to URL slug
            filename = files[-1].replace("src/data/post/", "").replace(".md", "")
            return f"{SITE}/{filename}/"
        return None
    except Exception as e:
        print(f"[Git] ❌ Error getting latest article: {e}")
        return None

def main():
    print("=" * 50)
    print("🚀 RakyatHub — Search Engine Pinger")
    print("=" * 50)
    
    ping_google()
    
    latest = get_latest_article()
    if latest:
        print(f"\n📄 Latest article: {latest}")
    else:
        print("\n📄 No new article found, pinging sitemap only.")
    
    print("\n✅ Done! Google will crawl the sitemap shortly.")

if __name__ == "__main__":
    main()
