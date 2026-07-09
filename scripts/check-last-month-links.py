import os, re, glob
from datetime import datetime

cutoff = datetime(2026, 6, 9)
recent_slugs = []

for f in sorted(glob.glob('src/data/post/*.md')):
    slug = os.path.splitext(os.path.basename(f))[0]
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    m = re.search(r'^publishDate:\s*(.+)', content, re.MULTILINE)
    if not m:
        continue
    pd_str = m.group(1).strip().strip('"').strip("'")
    for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S']:
        try:
            pd = datetime.strptime(pd_str, fmt)
            break
        except:
            continue
    if pd >= cutoff:
        recent_slugs.append((slug, f))

print(f'Total articles since {cutoff.date()}: {len(recent_slugs)}')

link_pattern = re.compile(r'\]\(/(?!https?://)[^)]+/\)')
missing = []
has_links = []

for slug, f in recent_slugs:
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    parts = content.split('---', 2)
    body = parts[2] if len(parts) >= 3 else content
    
    links = link_pattern.findall(body)
    if len(links) < 2:
        has_baca = bool(re.search(r'Baca juga|artikel lain|artikel-artikel|baca juga', body, re.IGNORECASE))
        missing.append((slug, len(links), has_baca, f))
    else:
        has_links.append((slug, len(links)))

print(f'\nArticles WITH >=2 internal links: {len(has_links)}')
print(f'Articles MISSING internal links (<2): {len(missing)}')
print(f'\n--- MISSING ---')
for slug, count, has_baca, f in missing:
    status = "HAS baca juga" if has_baca else "NO baca juga"
    print(f'  {count} link(s) | {status:20s} | {slug}')
