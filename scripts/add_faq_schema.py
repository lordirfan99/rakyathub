#!/usr/bin/env python3
"""
Scan posts with "Soalan Lazim" sections, extract Q&A pairs,
and insert faq: frontmatter. Run: python3 scripts/add_faq_schema.py
"""
import os, re, json, shutil

POST_DIR = os.path.expanduser('~/rakyathub/src/data/post')
BACKUP_DIR = os.path.expanduser('~/rakyathub/src/data/post_backup_faq')

os.makedirs(BACKUP_DIR, exist_ok=True)

# Priority: process these first (all have numbered FAQ sections)
# Full list of 55, we'll process in order of importance
ALL_POSTS = [
    # === TOP PRIORITY: High-traffic evergreen ===
    'cara-kira-gaji-bersih-panduan-potongan-kwsp-perkeso-pcb.md',
    '7-side-hustle-paling-laku-malaysia-2026.md',
    '7-pekerjaan-paling-laris-2026-malaysia.md',
    'beli-rumah-vs-sewa-rumah-mana-lebih-untung-anak-muda.md',
    'cara-beli-emas-public-gold.md',
    'cara-mula-melabur-saham-bursa-malaysia-panduan-pemula-2026.md',
    'bonus-asb-cara-kira-dan-beza-dengan-dividen.md',
    'asb-2-panduan-lengkap-simpanan-berkala-2026.md',
    'kwsp-akaun-1-2-3-panduan-lengkap-simpanan-sejahtera-fleksibel.md',
    'kwsp-pengeluaran-perumahan-akaun-2-beli-rumah-2026.md',
    'kerja-kerajaan-vs-swasta-2026-perbandingan-gaji-pencen.md',
    'kerja-remote-hibrid-malaysia-2026.md',
    'cara-mohon-rumah-pr1ma-2026-syarat-kelayakan.md',
    'cara-kira-dividen-kwsp-metode-madb-strategi-pulangan.md',
    'bisnes-makanan-frozen-dari-rumah-2026.md',
    # === SECOND PRIORITY ===
    'dca-emas-gap-public-gold-strategi-beli-konsisten.md',
    'bisnes-bundle-preloved-online-2026.md',
    'bisnes-produk-digital-ai-side-hustle-malaysia-2026.md',
    'panduan-bayar-ptptn-2026-diskaun-insentif.md',
    'panduan-insurans-kereta-malaysia-first-time-owner.md',
    'insurans-hayat-vs-insurans-perubatan-beza-mana-sesuai.md',
    'medical-card-standalone-vs-rider-ilp-mana-paling-jimat-2026.md',
    'panduan-tabung-haji-2026-cara-simpan-daftar-haji.md',
    'panduan-sspn-2026-simpanan-pendidikan-pelepasan-cukai.md',
    'pajak-gadai-emas-ar-rahnu-panduan-kira-upah-simpan.md',
    'panduan-lengkap-tukar-kerjaya-malaysia-2026.md',
    'urus-duit-gaji-bawah-rm3000.md',
    'cara-urus-duit-rumah-tangga-pasangan-suami-isteri.md',
    'base-mhit-plan-insurans-kerajaan-2026.md',
    'inflasi-perubatan-malaysia-kenapa-premium-medical-card-naik.md',
    'sara-2026-sumbangan-asas-rahmah-panduan-lengkap.md',
    '📘-cara-elak-scam-pinjaman-online-panduan-lengkap-tips-selamat.md',
    '📉-info-bantuan-rm100-mykad-subsidi-ron95-kemas-kini-rakyathub.md',
    '💼-adakah-freelancer-boleh-carum-kwsp-sendiri.md',
    'medical-card-vs-critical-illness-beza-perlukan.md',
    'harga-emas-cecah-rm764-6-platform-pelaburan-terbaik-2026.md',
    'industri-paling-prospek-malaysia-2026.md',
    'versa-vs-kdi-vs-tng-go-platform-simpanan-alternatif-2026.md',
    'pelan-perlindungan-ikut-tahap-umur-insurans-takaful.md',
    'insurans-perjalanan-malaysia-panduan-lengkap-2026.md',
    'pekerjaan-high-demand-malaysia-2026.md',
    'prs-skim-persaraan-swasta-panduan-lengkap-2026.md',
    'premium-insurans-perubatan-naik-2026-alternatif-mhit.md',
    'persediaan-kewangan-ibu-bapa-baru-malaysia.md',
    'panduan-lengkap-berpindah-rumah-checklist.md',
    '❓-pelaburan-asas-asb-kwsp-dca-apa-pilihan-terbaik-untuk-rakyat-malaysia.md',
    # Also include the tips temuduga one (different pattern: ### 7 Soalan Lazim Temuduga)
    'tips-temuduga-kerja-fresh-graduate-malaysia.md',
    '💰7-kelebihan-simpanan-asb-pelaburan-bijak-pulangan-konsisten-yang-pasti-korang-tak-tahu.md',
]

