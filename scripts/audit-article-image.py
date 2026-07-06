#!/usr/bin/env python3
"""audit-article-image.py — Check artikel image & auto-suggest replacement.

Usage:
    python3 scripts/audit-article-image.py src/data/post/<slug>.md

Checks:
    1. File size > 1.5MB? → almost certainly stock photo
    2. Duplicate? → same image used by >1 article
    3. Missing file? → frontmatter references non-existent file
    4. Known stock naming pattern? → asian-woman-calc, smiling, etc.
    5. Unused images in pool? → opportunities to reuse existing assets

Exit code:
    0 — all clean
    1 — issues found (stock photo, missing file, etc.)
"""

import os, re, sys, glob

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POSTS_DIR = os.path.join(PROJECT_ROOT, 'src', 'data', 'post')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images')

STOCK_PATTERNS = re.compile(
    r'(asian|smiling|stock|cash|woman.calc|woman.calc|handshake|office.meeting|'
    r'business.people|corporate|happy.worker|diverse|ethnic|'
    r'calculator.money|hijab.woman|asian.man|asian.woman)',
    re.IGNORECASE
)

STOCK_SIZE_MB = 1.5  # > 1.5MB almost certainly stock photo


def load_referenced_images() -> dict[str, list[str]]:
    """Build {filename: [slug, ...]} from all post frontmatter."""
    referenced = {}
    for md_file in glob.glob(os.path.join(POSTS_DIR, '*.md')):
        with open(md_file, encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'^image:\s*"(.*?)"', content, re.MULTILINE)
        if m:
            fname = os.path.basename(m.group(1))
            slug = os.path.splitext(os.path.basename(md_file))[0]
            referenced.setdefault(fname, []).append(slug)
    return referenced


def audit_single(slug: str, image_path: str | None, referenced: dict) -> list[str]:
    """Audit one article's image. Returns list of issue strings."""
    issues = []

    if not image_path:
        issues.append("❌ No image: frontmatter has no `image:` field")
        return issues
    
    if not os.path.exists(image_path):
        issues.append(f"❌ Missing file: '{os.path.basename(image_path)}' referenced but not found on disk")
        return issues

    fname = os.path.basename(image_path)
    size_mb = os.path.getsize(image_path) / (1024 * 1024)
    
    # Check 1: File size (stock photo indicator)
    if size_mb > STOCK_SIZE_MB:
        issues.append(f"🔴 Stock: {fname} ({size_mb:.1f}MB > {STOCK_SIZE_MB:.0f}MB threshold)")
    elif size_mb > 0.5:
        issues.append(f"🟡 Large-ish: {fname} ({size_mb:.1f}MB) — may be stock, check manually")
    else:
        issues.append(f"✅ Size OK: {fname} ({size_mb*1000:.0f}KB)")

    # Check 2: Naming pattern (known stock patterns)
    if STOCK_PATTERNS.search(fname):
        issues.append(f"🔴 Stock pattern: '{fname}' matches known stock naming pattern")
    else:
        issues.append("✅ Name OK: no stock naming pattern detected")

    # Check 3: Duplicate (same image used by multiple articles)
    users = referenced.get(fname, [])
    if len(users) > 1:
        others = [s for s in users if s != slug]
        issues.append(f"🔴 Duplicate: '{fname}' also used by: {', '.join(others)}")
    else:
        issues.append("✅ Unique — 1 article uses this")

    # Check 4: Unused images available
    unused = []
    for img_file in glob.glob(os.path.join(IMAGES_DIR, 'hero-*.jpg')):
        b = os.path.basename(img_file)
        if b not in referenced:
            unused.append(b)
    if unused:
        issues.append(f"⚠️  {len(unused)} unused images available for reuse")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/audit-article-image.py src/data/post/<slug>.md")
        sys.exit(1)

    md_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(md_path):
        print(f"❌ File not found: {md_path}")
        sys.exit(1)

    slug = os.path.splitext(os.path.basename(md_path))[0]

    # Read frontmatter
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    m = re.search(r'^image:\s*"(.*?)"', content, re.MULTILINE)
    image_ref = m.group(1) if m else None

    # Resolve image path
    image_path = None
    if image_ref:
        # Handle ~/assets/images/... → resolve from project root
        if image_ref.startswith('~/assets/images/'):
            fname = os.path.basename(image_ref)
            image_path = os.path.join(IMAGES_DIR, fname)
        elif image_ref.startswith('~/'):
            fname = os.path.basename(image_ref)
            image_path = os.path.join(IMAGES_DIR, fname)
        elif image_ref.startswith('src/'):
            image_path = os.path.join(PROJECT_ROOT, image_ref)
        else:
            # Assume just a filename relative to images dir
            image_path = os.path.join(IMAGES_DIR, os.path.basename(image_ref))

    referenced = load_referenced_images()

    print(f"\n📸 {md_path}")
    print(f"   Slug: {slug}")
    print(f"   Image ref: {image_ref or '(none)'}")

    issues = audit_single(slug, image_path, referenced)

    print()
    for issue in issues:
        print(f"   {issue}")
    
    has_red = any(i.startswith("🔴") or i.startswith("❌") for i in issues)
    if has_red:
        print(f"\n   🔴 ACTION REQUIRED — replace with gradient banner:")
        print(f"      python3 scripts/generate-hero-banner.py \"{slug}\" \"<title>\" --category \"<cat>\"")
        sys.exit(1)
    else:
        print(f"\n   ✅ All clear — no action needed")
        sys.exit(0)


if __name__ == '__main__':
    main()
