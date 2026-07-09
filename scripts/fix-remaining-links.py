#!/usr/bin/env python3
"""Fix remaining 15 articles that still have <2 internal links."""
import re, os, glob, random

POST_DIR = 'src/data/post'
link_pattern = re.compile(r'\]\(/(?!https?://)[^)]+/\)')

# Load all articles to find related ones
all_articles = {}
category_index = {}

for f in glob.glob(f'{POST_DIR}/*.md'):
    slug = os.path.splitext(os.path.basename(f))[0]
    with open(f, encoding='utf-8') as fh:
        raw = fh.read()
    parts = raw.split('---', 2)
    if len(parts) < 3:
        continue
    fm = parts[1]
    body = parts[2]
    
    title_m = re.search(r'^title:\s*"(.+)"', fm, re.MULTILINE)
    cat_m = re.search(r'^category:\s*(.+)', fm, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else slug
    category = cat_m.group(1).strip().strip('"') if cat_m else 'Lain-lain'
    
    all_articles[slug] = {'title': title, 'category': category, 'body': body, 'raw': raw, 'parts': parts, 'path': f}
    category_index.setdefault(category, []).append(slug)

random.seed(42)

slugs = ['baucar-kita-selangor-2026-mohon-rm600','bnpl-rm4-9-bilion-hutang-belia-malaysia','cara-cari-sumber-rujukan-ilmiah-untuk-assignment','cara-daftar-sijil-halal-jakim-online-2026','cara-mohon-skim-perubatan-madani-peka-b40-2026','cara-pembahagian-gaji-bulanan-50-30-20-malaysia','cara-tuntut-insurans-motosikal-kemalangan','panduan-budget-bulanan-anak-muda-malaysia-2026','panduan-cari-internship-latihan-industri-malaysia-2026','panduan-cukai-pendapatan-sewa-rumah-malaysia-2026','platform-belajar-online-percuma-malaysia-2026','ringgit-melemah-impak-belanja-anak-muda','side-hustle-content-creator-ugc-malaysia-2026','subsidi-minyak-cecah-rm7-5-bilion','tutor-online-side-hustle-malaysia-2026']

changes = 0
for slug in slugs:
    if slug not in all_articles:
        continue
    info = all_articles[slug]
    body = info['body']
    existing_links = link_pattern.findall(body)
    existing_count = len(existing_links)
    
    if existing_count >= 2:
        continue
    
    needed = 3 - existing_count  # Add enough to reach 3 total, or at least 2
    if needed < 1:
        needed = 1
    
    # Find related articles from same category
    candidates = [s for s in category_index.get(info['category'], []) if s != slug]
    # Remove already-linked
    linked_slugs = set()
    for link in existing_links:
        m = re.search(r'\]\(/([^)/]+)/', link)
        if m:
            linked_slugs.add(m.group(1))
    candidates = [s for s in candidates if s not in linked_slugs]
    
    random.shuffle(candidates)
    to_link = candidates[:needed]
    if not to_link:
        # Fallback to random articles
        to_link = [s for s in all_articles if s != slug and s not in linked_slugs][:needed]
    
    if not to_link:
        print(f'  ⚠️ {slug}: no related articles found')
        continue
    
    # Build Baca juga markdown
    baca_links = []
    for ls in to_link:
        anchor = all_articles[ls]['title'][:60]
        baca_links.append(f"- [{anchor}](/{ls}/)")
    
    baca_md = "\n**Baca juga:**\n" + "\n".join(baca_links) + "\n"
    
    # Insert before Rujukan section or at end
    rujukan_match = re.search(r'\n## (?:Rujukan|Sumber|Rujukan Rasmi|📚|Kredit Gambar)', body)
    if rujukan_match:
        insert_pos = rujukan_match.start()
        new_body = body[:insert_pos] + baca_md + '\n' + body[insert_pos:]
    elif body.rstrip().endswith('---'):
        # Before trailing --- if present
        body = body.rstrip()
        if body.endswith('---'):
            new_body = body[:-3].rstrip() + '\n\n' + baca_md + '\n---'
        else:
            new_body = body + '\n\n' + baca_md
    else:
        new_body = body.rstrip() + '\n\n' + baca_md
    
    # Verify
    new_links = link_pattern.findall(new_body)
    if len(new_links) <= existing_count:
        print(f'  ❌ {slug}: links not increased ({existing_count} -> {len(new_links)})')
        continue
    
    # Reconstruct
    new_raw = info['parts'][0] + '---' + info['parts'][1] + '---' + new_body
    with open(info['path'], 'w', encoding='utf-8') as fh:
        fh.write(new_raw)
    
    linked_titles = [all_articles[ls]['title'][:50] for ls in to_link]
    print(f'  ✅ {slug}: {existing_count} -> {len(new_links)} links ({", ".join(linked_titles)})')
    changes += 1

print(f'\nFixed: {changes} articles')
