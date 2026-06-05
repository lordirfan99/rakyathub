"""
Download all Unsplash hero images for RakyatHub blog posts and
update frontmatter to use local ~/assets/images/ paths.
"""
import os
import re
import urllib.request
import time

POSTS_DIR = r'C:\Users\irfan\rakyathub\src\data\post'
ASSETS_DIR = r'C:\Users\irfan\rakyathub\src\assets\images'

os.makedirs(ASSETS_DIR, exist_ok=True)

# Known local path prefix
LOCAL_PREFIX = '~/assets/images'

# Map by slug -> descriptive filename (keep it simple)
# The rest will use auto-generated names
TOPIC_NAMES = {
    'urus-duit-gaji-bawah-rm3000': 'urus-gaji',
    'cadangan-bajet-50-30-20-di-malaysia': 'bajet',
    'cara-beli-emas-public-gold': 'beli-emas',
    'cara-semak-baki-kwsp-online-tanpa-pergi-kaunter-2025-panduan-lengkap': 'kwsp-online',
    'cara-renew-roadtax-jpj-online-2025-panduan-lengkap': 'roadtax',
    'strategi-dca-vs-lump-sum-pilihan-pelaburan-bijak-untuk-orang-muda': 'dca-vs-lumpsum',
    '7-rahsia-bijak-beli-saham-usa-guna-moomoo-malaysia-panduan-lengkap': 'saham-moomoo',
    '7-kelebihan-simpanan-asb-pelaburan-bijak-pulangan-konsisten-yang-pasti-korang-tak-tahu': 'asb-kelebihan',
    'info-terkini-apa-itu-kwsp-akaun-fleksibel-2025-rakyat-kini-boleh-akses-simpanan-bila-bila-masa': 'kwsp-fleksibel',
    'kereta-sesuai-untuk-fresh-graduate-malaysia-2025-gaji-bajet': 'kereta-fresh-grad',
    'pelaburan-asas-asb-kwsp-dca-apa-pilihan-terbaik-untuk-rakyat-malaysia': 'pelaburan-asas',
    'loan-rumah-calculator-kiraan-ansuran-perancangan-kewangan': 'loan-rumah',
    'risiko-dan-pulangan-robo-advisor-di-malaysia-2025': 'robo-advisor',
    'semakan-saman-jpj-pdrm': 'saman-jpj',
    'carawithdrawkwsp': 'kwsp-withdraw',
    'cukai-jualan-cukai-perkhidmatan-malaysia-2025-barang-dan-servis-yang-akan-terjejas': 'cukai-sst',
    'tebus-bantuan-sara-rm100-guna-ic-pengumuman-pagi-ini-23-julai-2025': 'bantuan-sara',
    'adakah-pinjaman-dari-shopee-boleh-dipercayai-panduan-2025': 'pinjaman-scam',
    'adakah-freelancer-boleh-carum-kwsp-sendiri': 'freelancer-kwsp',
    'cara-elak-scam-pinjaman-online-panduan-lengkap-tips-selamat': 'scam-online',
    'info-bantuan-rm100-mykad-subsidi-ron95-kemas-kini-rakyathub': 'bantuan-rm100',
}

files_fixed = []
files_skipped = []

for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.endswith('.md'):
        continue
    
    fpath = os.path.join(POSTS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already uses local image
    if '~/assets/images/' in content:
        print(f"  ✓ Already local: {fname}")
        continue
    
    # Find Unsplash URL
    m = re.search(r'https://images\.unsplash\.com/photo-([\w-]+)', content)
    if not m:
        print(f"  - No Unsplash: {fname}")
        continue
    
    full_url = m.group(0)
    photo_id = m.group(1)
    
    # Determine image name
    slug = fname.replace('.md', '')
    
    # Clean slug for filename (remove emoji prefixes)
    clean_slug = re.sub(r'^[^\w]+-', '', slug)
    clean_slug = re.sub(r'[^\w-]', '', clean_slug)
    clean_slug = clean_slug.strip('-')
    
    base = TOPIC_NAMES.get(slug, clean_slug)
    if not base.startswith('hero-') and not base.startswith('hero_'):
        base = f'hero-{base}'
    
    img_name = f'{base}.jpg'
    img_path = os.path.join(ASSETS_DIR, img_name)
    
    # Download
    if not os.path.exists(img_path):
        dl_url = f'{full_url}?w=1200&h=630&fit=crop'
        try:
            print(f"  ↓ {img_name}")
            urllib.request.urlretrieve(dl_url, img_path)
            time.sleep(0.3)
            kb = os.path.getsize(img_path) / 1024
            print(f"    {kb:.0f} KB")
        except Exception as e:
            print(f"    ✗ {e}")
            continue
    else:
        print(f"  ✓ Exists: {img_name}")
    
    # Replace URL in content
    local_path = f'{LOCAL_PREFIX}/{img_name}'
    
    # The image line in frontmatter looks like: image: "URL"
    old_line_pattern = re.compile(r'^image:\s*"[^"]*"', re.MULTILINE)
    old_line_match = old_line_pattern.search(content)
    if not old_line_match:
        print(f"  ✗ No image line found")
        continue
    
    old_line = old_line_match.group(0)
    new_line = f'image: "{local_path}"'
    
    new_content = content.replace(old_line, new_line, 1)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    files_fixed.append(fname)
    print(f"    ✅ {fname}")

print(f"\n{'='*50}")
print(f"Fixed: {len(files_fixed)} | Skipped (already local): {len(files_skipped)}")
if files_fixed:
    for f in files_fixed:
        print(f"  • {f}")
