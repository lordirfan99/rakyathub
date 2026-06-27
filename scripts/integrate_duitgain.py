#!/usr/bin/env python3
"""
Convert scraped DuitGain data into RakyatHub-compatible data files.
Generates:
  - src/data/duitgain-cards.json       (all 281 credit cards, flattened)
  - src/data/duitgain-cashback.json    (cashback-specific view)
  - src/data/duitgain-mileage.json     (mileage/points view)
  - src/data/duitgain-enrich.json      (enrich destination & redemption data)
"""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN = os.path.join(BASE, "src", "data", "duitgain")
OUT = os.path.join(BASE, "src", "data")

def load(name):
    path = os.path.join(IN, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def main():
    cc = load("credit_cards.json")
    mc = load("mileage_cards.json")
    cb = load("cashback_cards.json")
    el = load("enrich_locations.json")

    print(f"📦 Converting {len(cc)} credit cards, {len(mc)} mileage cards, {len(cb)} cashback cards, {len(el)} locations\n")

    # ── 1. All Cards Master List ──────────────────────
    images_data = {}
    img_path = os.path.join(IN, "card_images.json")
    if os.path.exists(img_path):
        with open(img_path) as f:
            images_data = json.load(f)
    print(f"    Loaded {len(images_data)} card image mappings")

    all_cards = []
    for c in cc:
        img_id = str(c.get("credit_card_image", ""))
        img_info = images_data.get(img_id, {})
        
        card = {
            "id": c.get("id"),
            "bank": c.get("bank_name") or c.get("credit_card_bank", ""),
            "name": c.get("credit_card_name", ""),
            "slug": c.get("slug", ""),
            "image": img_info.get("thumb", ""),
            "image_url": img_info.get("url", ""),
            "image_alt": img_info.get("alt", ""),
            "min_income": parse_income(c.get("annual_income_number", 0)),
            "islamic": c.get("is_islamic", False),
            "card_type": detect_type(c),
            "networks": detect_networks(c),
            "annual_fee": parse_fee_annual(c.get("annual_fee_principal", "")),
            "annual_fee_num": c.get("annual_fee_number") or parse_fee_annual(c.get("annual_fee_principal", "")),
            "free_for_life": c.get("freeforlife", False),
            "fee_waiver": c.get("annual_fee_principal", ""),
            "supplementary_fee": c.get("annual_fee_supplementary", "Free for Life"),
            "card_category": c.get("card_category", ""),
            "card_type_cash_back": c.get("card_type_cash_back", False),
            "card_type_mileage": c.get("card_type_mileage", False),
            "card_type_balance_transfer": c.get("card_type_balance_transfer", False),
            "card_type_airline": c.get("card_type_airline", False),
            "islamic": c.get("is_islamic", False),
        }

        # Category rates
        cats = ["airlines", "dining", "groceries", "petrol", "online", "overseas",
                "entertainment", "shopping", "utilities", "education", "insurance",
                "pharmacy", "transport", "hotel", "ewallet", "contactless", "tng"]
        for cat in cats:
            cb_rate = c.get(f"cbrate_{cat}", 0)
            kf_rate = c.get(f"kfrate_{cat}", 0)
            mh_rate = c.get(f"mhrate_{cat}", 0)
            pts_rate = c.get(f"ptsrate_{cat}", 0)
            cb_cap = c.get(f"cbcap_{cat}", 0)
            cb_annual = c.get(f"cbcap_{cat}_annual", 0)
            cat_tf = c.get(f"cbcap_{cat}_tf", False)

            if cb_rate or kf_rate or mh_rate or pts_rate:
                entry = cat
                if cb_rate:
                    card[f"cb_{entry}"] = parse_rate(cb_rate)
                    cap_val = parse_cap(cb_cap, cat_tf)
                    if cap_val > 0:
                        card[f"cb_cap_{entry}"] = cap_val
                    if cb_annual:
                        card[f"cb_annual_{entry}"] = cb_annual
                if kf_rate:
                    card[f"kf_{entry}"] = parse_rate(kf_rate)
                if mh_rate:
                    card[f"mh_{entry}"] = parse_rate(mh_rate)
                if pts_rate:
                    card[f"pts_{entry}"] = parse_rate(pts_rate)

        all_cards.append(card)

    save("duitgain-cards.json", all_cards)
    print(f"  ✓ duitgain-cards.json ({len(all_cards)} cards)")

    # ── 2. Cashback Cards View ───────────────────────
    cb_view = []
    for c in all_cards:
        has_cb = any(k.startswith("cb_") and not k.startswith("cb_cap") and not k.startswith("cb_annual") and isinstance(v, (int, float)) and v > 0 for k, v in c.items())
        if has_cb:
            cb_view.append(c)
    save("duitgain-cashback.json", cb_view)
    print(f"  ✓ duitgain-cashback.json ({len(cb_view)} cards with cashback)")

    # ── 3. Mileage Cards View ────────────────────────
    mc_view = []
    for c in all_cards:
        has_kf = any(k.startswith("kf_") and isinstance(v, (int, float)) and v > 0 for k, v in c.items())
        has_mh = any(k.startswith("mh_") and isinstance(v, (int, float)) and v > 0 for k, v in c.items())
        if has_kf or has_mh:
            mc_view.append(c)
    save("duitgain-mileage.json", mc_view)
    print(f"  ✓ duitgain-mileage.json ({len(mc_view)} cards with miles)")

    # ── 4. Enrich Redemption Data ────────────────────
    enrich_out = []
    for loc in el:
        enrich_out.append({
            "city": loc.get("title", ""),
            "zone": loc.get("enrich_zone", "").replace("_", " ").title(),
            "zone_id": loc.get("enrich_zone", ""),
            "country": loc.get("enrich_country", ""),
            "eco_saver": loc.get("enrich_economy_saver", 0),
            "eco_flex": loc.get("enrich_economy_flex", 0),
            "biz_saver": loc.get("enrich_business_saver", 0),
            "biz_flex": loc.get("enrich_business_flex", 0),
        })
    save("duitgain-enrich.json", enrich_out)
    print(f"  ✓ duitgain-enrich.json ({len(enrich_out)} destinations)")

    print(f"\n✅ Integration complete! Output in {OUT}")

def detect_type(c):
    types = []
    if c.get("card_type_cash_back"): types.append("cashback")
    if c.get("card_type_mileage"): types.append("mileage")
    return "|".join(types) if types else "standard"

def detect_networks(c):
    nets = []
    if c.get("visa"): nets.append("Visa")
    if c.get("mastercard"): nets.append("Mastercard")
    if c.get("amex"): nets.append("Amex")
    if c.get("unionpay"): nets.append("UnionPay")
    return nets

def parse_income(v):
    if isinstance(v, (int, float)):
        return int(v)
    return 0

def parse_fee_annual(v):
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        m = re.search(r'RM\s*([0-9,]+)', v)
        if m:
            return int(m.group(1).replace(",", ""))
    return 0

def parse_rate(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r'([0-9.]+)', v)
        if m:
            return float(m.group(1))
    return 0

def parse_cap(v, tf):
    if isinstance(v, (int, float)):
        return int(v) if v else 0
    return 0

def save(name, data):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size = os.path.getsize(path)
    print(f"    {size/1024:.0f} KB written")

if __name__ == "__main__":
    main()
