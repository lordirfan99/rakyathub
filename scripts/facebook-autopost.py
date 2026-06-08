#!/usr/bin/env python3
"""Post new RakyatHub articles to Facebook page.

Usage:
  python3 scripts/facebook-autopost.py                  # posts latest new article
  python3 scripts/facebook-autopost.py --all             # posts all unposted new articles
  python3 scripts/facebook-autopost.py --url <url>       # posts a specific URL

Requires:
  - FACEBOOK_PAGE_TOKEN env var or scripts/.fb_token file
  - FACEBOOK_PAGE_ID env var or defaults to RakyatHub page
"""

import os, sys, json, subprocess, re, time, urllib.request, urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOKEN_FILE = REPO / 'scripts' / '.fb_token'
PAGE_ID = '722736938147022'

def get_token():
    """Get FB page token from env or file."""
    tok = os.environ.get('FACEBOOK_PAGE_TOKEN')
    if tok:
        return tok
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    print("❌ No Facebook token found. Set FACEBOOK_PAGE_TOKEN or create scripts/.fb_token")
    sys.exit(1)

def get_new_articles():
    """Find new article slugs from latest git commits (today)."""
    result = subprocess.run(
        ['git', 'log', '--since=today', '--name-only', '--pretty=format:',
         '--', 'src/data/post/'],
        capture_output=True, text=True, cwd=REPO
    )
    files = set()
    for line in result.stdout.strip().split('\n'):
        line = line.strip()
        if line.endswith('.md') and 'src/data/post/' in line:
            slug = Path(line).stem
            files.add(slug)
    return list(files)

def get_article_meta(slug):
    """Extract title and excerpt from article frontmatter."""
    path = REPO / 'src' / 'data' / 'post' / f'{slug}.md'
    if not path.exists():
        return None, None
    content = path.read_text(encoding='utf-8')
    title_m = re.search(r'title:\s*"(.+?)"', content)
    excerpt_m = re.search(r'excerpt:\s*"(.+?)"', content)
    title = title_m.group(1) if title_m else slug.replace('-', ' ').title()
    excerpt = excerpt_m.group(1) if excerpt_m else ''
    return title, excerpt

def get_posted_log():
    """Read set of already-posted article slugs."""
    log = REPO / 'scripts' / '.fb_posted.log'
    if log.exists():
        return set(log.read_text().strip().split('\n'))
    return set()

def mark_posted(slug):
    """Mark article as posted."""
    log = REPO / 'scripts' / '.fb_posted.log'
    posted = get_posted_log()
    posted.add(slug)
    log.write_text('\n'.join(sorted(posted)) + '\n')

def post_to_facebook(title, url, token):
    """Post article to Facebook page."""
    message = f"📖 {title}\n\n{url}"
    
    import urllib.request
    data = urllib.parse.urlencode({
        'message': message,
        'link': url,
        'access_token': token
    }).encode()
    
    req = urllib.request.Request(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed',
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        if 'id' in result:
            return True, result['id']
        return False, result.get('error', str(result))
    except Exception as e:
        return False, str(e)

def main():
    posted = get_posted_log()
    token = get_token()
    
    slugs = get_new_articles()
    
    if '--url' in sys.argv:
        idx = sys.argv.index('--url')
        url = sys.argv[idx + 1]
        slug = url.strip('/').split('/')[-1]
        title, _ = get_article_meta(slug)
        if not title:
            title = slug.replace('-', ' ').title()
        ok, msg = post_to_facebook(title, url, token)
        if ok:
            print(f"✅ Posted: {title}")
            mark_posted(slug)
        else:
            print(f"❌ Failed: {msg}")
        return
    
    if '--all' in sys.argv:
        targets = slugs
    else:
        targets = slugs[:1]  # just one by default
    
    new_posts = [s for s in targets if s not in posted]
    
    if not new_posts:
        print("No new articles to post.")
        return
    
    base_url = 'https://rakyathub.my'
    for slug in new_posts:
        title, excerpt = get_article_meta(slug)
        if not title:
            print(f"⚠️  Skipping {slug}: no article found")
            continue
        
        article_url = f'{base_url}/{slug}/'
        ok, msg = post_to_facebook(title, article_url, token)
        if ok:
            print(f"✅ Posted: {title}")
            mark_posted(slug)
        else:
            print(f"❌ Failed {slug}: {msg}")
            time.sleep(2)

if __name__ == '__main__':
    main()
