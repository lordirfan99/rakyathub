#!/usr/bin/env python3
"""Post new RakyatHub articles to Facebook with engaging teasers + link in comments.

Usage:
  python3 scripts/facebook-autopost.py                  # posts latest new article
  python3 scripts/facebook-autopost.py --all             # posts all unposted new articles
  python3 scripts/facebook-autopost.py --url <url>       # posts a specific URL

Requires scripts/.fb_token file with a Facebook Page Access Token.
"""

import os, sys, json, subprocess, re, time, urllib.request, urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOKEN_FILE = REPO / 'scripts' / '.fb_token'
PAGE_ID = '722736938147022'

# ── Token ──────────────────────────────────────────
def get_token():
    tok = os.environ.get('FACEBOOK_PAGE_TOKEN') or (
        TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else None)
    if tok: return tok
    print("❌ No Facebook token. Set FACEBOOK_PAGE_TOKEN or create scripts/.fb_token")
    sys.exit(1)

# ── Article detection via filesystem ──────────────
def get_new_articles():
    """Find all .md articles not yet in the posted log."""
    posts_dir = REPO / 'src' / 'data' / 'post'
    if not posts_dir.exists():
        return []
    posted = get_posted_log()
    results = []
    for f in sorted(posts_dir.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True):
        slug = f.stem
        if slug not in posted:
            results.append(slug)
    return results

# ── Article parsing ───────────────────────────────
def get_article_meta(slug):
    path = REPO / 'src' / 'data' / 'post' / f'{slug}.md'
    if not path.exists():
        return None, None, [], ''
    content = path.read_text(encoding='utf-8')
    
    title_m = re.search(r'title:\s*"(.+?)"', content)
    excerpt_m = re.search(r'excerpt:\s*"(.+?)"', content)
    title = title_m.group(1) if title_m else slug.replace('-', ' ').title()
    excerpt = excerpt_m.group(1) if excerpt_m else ''
    
    # Extract H2 headings as teaser points (skip "Kesimpulan" & "Soalan Lazim")
    teasers = []
    for m in re.finditer(r'^##\s+(.+)$', content, re.MULTILINE):
        h2 = m.group(1).strip()
        # Skip emoji-only, Kesimpulan, FAQ, and navigational headings
        skip_words = ['kesimpulan', 'soalan lazim', 'tindakan segera', 'artikel berkaitan',
                       'kalkulator', 'lagi', 'dokumen', 'sumber rujukan']
        if any(s in h2.lower() for s in skip_words):
            continue
        # Remove leading emoji for cleaner teaser
        clean = re.sub(r'^[^\w\s]*\s*', '', h2)
        if clean and len(clean) > 10:
            teasers.append(clean)
    
    return title, excerpt, teasers[:4], content  # max 4 teasers

def get_category(content):
    m = re.search(r'category:\s*"?(.+?)"?\n', content)
    return m.group(1).strip() if m else ''

# ── Posting log ───────────────────────────────────
def get_posted_log():
    log = REPO / 'scripts' / '.fb_posted.log'
    if log.exists():
        return set(filter(None, log.read_text().strip().split('\n')))
    return set()

def mark_posted(slug):
    log = REPO / 'scripts' / '.fb_posted.log'
    posted = get_posted_log()
    posted.add(slug)
    log.write_text('\n'.join(sorted(posted)) + '\n')

# ── Facebook API calls ────────────────────────────
def fb_post(message, link_url, token):
    data = urllib.parse.urlencode({
        'message': message,
        'link': link_url,
        'access_token': token
    }).encode()
    req = urllib.request.Request(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed',
        data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        if 'id' in result:
            return True, result['id']
        return False, result
    except Exception as e:
        return False, str(e)

# ── Message builder ───────────────────────────────
def pick_emoji(title, category):
    mapping = [
        ('kwsp', '🏦'), ('asb', '💰'), ('emas', '🟡'),
        ('kereta', '🚗'), ('insurans', '🛡️'), ('kewangan', '💵'),
        ('kerajaan', '🏛️'), ('percukaian', '🧾'), ('kerjaya', '💼'),
        ('pelaburan', '📈'), ('medic', '🏥'), ('rumah', '🏠'),
        ('loan', '💳'), ('ptptn', '🎓'),
    ]
    for kw, e in mapping:
        if kw in title.lower() or kw in category.lower():
            return e
    return '📖'

def build_post(title, excerpt, teasers, category):
    """Natural, short casual post — macam orang sembang je."""
    emoji = pick_emoji(title, category)
    
    # Just a short natural paragraph
    parts = [f"{emoji} Baru update artikel — {title.lower().rstrip('.')}"]
    
    if excerpt:
        excerpt_clean = excerpt.strip('.')
        parts.append(f"\n{excerpt_clean}.")
    
    # One natural sentence from teasers if available
    if teasers:
        sample = teasers[0]
        parts.append(f"\nAntara yang dibincangkan: {sample.lower()}.")
        if len(teasers) > 1:
            parts.append(f"Plus, {teasers[1].lower()}.")
    
    parts.append(f"\nFull details dekat link bawah — ada angka, jadual, langkah praktikal semua dah siap.")
    
    return '\n'.join(parts)

# ── Main ──────────────────────────────────────────
def main():
    posted = get_posted_log()
    token = get_token()
    
    slugs = get_new_articles()
    
    # Manual URL mode
    if '--url' in sys.argv:
        idx = sys.argv.index('--url')
        url = sys.argv[idx + 1]
        slug = url.strip('/').split('/')[-1]
        title, excerpt, teasers, content = get_article_meta(slug)
        if not title:
            title = slug.replace('-', ' ').title()
        cat = get_category(content) if content else ''
        msg = build_post(title, excerpt or '', teasers, cat)
        article_url = f'https://rakyathub.my/{slug}/'
        ok, post_id = fb_post(msg, article_url, token)
        if ok:
            print(f"✅ Posted: {title}")
            mark_posted(slug)
        else:
            print(f"❌ Failed: {post_id}")
        return
    
    # Auto mode — one per run by default
    targets = slugs if '--all' in sys.argv else slugs[:1]
    new_posts = [s for s in targets if s not in posted]
    
    if not new_posts:
        print("No new articles to post.")
        return
    
    for slug in new_posts:
        title, excerpt, teasers, content = get_article_meta(slug)
        if not title:
            print(f"⚠️  Skipping {slug}: no article found")
            continue
        
        cat = get_category(content) if content else ''
        msg = build_post(title, excerpt or '', teasers, cat)
        
        article_url = f'https://rakyathub.my/{slug}/'
        ok, post_id = fb_post(msg, article_url, token)
        if ok:
            print(f"✅ Posted: {title}")
            mark_posted(slug)
        else:
            print(f"❌ Failed {slug}: {post_id}")
            time.sleep(2)

if __name__ == '__main__':
    main()
