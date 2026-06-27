#!/usr/bin/env python3
"""
Full DuitGain data scraper — extracts ALL card data via WordPress REST API.
Saves structured JSON to src/data/duitgain/ for integration into RakyatHub.

Usage:  python3 scripts/scrape_duitgain.py
"""
import json, os, sys, urllib.request, time, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "src", "data", "duitgain")
os.makedirs(OUT, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://duitgain.com/wp-json/wp/v2"
DELAY = 0.3  # seconds between pages to be polite

def fetch_url(url, retries=2):
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
                if not raw:
                    raise Exception("Empty response")
                return json.loads(raw)
        except Exception as e:
            if attempt < retries:
                print(f"  ⚠ Retry {attempt+1}/{retries}: {e}", file=sys.stderr)
                time.sleep(1)
            else:
                print(f"  ✗ FAILED: {e}", file=sys.stderr)
    return None

def paginate(endpoint, per_page=50):
    """Fetch all pages of a WP REST API endpoint."""
    results = []
    page = 1
    while True:
        url = f"{API}{endpoint}?per_page={per_page}&page={page}"
        data = fetch_url(url)
        if data is None:
            break
        if not isinstance(data, list) or len(data) == 0:
            break
        results.extend(data)
        if len(data) < per_page:
            break
        page += 1
        time.sleep(DELAY)
        # Show progress
        print(f"    [page {page - 1} → {len(results)} items]", file=sys.stderr)
    return results

def clean_card(card):
    """Flatten post into a clean dict with ACF fields."""
    result = {
        "id": card.get("id"),
        "slug": card.get("slug"),
        "title": card.get("title", {}).get("rendered", ""),
        "link": card.get("link", ""),
    }
    acf = card.get("acf", {})
    # Only include non-empty ACF fields
    for k, v in acf.items():
        if v is not None and v != "" and v != [] and v != {}:
            # Convert strings to numbers where possible
            if isinstance(v, str) and v.replace(".", "").replace("-", "").isdigit():
                try:
                    result[k] = float(v) if "." in v else int(v)
                except ValueError:
                    result[k] = v
            else:
                result[k] = v
    return result

def main():
    print("=" * 60)
    print("📡 DuitGain Full Data Scraper")
    print("=" * 60)

    # 1. Mileage Cards (KrisFlyer + Enrich) — 80+ cards
    print("\n[1] Mileage Cards...")
    mc = paginate("/mileage_card", per_page=100)
    if mc:
        data = [clean_card(c) for c in mc]
        save("mileage_cards.json", data)
        non_zero = sum(1 for d in data if any("multiplier" in k and d.get(k, 0) != 0 for k in d))
        print(f"    ✓ {len(data)} cards ({non_zero} with multipliers)")

    # 2. Cashback Cards — 69 cards
    print("\n[2] Cashback Cards...")
    cc = paginate("/cashback_card", per_page=100)
    if cc:
        data = [clean_card(c) for c in cc]
        save("cashback_cards.json", data)
        print(f"    ✓ {len(data)} cards")

    # 3. Credit Cards (main DB — 280+ cards)
    print("\n[3] Credit Cards (main DB)...")
    cr = paginate("/credit_cards", per_page=50)
    if cr:
        data = [clean_card(c) for c in cr]
        save("credit_cards.json", data)
        print(f"    ✓ {len(data)} cards")

    # 4. Enrich Locations (redemption rates — 51 destinations)
    print("\n[4] Enrich Locations...")
    el = paginate("/enrich_location", per_page=100)
    if el:
        data = [clean_card(c) for c in el]
        save("enrich_locations.json", data)
        print(f"    ✓ {len(data)} destinations")

    # 6. Card Images (resolve media IDs to URLs for credit cards, mileage cards, cashback cards)
    print("\n[6] Card Images...")
    img_ids = set()
    # From credit cards (main DB)
    for c in cr:
        img_id = c.get("credit_card_image") or c.get("acf", {}).get("credit_card_image")
        if img_id and str(img_id).isdigit():
            img_ids.add(int(img_id))
    # From mileage cards  
    for c in mc:
        for field in ['mileage_card_image', 'card_image', 'credit_card_image']:
            img_id = c.get(field) or c.get("acf", {}).get(field)
            if img_id and str(img_id).isdigit():
                img_ids.add(int(img_id))
    # From cashback cards
    for c in cc:
        for field in ['cashback_card_image', 'card_image', 'credit_card_image']:
            img_id = c.get(field) or c.get("acf", {}).get(field)
            if img_id and str(img_id).isdigit():
                img_ids.add(int(img_id))
    print(f"    {len(img_ids)} unique image IDs to resolve")
    
    images = {}
    resolved = 0
    for iid in sorted(img_ids):
        url = f"{API}/media/{iid}"
        data = fetch_url(url)
        if data and isinstance(data, dict):
            src = data.get("source_url", "")
            alt = data.get("alt_text", "") or data.get("title", {}).get("rendered", "")
            sizes = data.get("media_details", {}).get("sizes", {})
            thumb = ""
            if sizes:
                # Prefer medium, fallback to full
                thumb = sizes.get("medium", sizes.get("full", {})).get("source_url", "")
            images[str(iid)] = {"url": src, "alt": alt, "thumb": thumb or src}
            resolved += 1
        time.sleep(0.1)
    save("card_images.json", images)
    print(f"    ✓ {resolved}/{len(img_ids)} images resolved ({len(images)} total)")
    print(f"    ✓ card_images.json")
    print("\n[5] Blog Posts...")
    posts = paginate("/posts", per_page=50)
    if posts:
        data = [{
            "id": p.get("id"),
            "slug": p.get("slug"),
            "title": p.get("title", {}).get("rendered", ""),
            "date": p.get("date"),
            "link": p.get("link"),
            "excerpt": p.get("excerpt", {}).get("rendered", ""),
            "yoast_title": p.get("yoast_head_json", {}).get("title", "") if isinstance(p.get("yoast_head_json"), dict) else "",
            "yoast_desc": p.get("yoast_head_json", {}).get("description", "") if isinstance(p.get("yoast_head_json"), dict) else "",
        } for p in posts]
        save("posts.json", data)
        print(f"    ✓ {len(data)} posts")

    # Summary
    print("\n" + "=" * 60)
    print("✅ Scrape Complete!")
    total_files = len([f for f in os.listdir(OUT) if f.endswith(".json")])
    total_size = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith(".json"))
    print(f"   Files: {total_files}")
    print(f"   Size:  {total_size / 1024:.0f} KB")
    print(f"   Saved: {OUT}")

def save(name, data):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    💾 {name} ({len(json.dumps(data)) / 1024:.0f} KB)")

if __name__ == "__main__":
    main()
