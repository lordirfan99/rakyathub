#!/usr/bin/env python3
"""Update frontmatter image references and delete old stock files."""
import os, glob, re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(PROJECT_ROOT, 'src', 'data', 'post')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images')

# Build mapping of slug -> old image filename
fm_updates = []
old_files_to_delete = set()

for md_file in sorted(glob.glob(os.path.join(POSTS_DIR, '*.md'))):
    slug = os.path.splitext(os.path.basename(md_file))[0]
    expected = f"hero-{slug}.jpg"
    
    with open(md_file, encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'^image:\s*"(.*?)"', content, re.MULTILINE)
    if not m:
        continue
    old_fname = os.path.basename(m.group(1))
    
    if old_fname == expected:
        continue  # Already correct
    
    # Update frontmatter
    old_line = m.group(0)
    new_line = f'image: "~/assets/images/{expected}"'
    new_content = content.replace(old_line, new_line, 1)
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    fm_updates.append((slug, old_fname, expected))
    
    # Mark old file for deletion if it exists and is not the new file
    old_path = os.path.join(IMAGES_DIR, old_fname)
    new_path = os.path.join(IMAGES_DIR, expected)
    if old_fname != expected and os.path.exists(old_path):
        old_files_to_delete.add(old_path)

print(f"=== Frontmatter updates: {len(fm_updates)} ===\n")
for slug, old, new in sorted(fm_updates):
    print(f"  ✅ {slug}")
    print(f"     {old}  →  {new}")

print(f"\n=== Delete old stock files: {len(old_files_to_delete)} ===\n")
for fp in sorted(old_files_to_delete):
    mb = os.path.getsize(fp) / (1024*1024)
    os.remove(fp)
    print(f"  🗑️  DELETED  {mb:.1f}MB  {os.path.basename(fp)}")

print(f"\nDone! {len(fm_updates)} frontmatter updated, {len(old_files_to_delete)} old files deleted.")
