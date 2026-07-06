#!/usr/bin/env python3
"""Regenerate all missing hero-{slug}.jpg files using the gradient banner generator."""
import os, glob, re, sys, importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
POSTS_DIR = os.path.join(PROJECT_ROOT, 'src', 'data', 'post')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images')

# Import generate-hero-banner
SPEC = importlib.util.spec_from_file_location(
    "generate_hero_banner",
    os.path.join(SCRIPT_DIR, "generate-hero-banner.py")
)
ghb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ghb)
build_banner = ghb.build_banner
ghb.fetch_pollinations_bg = lambda prompt: None  # Skip Pollinations, use Pillow only

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

to_gen = []
for md_file in sorted(glob.glob(os.path.join(POSTS_DIR, '*.md'))):
    slug = os.path.splitext(os.path.basename(md_file))[0]
    expected = f'hero-{slug}.jpg'
    img_path = os.path.join(IMAGES_DIR, expected)
    
    if os.path.exists(img_path):
        continue  # Already exists
    
    with open(md_file, encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'^image:\s*"(.*?)"', content, re.MULTILINE)
    if not m:
        continue
    ref = os.path.basename(m.group(1))
    if ref != expected:
        continue  # Skip - frontmatter not yet updated (unlikely)
    
    m2 = re.search(r'^title:\s*(.*)', content, re.MULTILINE)
    title = m2.group(1).strip().strip('"').strip("'") if m2 else slug
    m3 = re.search(r'^category:\s*(.*)', content, re.MULTILINE)
    cat = m3.group(1).strip().strip('"').strip("'") if m3 else 'default'
    banner_cat = map_category(cat, slug)
    to_gen.append((slug, title, banner_cat))

if not to_gen:
    print("No missing images!")
    sys.exit(0)

print(f"Regenerating {len(to_gen)} missing banners...\n")

gen = 0
fail = 0
for slug, title, cat in to_gen:
    try:
        out_path = build_banner(slug, title, cat)
        kb = os.path.getsize(out_path) / 1024
        print(f"  ✅ {slug}  ({kb:.0f}KB)  [{cat}]")
        gen += 1
    except Exception as e:
        print(f"  ❌ {slug}  {e}")
        fail += 1

print(f"\nDone: {gen} generated, {fail} failed")
