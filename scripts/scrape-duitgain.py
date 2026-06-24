#!/usr/bin/env python3
"""
DuitGain Credit Card Scraper
============================
Scrapes https://duitgain.com/credit_cards/ for Malaysian credit card data.
Outputs a clean JSON file suitable for RakyatHub's credit card directory.

Usage:
    python scripts/scrape-duitgain.py

Requirements:
    pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from urllib.parse import urljoin

BASE_URL = "https://duitgain.com/credit_cards/"
OUTPUT_FILE = "src/data/duitgain-cards.json"
IMG_DIR = "public/images/cards"

# ── Helpers ──────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def safe_text(el, selector, default=""):
    """Extract text from first matching child element."""
    found = el.select_one(selector)
    return found.get_text(strip=True) if found else default


def parse_card_row(row):
    """
    Parse a single card <tr> or card container from DuitGain's listing page.
    Returns a dict with keys: id, bank, name, imageUrl, cashbackRates, annualFee.
    """
    # --- Card name & detail page link ---
    name_el = row.select_one("a[href*='/credit_cards/']")
    if not name_el:
        return None

    card_name = name_el.get_text(strip=True)
    detail_path = name_el.get("href", "")
    detail_url = urljoin(BASE_URL, detail_path)

    # Derive a unique slug from the URL
    slug = detail_path.strip("/").split("/")[-1] if detail_path else ""
    card_id = re.sub(r"[^a-z0-9-]", "", slug.lower())

    # --- Bank name ---
    bank_el = row.select_one(".bank-name, .issuer, td:nth-child(2)")
    bank = bank_el.get_text(strip=True) if bank_el else "Unknown"

    # --- Card image ---
    img_el = row.select_one("img[src*='uploads']")
    img_url = ""
    if img_el:
        src = img_el.get("src", "")
        if src and "150x150" not in src and "logo" not in src.lower():
            img_url = urljoin(BASE_URL, src) if not src.startswith("http") else src

    # --- Cashback / rate summary ---
    rate_el = row.select_one(".cashback-rate, td:nth-child(3)")
    rate_text = rate_el.get_text(strip=True) if rate_el else ""

    # --- Annual fee ---
    fee_el = row.select_one(".annual-fee, td:nth-child(4)")
    fee_text = fee_el.get_text(strip=True) if fee_el else ""

    return {
        "id": card_id or f"card-{int(time.time())}",
        "slug": slug,
        "bank": bank,
        "name": card_name,
        "imageUrl": img_url,
        "detailUrl": detail_url,
        "rateSummary": rate_text,
        "feeText": fee_text,
    }


def download_image(img_url, local_name):
    """Download card image to local directory. Returns local path or empty string."""
    os.makedirs(IMG_DIR, exist_ok=True)
    ext = os.path.splitext(img_url.split("/")[-1])[1] or ".jpg"
    local_path = os.path.join(IMG_DIR, f"{local_name}{ext}")

    if os.path.exists(local_path):
        return f"/images/cards/{local_name}{ext}"  # already exists

    try:
        resp = requests.get(img_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(resp.content)
        print(f"  ✅ Downloaded → {local_name}{ext}")
        return f"/images/cards/{local_name}{ext}"
    except Exception as e:
        print(f"  ⚠️  Download failed: {e}")
        return img_url  # fall back to remote URL


# ── Scrape ───────────────────────────────────────────────────────────────

def scrape_listing():
    """Scrape the main credit cards listing page."""
    print(f"🌐 Fetching {BASE_URL} ...")
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = []

    # DuitGain typically uses a <table> or card grid
    # Try multiple selectors for robustness
    rows = []

    # 1) Try table rows
    table_rows = soup.select("table tbody tr, .card-list .card-item, .credit-card-item")
    if table_rows:
        rows = table_rows
    else:
        # 2) Fallback: find all links containing card names
        for link in soup.select("a[href*='/credit_cards/']"):
            parent = link.find_parent(["div", "li", "tr", "article"])
            if parent:
                rows.append(parent)

    # Deduplicate by detail URL
    seen_urls = set()
    for row in rows:
        card = parse_card_row(row)
        if card and card["detailUrl"] not in seen_urls:
            seen_urls.add(card["detailUrl"])
            cards.append(card)

    print(f"  Found {len(cards)} cards\n")
    return cards


def scrape_detail(card):
    """
    (Optional) Visit each card's detail page for richer data:
    cashback categories, fees, minimum spend, etc.
    """
    if not card.get("detailUrl"):
        return card

    try:
        resp = requests.get(card["detailUrl"], headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # --- Better image (hero/large) ---
        hero_img = soup.select_one(
            "img.card-hero, img.main-card-image, "
            ".card-image img, figure img[src*='uploads']"
        )
        if hero_img:
            src = hero_img.get("src", "")
            if src and "150x150" not in src:
                card["imageUrl"] = urljoin(card["detailUrl"], src)

        # --- Cashback categories ---
        categories = []
        for cat_row in soup.select(".cashback-category tr, .category-item"):
            cat_name = safe_text(cat_row, ".category-name, td:nth-child(1)")
            cat_rate = safe_text(cat_row, ".category-rate, td:nth-child(2)")
            cat_cap = safe_text(cat_row, ".category-cap, td:nth-child(3)")
            if cat_name:
                categories.append({
                    "name": cat_name,
                    "rate": cat_rate,
                    "cap": cat_cap,
                })
        if categories:
            card["categories"] = categories

        # --- Annual fee ---
        fee_detail = soup.select_one(".fee-detail, .annual-fee-value")
        if fee_detail:
            card["annualFeeDetail"] = fee_detail.get_text(strip=True)

        # --- Min income ---
        income_el = soup.select_one(".min-income, .income-requirement")
        if income_el:
            card["minIncome"] = income_el.get_text(strip=True)

    except Exception as e:
        print(f"  ⚠️  Detail scrape failed for {card['id']}: {e}")

    return card


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  DuitGain Credit Card Scraper — for RakyatHub")
    print("=" * 60)

    # Step 1: Scrape listing
    cards = scrape_listing()
    if not cards:
        print("❌ No cards found. DuitGain markup may have changed.")
        return

    # Step 2: Download images
    print("🖼️  Downloading card images ...")
    for i, card in enumerate(cards, 1):
        if card.get("imageUrl"):
            local = download_image(card["imageUrl"], card["id"])
            card["imageLocalUrl"] = local
        print(f"  [{i:02d}/{len(cards)}] {card['bank'][:15]:15s} | {card['name'][:40]:40s}")
        time.sleep(0.3)

    # Step 3: (Optional) Visit detail pages for richer data
    print("\n🔍 Scraping detail pages for richer data ...")
    for i, card in enumerate(cards):
        print(f"  [{i+1:02d}/{len(cards)}] {card['id']}")
        card = scrape_detail(card)
        time.sleep(0.5)

    # Step 4: Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"cards": cards, "count": len(cards)}, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! {len(cards)} cards saved to {OUTPUT_FILE}")
    print(f"   Images saved to {IMG_DIR}/")


if __name__ == "__main__":
    main()
