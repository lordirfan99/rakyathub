#!/usr/bin/env python3
"""Scrape card images from DuitGain for the new TypeScript-based card database.
Downloads images to public/images/cards/ and prints the IMAGE_MAP entries for cashback-combo.astro."""

import urllib.request, json, re, os, time, sys

REPO = os.path.expanduser('~/rakyathub')
IMG_DIR = os.path.join(REPO, 'public/images/cards')
os.makedirs(IMG_DIR, exist_ok=True)

# ── New TS card ID → DuitGain slug mapping ──
# These are the 52 cards from cashback-cards.ts
# Some reuse old slugs, some need new ones (guessed from card name patterns)
DUITGAIN_MAP = {
    # Maybank
    "maybank-2-cards": "maybank-2-gold-cards-amex",
    "maybank-visa-signature": "maybank-visa-signature",
    "maybank-2-card-amex": "maybank-2-cards-amex",
    "maybank-fc-barcelona": "maybank-fc-barcelona-visa-signature-card",
    "maybank-lazada": "maybank-lazada-visa-credit-card",
    "maybank-shopee": "maybank-shopee-mastercard-credit-card",

    # CIMB
    "cimb-cash-rebate-platinum": "cimb-cash-rebate-platinum-credit-card",
    "cimb-cashback-gold": "cimb-cash-rebate-gold-credit-card",
    "cimb-petronas-visa": "cimb-petronas-visa-platinum-i-credit-card",
    "cimb-preferred-visa-infinite": "cimb-preferred-visa-infinite-credit-card",
    "cimb-shopee": "cimb-shopee-visa-credit-card",
    "cimb-utama": "cimb-utama-visa-credit-card",

    # Public Bank
    "pb-quantum-visa": "pb-quantum-visa-card",
    "pb-quantum-mc": "pb-quantum-mastercard",
    "pb-visa-signature": "pb-visa-signature-credit-card",
    "pb-petronas-mc": "pb-petronas-mastercard-credit-card",
    "pb-petron-visa": "pb-petron-visa-credit-card",

    # Hong Leong
    "hlb-wise-gold": "hlb-wise-card",
    "hlb-visa-platinum": "hlb-visa-platinum-cashback-credit-card",
    "hlb-golf-visa": "hlb-golf-business-mastercard",
    "hlb-eon-cashback": "hlb-eon-cashback-visa-credit-card",

    # RHB
    "rhb-cashback": "rhb-visa-cash-back-credit-card",
    "rhb-smart-value": "rhb-smart-value-credit-card",
    "rhb-visa-infinite": "rhb-visa-infinite-credit-card",
    "rhb-pharmacy": "rhb-health-wellness-credit-card",

    # AmBank
    "ambank-true-cashback": "ambank-true-cashback-visa-credit-card",
    "ambank-cashback-platinum": "ambank-carz-mastercard",
    "ambank-visa-infinite": "ambank-visa-infinite-credit-card",

    # Affin
    "affin-cashback-platinum": "affin-cashback-platinum-credit-card",
    "affin-visa-infinite": "affin-visa-infinite",

    # Alliance
    "alliance-viz-visa": "alliance-bank-viz-visa-credit-card",
    "alliance-weekend-platinum": "alliance-weekend-platinum-credit-card",
    "alliance-bank-visa-infinite": "alliance-bank-visa-infinite-credit-card",

    # BSN
    "bsn-cash-visa": "bsn-visa-cash-back-credit-card",
    "bsn-zing": "bsn-zing-mastercard-credit-card",
    "bsn-mastercard-platinum": "bsn-mastercard-platinum-credit-card",

    # Bank Islam
    "bank-islam-visa": "bank-islam-visa-platinum-credit-card-i",

    # Standard Chartered
    "sc-smart": "standard-chartered-smart-credit-card",
    "sc-platinum-cashback": "standard-chartered-platinum-cashback-credit-card",
    "sc-worldmiles": "standard-chartered-worldmiles-credit-card",
    "sc-jumbo-spend": "standard-chartered-jumpstart-credit-card",

    # UOB
    "uob-cashback-platinum": "uob-cash-rebate-platinum-credit-card",
    "uob-one": "uob-one-platinum-card",
    "uob-visa-infinite": "uob-visa-infinite-credit-card",

    # OCBC
    "ocbc-cashback": "ocbc-cashback-credit-card",
    "ocbc-visa-infinite": "ocbc-visa-infinite-credit-card",

    # Others
    "citi-prestige": "citi-prestige-credit-card",
    "muamalat-cashback": "bank-muamalat-visa-cashback-credit-card",
    "tng-go-visa": "tng-go-visa-credit-card",
    "boost-visa": "boost-visa-infinite-credit-card",
    "gxbank-card": "gxbank-debit-mastercard",
    "aeon-eshop": "aeon-eshop-mastercard",
}


def find_duitgain_image(duitgain_slug):
    """Scrape DuitGain page to find the actual card image URL."""
    url = f"https://duitgain.com/credit_cards/{duitgain_slug}/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        imgs = re.findall(r'src="([^"]+\.(?:png|jpg|jpeg|webp))"', html)
        for i in imgs:
            if ('150x150' not in i and 'logo' not in i and 'icon' not in i
                and 'removebg' not in i and 'jquery' not in i and 'uploads' in i):
                return i
    except Exception as e:
        print(f"    ⚠️  HTTP error: {e}")
    return None


# ── Main ──
print("=" * 60)
print("DuitGain Card Image Scraper v2 (for TypeScript cards)")
print("=" * 60)

new_cards = list(DUITGAIN_MAP.keys())
print(f"\nTotal cards to process: {len(new_cards)}")
print()

image_map_entries = {}
downloaded = 0

for i, cid in enumerate(new_cards, 1):
    slug = DUITGAIN_MAP[cid]
    print(f"[{i:02d}/{len(new_cards)}] {cid[:35]:35s} → {slug}", end="")

    # Check if image already exists
    for ext in ['.png', '.jpg']:
        if os.path.exists(os.path.join(IMG_DIR, f"{cid}{ext}")):
            print(f" ✅ already exists", end="")
            image_map_entries[cid] = f"/images/cards/{cid}{ext}"
            downloaded += 1
            break
    else:
        # Need to scrape
        print(f" ... scraping", end="")
        sys.stdout.flush()
        img_url = find_duitgain_image(slug)
        if img_url:
            ext = os.path.splitext(img_url.split('/')[-1])[1] or '.png'
            local_name = f"{cid}{ext}"
            local_path = os.path.join(IMG_DIR, local_name)
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=15)
                with open(local_path, 'wb') as f:
                    f.write(resp.read())
                image_map_entries[cid] = f"/images/cards/{local_name}"
                downloaded += 1
                print(f" ✅ downloaded {local_name}", end="")
            except Exception as e:
                print(f" ❌ download failed: {e}", end="")
        else:
            print(f" ❌ no image found", end="")

    print()
    time.sleep(0.5)  # Be polite to DuitGain

print(f"\n{'=' * 60}")
print(f"Downloaded/found: {downloaded}/{len(new_cards)}")
print(f"\n{'=' * 60}")
print(f"IMAGE_MAP entries for cashback-combo.astro:")
print(f"{'=' * 60}")
print()

# Print in JavaScript/TypeScript format
for cid in new_cards:
    if cid in image_map_entries:
        print(f"  '{cid}': '{image_map_entries[cid]}',")
    else:
        print(f"  // '{cid}': 'NO IMAGE',")

print(f"\n{'=' * 60}")
print(f"Images saved to: {IMG_DIR}")
print(f"Done!")