def parse_faq_section(lines, start_idx):
    """Parse numbered FAQ items from the section.
    Format: ### N. Question? / Answer paragraph(s)
    Returns list of {question, answer} and end index.
    """
    faqs = []
    i = start_idx
    while i < len(lines):
        line = lines[i]
        # Look for ### N. Question? pattern
        m = re.match(r'^###\s+\d+[\.\)]\s+(.+)$', line.strip())
        if not m:
            # Also match ### 7 Soalan Lazim Temuduga without number
            m = re.match(r'^###\s+(.+\?)$', line.strip())
        if m:
            question = m.group(1).strip()
            # Collect answer: everything until next ### or ## or end
            i += 1
            answer_parts = []
            while i < len(lines):
                next_line = lines[i].strip()
                if re.match(r'^###\s+\d+[\.\)]', next_line) or next_line.startswith('## ') or next_line.startswith('---'):
                    break
                if next_line.strip():
                    answer_parts.append(next_line.strip())
                i += 1
            answer = ' '.join(answer_parts)
            # Clean up markdown bold/links for answer (keep text readable)
            answer = re.sub(r'\*\*([^*]+)\*\*', r'\1', answer)
            if question and answer:
                faqs.append({'question': question, 'answer': answer})
            continue
        # Stop at next ## heading or --- or end
        if line.strip().startswith('## ') or line.strip().startswith('---') or line.strip().startswith('### Tips'):
            i += 1
            continue
        i += 1

    return faqs

def update_post(filepath, faqs):
    """Add faq: frontmatter to a post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if faq already exists in frontmatter
    if 'faq:' in content.split('---')[1] if content.startswith('---') else '':
        # Split correctly
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if 'faq:' in fm:
                print(f"  SKIP: faq already in frontmatter")
                return False

    # Find the end of frontmatter (---) and insert faq before the closing ---
    if not content.startswith('---'):
        print(f"  SKIP: no frontmatter found")
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  SKIP: malformed frontmatter")
        return False

    before = parts[0]  # empty
    frontmatter = parts[1]
    after = parts[2]

    # Build YAML faq block with proper indentation
    faq_yaml_lines = ['faq:']
    for item in faqs:
        q_escaped = item['question'].replace('"', '\\"')
        a_escaped = item['answer'].replace('"', '\\"')
        faq_yaml_lines.append(f'  - question: "{q_escaped}"')
        faq_yaml_lines.append(f'    answer: "{a_escaped}"')

    faq_yaml = '\n' + '\n'.join(faq_yaml_lines)

    # Insert before the closing ---
    new_frontmatter = frontmatter.rstrip() + faq_yaml + '\n'
    new_content = '---' + new_frontmatter + '---' + after

    # Backup original
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(filepath))
    shutil.copy2(filepath, backup_path)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Added {len(faqs)} FAQ items")
    return True


def process_posts(post_list):
    """Process all posts in the list."""
    processed = 0
    skipped = 0
    errors = 0

    for fname in post_list:
        filepath = os.path.join(POST_DIR, fname)
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {fname}")
            errors += 1
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the FAQ section start
        faq_start = None
        for i, line in enumerate(lines):
            if re.match(r'^##\s*[❓]?\s*Soalan Lazim', line.strip()):
                faq_start = i
                break

        if faq_start is None:
            print(f"  SKIP: no Soalan Lazim section: {fname}")
            skipped += 1
            continue

        # Parse FAQ items
        faqs = parse_faq_section(lines, faq_start + 1)
        if not faqs:
            print(f"  SKIP: no FAQ items parsed: {fname}")
            skipped += 1
            continue

        print(f"\n{fname}: {len(faqs)} item(s)")
        for item in faqs:
            print(f"    Q: {item['question'][:80]}...")

        if update_post(filepath, faqs):
            processed += 1
        else:
            skipped += 1

    return processed, skipped, errors


if __name__ == '__main__':
    print("=" * 60)
    print("Adding FAQPage schema frontmatter to RakyatHub posts")
    print("=" * 60)
    
    p, s, e = process_posts(ALL_POSTS)
    print(f"\n{'='*60}")
    print(f"Done: {p} processed, {s} skipped, {e} errors")
    print(f"Backups saved to {BACKUP_DIR}")
    print(f"{'='*60}")
    print("\nRun 'npm run build' to verify after review.")
