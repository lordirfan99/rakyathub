#!/usr/bin/env python3
"""Global URL lockdown script — purges all legacy rakyathub.com and external app links"""
import os, re, sys

POST_DIR = 'src/data/post'
NAV_FILE = 'src/navigation.ts'
CONFIG_FILE = 'src/config.yaml'
INDEX_FILE = 'src/pages/index.astro'
BLOG_INDEX = 'src/pages/[...blog]/index.astro'
HUbUNGI = 'src/pages/hubungi.astro'
PRIVASI = 'src/pages/privasi.astro'

# Mapping of legacy external tool domains → internal calculator routes
TOOL_MAP = {
    r'https://keretakalkulator\.netlify\.app\b': '/kalkulator/kereta/',
    r'https://kwsp\.netlify\.app\b': '/kalkulator/kwsp/',
    r'https://emasrakyathub\.netlify\.app\b': '/kalkulator/emas/',
    r'https://loanrumah\.rakyathub\.online\b': '/kalkulator/loan-rumah/',
    r'https://loanrumah-rakyathub\.netlify\.app\b': '/kalkulator/loan-rumah/',
    r'https://app\.rakyathub\.online\b': '/',
    r'https://kwsp\.rakyathub\.online\b': '/kalkulator/kwsp/',
}

# Known broken blog slugs (from rakyathub.com URLs) → corrected clean slugs
SLUG_MAP = {
    '/kwsp/': '/blog/',
    '/kwsp': '/blog/',
    '/asb-2/': '/blog/',
    '/asb-2': '/blog/',
    '/asb/': '/blog/',
    '/asb': '/blog/',
    '/emas/': '/blog/',
    '/emas': '/blog/',
    '/str/': '/blog/',
    '/str': '/blog/',
    '/7-kelebihan-simpanan-asb-pelaburan-bijak-pulangan-konsisten-yang-pasti-korang-tak-tahu/': '/7-kelebihan-simpanan-asb-pelaburan-bijak-pulangan-konsisten-yang-pasti-korang-tak-tahu/',
}

def fix_internal_links(content):
    """Replace https://rakyathub.com/XXX with relative paths"""
    # First handle known slug patterns
    for old_slug, new_slug in SLUG_MAP.items():
        content = content.replace(f'https://rakyathub.com{old_slug}', new_slug)
    
    # Generic: https://rakyathub.com/anything → /anything
    content = re.sub(
        r'https://rakyathub\.com(/[^\s)\]\'">]*)?',
        lambda m: m.group(1) if m.group(1) else '/',
        content
    )
    
    # Fix articles/investment-strategy → doesn't exist, point to blog
    content = content.replace('/articles/investment-strategy', '/blog/')
    
    # Fix kalkulator-ansuran-kereta → point to our kereta calculator
    content = content.replace(
        'https://rakyathub.com/kalkulator-ansuran-kereta-bulanan-malaysia-2025-rakyathub/',
        '/kalkulator/kereta/'
    )
    
    # Replace external tool links
    for pattern, replacement in TOOL_MAP.items():
        content = re.sub(pattern, replacement, content)
    
    return content


def fix_image_urls(content):
    """Handle broken wp-content image URLs from old WordPress site"""
    # Replace wp-content image URLs with a placeholder or remove
    content = re.sub(
        r'https://rakyathub\.com/wp-content/uploads/\d+/\d+/[^\s)\]]+',
        '/_astro/default.CZ816Hke_Z20CwEO.jpg',
        content
    )
    return content


def fix_email(content):
    return content.replace('hello@rakyathub.com', 'hello@rakyathub.netlify.app')


def fix_frontmatter_image(content):
    """Fix image: field in frontmatter"""
    return re.sub(r'^image:\s*https://rakyathub\.com/wp-content/uploads/\d+/\d+/.+$', 
                  'image: /_astro/default.CZ816Hke_Z20CwEO.jpg', 
                  content, flags=re.MULTILINE)


def process_file(filepath, fixers):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for fixer in fixers:
        content = fixer(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


changed = []

# 1. Fix all markdown blog posts
for fname in os.listdir(POST_DIR):
    if fname.endswith('.md'):
        fpath = os.path.join(POST_DIR, fname)
        if process_file(fpath, [fix_frontmatter_image, fix_image_urls, fix_internal_links]):
            changed.append(f'post/{fname}')
            print(f'  FIXED: {fpath}')

# 2. Fix navigation.ts
if process_file(NAV_FILE, [
    lambda c: c.replace("'https://rakyathub.com'", "'/'"),
    lambda c: c.replace('"https://rakyathub.com"', '"/"'),
    lambda c: c.replace('https://rakyathub.com/favicon.ico', '/favicon.ico'),
    fix_email,
]):
    changed.append(NAV_FILE)
    print(f'  FIXED: {NAV_FILE}')

# 3. Fix config.yaml
if process_file(CONFIG_FILE, [
    lambda c: c.replace("site: 'https://rakyathub.com'", "site: 'https://rakyathub.netlify.app'"),
]):
    changed.append(CONFIG_FILE)
    print(f'  FIXED: {CONFIG_FILE}')

# 4. Fix index.astro (JSON-LD org schema)
if process_file(INDEX_FILE, []):
    # Only email fix needed
    pass

# 5. Fix blog index
if process_file(BLOG_INDEX, []):
    pass

# 6. Fix hubungi + privasi emails
for f in [HUbUNGI, PRIVASI]:
    if process_file(f, [fix_email]):
        changed.append(f)
        print(f'  FIXED: {f}')

print(f'\n=== Total files modified: {len(changed)} ===')
for f in changed:
    print(f'  • {f}')
