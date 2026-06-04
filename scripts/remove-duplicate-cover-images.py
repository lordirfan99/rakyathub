#!/usr/bin/env python3
"""Remove duplicate cover images from blog post body content."""
import yaml, re, glob

POST_DIR = "C:/Users/irfan/rakyathub/src/data/post"

for fp in sorted(glob.glob(f"{POST_DIR}/*.md")):
    fname = fp.split(chr(92))[-1]  # backslash split
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # Parse frontmatter
    if not c.startswith('---\n'):
        continue
    end = c.find('\n---\n', 4)
    if end == -1:
        continue

    fm = yaml.safe_load(c[4:end])
    cover = fm.get('image')
    if not cover:
        continue

    body = c[end+5:]
    old_body = body
    escaped_url = re.escape(cover)

    # Remove first markdown image with same URL: ![alt](url)
    body = re.sub(
        rf'!\[.*?\]\({escaped_url}\)\s*\n?',
        '',
        body,
        count=1
    )

    # Remove HTML img with same src
    body = re.sub(
        rf'<img[^>]*src=[\'"]{escaped_url}[\'"][^>]*>\s*\n?',
        '',
        body,
        count=1
    )

    if body == old_body:
        print(f"  SKIP: {fname}")
        continue

    new_c = c[:end+5] + body
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_c)
    print(f"  FIXED: {fname} (removed duplicate)")

print("Done!")
