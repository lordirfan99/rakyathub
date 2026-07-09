#!/usr/bin/env python3
"""Add "Baca juga" internal links to articles missing them.
For each article with <2 internal links, adds 2-3 contextual links
to related articles from the same category."""

import os, re, glob, sys, random
from datetime import datetime

# Config
CUTOFF = datetime(2026, 6, 9)
POST_DIR = 'src/data/post'

# Step 1: Load all articles
all_articles = {}  # slug -> {title, category, tags, body, path, publish_date}
category_index = {}  # category -> [slug, ...]

for f in glob.glob(f'{POST_DIR}/*.md'):
    slug = os.path.splitext(os.path.basename(f))[0]
    with open(f, encoding='utf-8') as fh:
        raw = fh.read()
    
    # Parse frontmatter
    parts = raw.split('---', 2)
    if len(parts) < 3:
        continue
    fm = parts[1]
    body = parts[2]
    
    # Extract fields
    title_m = re.search(r'^title:\s*"(.+)"', fm, re.MULTILINE)
    cat_m = re.search(r'^category:\s*(.+)', fm, re.MULTILINE)
    tags_m = re.findall(r'^\s+-\s+(.+)', fm, re.MULTILINE)
    pub_m = re.search(r'^publishDate:\s*(.+)', fm, re.MULTILINE)
    
    title = title_m.group(1).strip() if title_m else slug
    category = cat_m.group(1).strip().strip('"') if cat_m else 'Lain-lain'
    tags = [t.strip().strip('"') for t in tags_m]
    
    pub_date = None
    if pub_m:
        pd_str = pub_m.group(1).strip().strip('"').strip("'")
        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']:
            try:
                pub_date = datetime.strptime(pd_str, fmt)
                break
            except:
                pass
    
    all_articles[slug] = {
        'title': title,
        'category': category,
        'tags': tags,
        'body': body,
        'path': f,
        'raw': raw,
        'publish_date': pub_date,
        'parts': parts,
    }
    
    if category not in category_index:
        category_index[category] = []
    category_index[category].append(slug)

print(f"Loaded {len(all_articles)} articles in {len(category_index)} categories")

# Step 2: Find missing articles (from last month, <2 internal links)
link_pattern = re.compile(r'\]\(/(?!https?://)[^)]+/\)')

missing_articles = []
for slug, info in all_articles.items():
    if info['publish_date'] and info['publish_date'] >= CUTOFF:
        links = link_pattern.findall(info['body'])
        if len(links) < 2:
            has_baca = bool(re.search(r'Baca juga|artikel lain|artikel-artikel|artikel-artikel', info['body'], re.IGNORECASE))
            missing_articles.append((slug, info, has_baca, len(links)))

print(f"Missing articles (from last month, <2 links): {len(missing_articles)}")

# Step 3: For each missing article, find related articles from same category
baca_pattern = re.compile(r'(##\s*(Rujukan|Sumber|Rujukan Rasmi)\b.*)', re.DOTALL)

def find_related(slug, info, count=3):
    """Find related articles from same category with different slugs."""
    candidates = []
    for candidate_slug in category_index.get(info['category'], []):
        if candidate_slug == slug:
            continue
        candidates.append(candidate_slug)
    
    # Shuffle for variety
    random.shuffle(candidates)
    return candidates[:count]

def add_baca_juga(slug, info, related_slugs):
    """Add Baca juga section before the rujukan footer."""
    body = info['body']
    
    # Build the Baca juga section
    links_md = []
    for rs in related_slugs:
        if rs not in all_articles:
            continue
        r_title = all_articles[rs]['title']
        # Extract a clean anchor text from the title (remove year suffixes etc.)
        anchor = r_title
        # Trim if too long
        if len(anchor) > 60:
            anchor = anchor[:57] + '...'
        links_md.append(f"- [{anchor}](/{rs}/)")
    
    if not links_md:
        return None  # No related articles found
    
    baca_section = "\n**Baca juga:**\n" + "\n".join(links_md) + "\n"
    
    # Try to insert before "## Rujukan" or "## Rujukan Rasmi" section
    rujukan_match = re.search(r'\n## (?:Rujukan|Sumber|Rujukan Rasmi|📚|Kredit Gambar)', body)
    if rujukan_match:
        insert_pos = rujukan_match.start()
        new_body = body[:insert_pos] + baca_section + '\n' + body[insert_pos:]
    else:
        # Insert before the last --- if exists, or at the end
        new_body = body.rstrip() + '\n\n' + baca_section + '\n'
    
    return new_body

# Step 4: Apply changes
random.seed(42)
changes = 0
errors = 0

for slug, info, has_baca, link_count in missing_articles:
    # Skip articles that already have "Baca juga" even if links < 2
    # They have some form of cross-linking structure
    if has_baca:
        continue
    
    related = find_related(slug, info, 3)
    if not related:
        errors += 1
        print(f"  ⚠️ {slug}: no related articles found in category '{info['category']}'")
        continue
    
    new_body = add_baca_juga(slug, info, related)
    if new_body is None:
        errors += 1
        continue
    
    # Reconstruct the file
    new_raw = info['parts'][0] + '---' + info['parts'][1] + '---' + new_body
    
    # Verify we added links
    new_links = link_pattern.findall(new_body)
    if len(new_links) <= link_count:
        errors += 1
        print(f"  ❌ {slug}: links didn't increase ({link_count} -> {len(new_links)})")
        continue
    
    # Write back
    with open(info['path'], 'w', encoding='utf-8') as fh:
        fh.write(new_raw)
    
    related_titles = [all_articles[r]['title'][:50] for r in related]
    print(f"  ✅ {slug}: {link_count} -> {len(new_links)} links (related: {', '.join(related_titles)})")
    changes += 1

print(f"\n{'='*60}")
print(f"Changes made: {changes}")
print(f"Errors/skipped: {errors}")
print(f"Skipped (already has Baca): {sum(1 for _,_,b,_ in missing_articles if b)}")
print(f"{'='*60}")
