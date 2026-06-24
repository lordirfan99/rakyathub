#!/usr/bin/env python3
"""Map our card IDs to DuitGain card images and download them."""
import urllib.request, json, re, os, time, sys

REPO = os.path.expanduser('~/rakyathub')
CARD_DATA = os.path.join(REPO, 'src/data/cashback-cards.json')
IMG_DIR = os.path.join(REPO, 'public/images/cards')

os.makedirs(IMG_DIR, exist_ok=True)

with open(CARD_DATA) as f:
    data = json.load(f)

# DuitGain slug → image URL mapping (verified working)
DUITGAIN_MAP = {
    # AEON
    "aeon-biker-gold": "aeon-biker-gold-visa-card",
    "aeon-biker-infinite": "aeon-biker-infinite-visa-card",
    # AFFIN
    "affin-bhpetrol": "affin-bhpetrol-mastercard",
    "affin-duo": "affin-duo-visa-cash-back",
    "affin-duo-plus": "affin-duo-visa-cash-back",
    "affin-duoi": "affin-duo-visa-cash-back",
    "affin-duo-plus-i": "affin-duo-visa-cash-back",
    # Alliance
    "alliance-vsig": "alliance-bank-visa-signature",
    # Alrajhi
    "alrajhi-platinum": "alrajhi-bank-visa-platinum",
    "alrajhi-sig": "alrajhi-bank-visa-signature",
    # AmBank
    "ambank-cash-rebate": "ambank-cash-rebate-visa-platinum-card",
    # Bank Islam
    "bank-islam-gold": "bank-islam-visa-gold-credit-card-i",
    "bank-islam-platinum": "bank-islam-visa-platinum-credit-card-i",
    "bank-islam-infinite": "bank-islam-visa-infinite-credit-card-i",
    # BSN
    "bsn-cash-rebate": "bsn-visa-cash-back-credit-card",
    # CIMB
    "cimb-cash-rebate": "cimb-cash-rebate-platinum-credit-card",
    "cimb-petronas-platinum": "cimb-petronas-visa-platinum-i-credit-card",
    "cimb-petronas-infinite": "cimb-petronas-visa-infinite-i-credit-card",
    # HLB
    "hlb-essential": "hlb-essential-card",
    "hlb-wise": "hlb-wise-card",
    # HSBC
    "hsbc-mpower": "hsbc-amanah-mpower-platinum-credit-card-i",
    "hsbc-live-plus": "hsbc-live-credit-card",
    # Maybank
    "maybank-2-gold": "maybank-2-gold-cards-amex",
    "maybank-2-platinum": "maybank-2-platinum-cards-amex",
    "maybank-amex-cb-gold": "maybank-american-express-cash-back-gold-credit-card",
    "maybank-fcbarca": "maybank-fc-barcelona-visa-signature-card",
    "maybank-myimpact": "maybank-myimpact-visa-signature-credit-card",
    "maybank-vsig": "maybank-visa-signature",
    "maybank-islamic-ikhwan-amex": "maybank-islamic-ikhwan-american-express-platinum-card-i",
    "maybank-islamic-ikhwan-mc": "maybank-islamic-ikhwan-mastercard-platinum-card-i",
    # OCBC
    "ocbc-ge": "ocbc-great-eastern-platinum-mastercard",
    "ocbc-world": "ocbc-world-mastercard",
    # Public Bank
    "pb-quantum-mc": "pb-quantum-mastercard",
    "pb-quantum-visa": "pb-quantum-visa-card",
    "pb-visa-sig": "pb-visa-signature-credit-card",
    "pb-visa-infinite": "pb-visa-infinite-credit-card",
    # RHB
    "rhb-cashback": "rhb-visa-cash-back-credit-card",
    "rhb-shell": "rhb-shell-visa-credit-card",
    "rhb-vsig": "rhb-visa-signature",
    "rhb-world-mc": "rhb-world-mastercard-credit-card",
    # StanChart
    "sc-simply-cash": "standard-chartered-simply-cash-credit-card",
    # UOB
    "uob-evol": "uob-evol-card",
    "uob-one-platinum": "uob-one-platinum-card",
    # Bank Rakyat
    "bank-rakyat-cikgu-sejati": "bank-rakyat-cikgu-sejati-credit-card-i",
    "bank-rakyat-world-mc": "bank-rakyat-world-mastercard-credit-card-i",
}

def find_duitgain_image(duitgain_slug):
    """Scrape DuitGain page to find the actual card image URL."""
    url = f"https://duitgain.com/credit_cards/{duitgain_slug}/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        imgs = re.findall(r'src="([^"]+\.(?:png|jpg|jpeg|webp))"', html)
        for i in imgs:
            if ('150x150' not in i and 'logo' not in i and 'icon' not in i 
                and 'removebg' not in i and 'jquery' not in i and 'uploads' in i):
                return i
    except:
        pass
    return None

# Step 1: Find all image URLs
print("=== Step 1: Finding card images on DuitGain ===")
found = 0
for card in data["cards"]:
    cid = card["id"]
    if cid in DUITGAIN_MAP:
        img_url = find_duitgain_image(DUITGAIN_MAP[cid])
        if img_url:
            # Download image
            ext = os.path.splitext(img_url.split('/')[-1])[1] or '.png'
            local_name = f"{cid}{ext}"
            local_path = os.path.join(IMG_DIR, local_name)
            
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=15)
                with open(local_path, 'wb') as f:
                    f.write(resp.read())
                # Store local URL 
                card["imageUrl"] = f"/images/cards/{local_name}"
                found += 1
                print(f"✅ {cid[:30]:30s} → downloaded {local_name}")
            except Exception as e:
                print(f"⚠️ {cid[:30]:30s} → download failed: {e}")
                # Store duitgain URL as fallback
                card["imageUrl"] = img_url
        else:
            print(f"❌ {cid[:30]:30s} → no image on DuitGain")
    time.sleep(0.5)

# Step 2: Save updated card data
with open(CARD_DATA, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n=== Done! Downloaded {found} card images ===")
print(f"Images saved to: {IMG_DIR}")
print(f"Card data updated: {CARD_DATA}")
