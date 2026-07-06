#!/usr/bin/env python3
"""Batch-generate gradient banners for all articles with stock photos.
Uses Pillow gradient fallback (fast) - no Pollinations calls.
"""
import os, sys, glob, re, importlib.util

# Import generate-hero-banner.py via importlib
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "generate_hero_banner",
    os.path.join(SCRIPT_DIR, "generate-hero-banner.py")
)
ghb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ghb)
build_banner = ghb.build_banner
PALETTES = ghb.PALETTES

# Monkey-patch: skip Pollinations, use Pillow gradient directly
ghb.fetch_pollinations_bg = lambda prompt: None

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
POSTS_DIR = os.path.join(PROJECT_ROOT, 'src', 'data', 'post')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images')
STOCK_SIZE_MB = 1.5
STOCK_PATTERNS = re.compile(
    r'(asian|smiling|stock|cash|woman.calc|handshake|office.meeting|'
    r'business.people|corporate|happy.worker|diverse|ethnic|'
    r'calculator.money|hijab|asian.man|asian.woman)',
    re.IGNORECASE
)

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

# Find all articles needing replacement
to_generate = []
for md_file in sorted(glob.glob(os.path.join(POSTS_DIR, '*.md'))):
    slug = os.path.splitext(os.path.basename(md_file))[0]
    with open(md_file, encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'^image:\s*"(.*?)"', content, re.MULTILINE)
    if not m:
        continue
    fname = os.path.basename(m.group(1))
    img_path = os.path.join(IMAGES_DIR, fname)
    
    skip = False
    if not os.path.exists(img_path):
        skip = False  # Missing - needs generate
    else:
        mb = os.path.getsize(img_path) / (1024*1024)
        is_stock_name = bool(STOCK_PATTERNS.search(fname))
        if mb <= STOCK_SIZE_MB and not is_stock_name:
            skip = True  # Already clean
    
    if skip:
        continue
    
    m2 = re.search(r'^title:\s*(.*)', content, re.MULTILINE)
    title = m2.group(1).strip().strip('"').strip("'") if m2 else slug
    m3 = re.search(r'^category:\s*(.*)', content, re.MULTILINE)
    cat = m3.group(1).strip().strip('"').strip("'") if m3 else 'default'
    banner_cat = map_category(cat, slug)
    to_generate.append((slug, title, banner_cat))
    status = "MISSING" if not os.path.exists(img_path) else "STOCK"
    print(f"  [{status}]  {slug}  ->  [{banner_cat}]")

print(f"\n=== Generating {len(to_generate)} gradient banners (Pillow fast-path) ===\n")

generated = 0
failed = 0
for slug, title, cat in to_generate:
    try:
        out_path = build_banner(slug, title, cat)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  ✅ {slug}  ({size_kb:.0f}KB)  [{cat}]")
        generated += 1
    except Exception as e:
        print(f"  ❌ {slug}  FAILED: {e}")
        failed += 1

print(f"\nDone: {generated} generated, {failed} failed")
