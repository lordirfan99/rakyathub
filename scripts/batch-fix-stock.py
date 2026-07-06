#!/usr/bin/env python3
"""Batch audit, delete orphans, and list articles needing replacement."""
import os, glob, re, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(PROJECT_ROOT, 'src', 'data', 'post')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images')
STOCK_SIZE_MB = 1.5
STOCK_PATTERNS = re.compile(
    r'(asian|smiling|stock|cash|woman.calc|handshake|office.meeting|'
    r'business.people|corporate|happy.worker|diverse|ethnic|'
    r'calculator.money|hijab|asian.man|asian.woman)',
    re.IGNORECASE
)

# Load referenced images
referenced = {}
slug_info = {}  # slug -> {title, category, image_file}
for md_file in glob.glob(os.path.join(POSTS_DIR, '*.md')):
    slug = os.path.splitext(os.path.basename(md_file))[0]
    with open(md_file, encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^image:\s*"(.*?)"', content, re.MULTILINE)
    fname = os.path.basename(m.group(1)) if m else None
    if fname:
        referenced.setdefault(fname, []).append(slug)
    m2 = re.search(r'^title:\s*(.*)', content, re.MULTILINE)
    title = m2.group(1).strip().strip('"').strip("'") if m2 else slug
    m3 = re.search(r'^category:\s*(.*)', content, re.MULTILINE)
    cat = m3.group(1).strip().strip('"').strip("'") if m3 else 'default'
    slug_info[slug] = {'title': title, 'category': cat, 'image_file': fname}

CAT_MAP = {
    'keselamatan': 'teknologi', 'scam': 'teknologi', 'teknologi': 'teknologi',
    'kerjaya': 'kerjaya_bisnes', 'bisnes': 'kerjaya_bisnes',
    'pendidikan': 'pendidikan_student', 'student': 'pendidikan_student',
    'hartanah': 'hartanah_sewa',
    'insurans': 'insurans', 'kesihatan': 'umum_kesihatan',
    'kerajaan': 'kerajaan_cukai', 'percukaian': 'kerajaan_cukai', 'kwsp': 'kerajaan_cukai',
    'kewangan': 'default', 'pelaburan': 'default', 'emas': 'default',
    'asb': 'default', 'kenderaan': 'default', 'gaya_hidup': 'gaya_hidup',
}

def map_category(cat, slug):
    banner_cat = CAT_MAP.get(cat.lower(), 'default')
    if any(kw in slug for kw in ['cara', 'mohon', 'daftar', 'bayar', 'check', 'semak', 'beli']):
        banner_cat = 'bof_tutorial'
    return banner_cat

# Phase 1: Delete orphaned stock (>500KB, not referenced)
orphans = []
for img_file in glob.glob(os.path.join(IMAGES_DIR, 'hero-*.jpg')):
    b = os.path.basename(img_file)
    mb = os.path.getsize(img_file) / (1024*1024)
    if b not in referenced and mb > 0.5:
        orphans.append((mb, b, img_file))

print("=== PHASE 1: DELETE ORPHANED STOCK ===")
orphans.sort(reverse=True)
for mb, name, filepath in orphans:
    os.remove(filepath)
    print(f"  DELETED  {mb:.1f}MB  {name}")
print(f"Total: {len(orphans)} deleted\n")

# Phase 2: List articles needing replacement
to_fix = []
missing = []
for slug, info in sorted(slug_info.items()):
    fname = info['image_file']
    if not fname:
        continue
    img_path = os.path.join(IMAGES_DIR, fname)
    if not os.path.exists(img_path):
        missing.append((slug, fname, info))
        continue
    mb = os.path.getsize(img_path) / (1024*1024)
    is_stock_name = bool(STOCK_PATTERNS.search(fname))
    if mb > STOCK_SIZE_MB or is_stock_name:
        banner_cat = map_category(info['category'], slug)
        to_fix.append((mb, slug, fname, info['title'], info['category'], banner_cat))

# Generate bash commands
print("=== PHASE 2: ARTICLES TO REPLACE ===")
print(f"\nMissing: {len(missing)}")
for slug, fname, info in missing:
    bc = map_category(info['category'], slug)
    print(f"  MISSING  {slug}  ->  {fname}")
    print(f"    python3 scripts/generate-hero-banner.py \"{slug}\" \"{info['title']}\" --category \"{bc}\"")

print(f"\nStock: {len(to_fix)}")
to_fix.sort(reverse=True)
for mb, slug, fname, title, cat, bc in to_fix:
    print(f"  {mb:.1f}MB  {slug}  [{bc}]  {title[:50]}")
    print(f"    python3 scripts/generate-hero-banner.py \"{slug}\" \"{title}\" --category \"{bc}\"")

# Check which need frontmatter update (slug != old filename)
print(f"\n=== PHASE 3: FRONTMATTER CHECKS ===")
needs_fm_update = []
for mb, slug, fname, title, cat, bc in to_fix:
    expected = f"hero-{slug}.jpg"
    if fname != expected:
        needs_fm_update.append((slug, fname, expected))
        print(f"  FM UPDATE: {slug}")
        print(f"    old: {fname}")
        print(f"    new: {expected}")

for slug, fname, _ in missing:
    expected = f"hero-{slug}.jpg"
    needs_fm_update.append((slug, fname, expected))
    print(f"  FM UPDATE: {slug} (missing)")
    print(f"    old: {fname}")
    print(f"    new: {expected}")

print(f"\nTotal frontmatter updates needed: {len(needs_fm_update)}")
