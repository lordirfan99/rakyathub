#!/usr/bin/env python3
"""
Update Harga Makanan Asas — Download PriceCatcher data, aggregate food prices.
Run this before build to refresh food price data.

FIXED v2: Dynamic item code lookup by name instead of hardcoded codes.
Sources: KPDN PriceCatcher, DOSM CPI | CC BY 4.0
"""

import csv
import json
import os
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Item definitions: search by keyword, filter by unit ──
# Each entry: (display_name, search_keyword, unit_filter, exclude_keywords)
# unit_filter="" means accept any unit
# exclude_keywords: list of words to exclude from results
ITEM_DEFS = [
    # Ayam & Daging
    ("Ayam Standard",        "AYAM BERSIH - STANDARD",     "1kg",   []),
    ("Ayam Super",           "AYAM BERSIH - SUPER",        "1kg",   []),
    ("Daging Lembu Tempatan","DAGING LEMBU TEMPATAN",      "1kg",   []),
    ("Daging Lembu Import",  "DAGING LEMBU IMPORT",        "1kg",   []),
    ("Daging Kambing Import","DAGING KAMBING BEBIRI IMPORT BERTULANG", "1kg", []),

    # Ikan
    ("Ikan Kembung",         "IKAN KEMBUNG",               "1kg",   ["GORENG", "KICAP", "TIGA RASA", "KECIL/PELALING"]),
    ("Ikan Keli",            "IKAN KELI",                  "1kg",   []),
    ("Ikan Tilapia",         "IKAN TILAPIA",               "1kg",   ["GORENG"]),
    ("Ikan Haruan",          "IKAN HARUAN",                "1kg",   []),

    # Telur
    ("Telur Gred A",         "TELUR AYAM GRED A",          "",      []),
    ("Telur Gred B",         "TELUR AYAM GRED B",          "",      []),
    ("Telur Gred C",         "TELUR AYAM GRED C",          "",      []),

    # Beras
    ("Beras Super (10kg)",   "BERAS SUPER",                "10 kg", ["SABAH", "SARAWAK", "TEPUNG"]),

    # Minyak — group by unit size, average across brands
    ("Minyak Masak (1kg)",   "MINYAK MASAK",               "1kg",   []),
    ("Minyak Masak (5kg)",   "MINYAK MASAK",               "5 kg",  []),

    # Gula & Perasa
    ("Gula Pasir (1kg)",     "GULA PUTIH",                 "1kg",   []),
    ("Tepung Gandum (1kg)",  "TEPUNG GANDUM",              "1kg",   ["BERAS"]),
    ("Santan Kelapa Segar",  "SANTAN KELAPA SEGAR",        "",      []),

    # Bawang
    ("Bawang Merah",         "BAWANG KECIL MERAH ROSE IMPORT (INDIA)", "1kg", []),
    ("Bawang Putih",         "BAWANG PUTIH IMPORT (CHINA)", "1kg",  []),

    # Sayur
    ("Cili Hijau",           "CILI HIJAU",                 "1kg",   []),
    ("Cili Merah",           "CILI MERAH - KULAI",         "1kg",   []),
    ("Halia",                "HALIA BASAH (TUA)",          "1kg",   []),
    ("Kacang Bendi",         "KACANG BENDI",               "1kg",   []),
    ("Kacang Panjang",       "KACANG PANJANG",             "1kg",   []),
    ("Kubis Import",         "KUBIS BULAT IMPORT",         "1kg",   []),
    ("Kubis Tempatan",       "KUBIS BULAT (TEMPATAN)",     "1kg",   []),
    ("Lobak Merah",          "LOBAK MERAH",                "1kg",   []),
    ("Timun",                "TIMUN",                      "1kg",   []),
]


def download_csv(url):
    """Download a CSV and return parsed rows as list of dicts."""
    print(f"  Downloading {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "RakyatHub/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read().decode("utf-8")
    reader = csv.DictReader(data.splitlines())
    return list(reader)


def find_item_codes(items_csv, definitions):
    """
    Dynamically find item codes by searching item names.
    Returns: {display_name: [(code, unit, full_name), ...]}
    """
    item_map = {}
    for r in items_csv:
        name = r.get("item", "").strip().upper()
        code = int(r.get("item_code", 0))
        unit = r.get("unit", "").strip()
        full = r.get("item", "").strip()
        for display_name, keyword, unit_filter, excludes in definitions:
            # Match keyword
            if keyword.upper() not in name:
                continue
            # Filter by unit if specified
            if unit_filter and unit.upper() != unit_filter.upper():
                continue
            # Exclude keywords
            if any(excl.upper() in name for excl in excludes):
                continue
            if display_name not in item_map:
                item_map[display_name] = []
            item_map[display_name].append((code, unit, full))

    return item_map


def main():
    # Step 1: Download item lookup
    print("Step 1: Downloading item lookup...")
    try:
        items_csv = download_csv("https://storage.data.gov.my/pricecatcher/lookup_item.csv")
    except Exception as e:
        print(f"  FATAL: Cannot download item lookup: {e}")
        return

    # Step 2: Find current item codes
    print("Step 2: Looking up item codes by name...")
    item_map = find_item_codes(items_csv, ITEM_DEFS)

    # Build reverse map: code -> (display_name, unit)
    code_to_item = {}
    unit_map = {}
    for display_name, entries in item_map.items():
        for code, unit, full_name in entries:
            if code not in code_to_item:
                code_to_item[code] = display_name
                unit_map[code] = unit or "unit"

    wanted_codes = set(code_to_item.keys())
    print(f"  Found {len(wanted_codes)} item codes across {len(item_map)} categories:")
    for display_name, entries in sorted(item_map.items()):
        codes_str = ", ".join([f"{c} ({u})" for c, u, _ in entries])
        print(f"    {display_name:30s} → codes: {codes_str}")

    # Step 3: Download price data
    today = datetime.now()
    month_str = today.strftime("%Y-%m")

    print(f"Step 3: Downloading prices ({month_str})...")
    prices = None
    for attempt in range(2):
        url = f"https://storage.data.gov.my/pricecatcher/pricecatcher_{month_str}.csv"
        try:
            prices = download_csv(url)
            break
        except Exception as e:
            print(f"  Failed: {e}")
            # Try previous month
            prev = today.replace(day=1) - timedelta(days=1)
            month_str = prev.strftime("%Y-%m")
            print(f"  Trying previous month: {month_str}...")

    if prices is None:
        print("  FATAL: Cannot download price data")
        return

    print(f"  Got {len(prices):,} price records")

    # Step 4: Aggregate prices
    print("Step 4: Aggregating prices...")
    agg = defaultdict(lambda: defaultdict(list))
    dates_seen = set()
    total_matched = 0

    for r in prices:
        try:
            code = int(r["item_code"])
            price = float(r["price"])
            date = r["date"]
        except (ValueError, KeyError):
            continue

        if code in wanted_codes:
            agg[code][date].append(price)
            dates_seen.add(date)
            total_matched += 1

    dates_sorted = sorted(dates_seen)
    latest_date = dates_sorted[-1] if dates_sorted else today.strftime("%Y-%m-%d")

    print(f"  Matched {total_matched:,} records across {len(agg)} codes")

    # Step 5: Compute prices per category
    print("Step 5: Computing category averages...")

    result = {
        "last_updated": today.strftime("%Y-%m-%d %H:%M"),
        "source": "KPDN PriceCatcher",
        "method": "Dynamic item code lookup v2",
        "latest_date": latest_date,
        "dates_available": len(dates_sorted),
        "items": [],
        "categories_found": len(item_map),
        "codes_used": len(wanted_codes),
        "total_records": len(prices),
        "matched_records": total_matched,
    }

    for display_name, entries in sorted(item_map.items()):
        codes = [c for c, u, f in entries]

        # Collect all prices for this category across all dates
        cat_dates = defaultdict(list)
        for code in codes:
            if code in agg:
                for date, price_list in agg[code].items():
                    cat_dates[date].extend(price_list)

        if not cat_dates:
            continue

        date_keys = sorted(cat_dates.keys(), reverse=True)

        # Latest period (most recent date with data)
        latest_prices = cat_dates[date_keys[0]]
        # Previous period (second most recent date)
        prev_prices = cat_dates[date_keys[1]] if len(date_keys) >= 2 else latest_prices

        avg_price = round(sum(latest_prices) / len(latest_prices), 2) if latest_prices else 0
        prev_avg = round(sum(prev_prices) / len(prev_prices), 2) if prev_prices else avg_price

        change = round(avg_price - prev_avg, 2)
        change_pct = round((change / prev_avg) * 100, 1) if prev_avg > 0 else 0

        min_price = round(min(latest_prices), 2)
        max_price = round(max(latest_prices), 2)

        # Get unit from first matched entry
        unit = unit_map.get(codes[0], "") if codes else ""

        result["items"].append({
            "name": display_name,
            "unit": unit,
            "codes": codes,
            "price": avg_price,
            "min_price": min_price,
            "max_price": max_price,
            "prev_price": prev_avg,
            "change": change,
            "change_pct": change_pct,
            "sample_size": len(latest_prices),
            "latest_date": date_keys[0],
        })

    # Summary stats
    result["items_count"] = len(result["items"])
    prices_list = [i["price"] for i in result["items"] if i["price"] > 0]
    result["avg_price"] = round(sum(prices_list) / len(prices_list), 2) if prices_list else 0

    up = sum(1 for i in result["items"] if i["change"] > 0.01)
    down = sum(1 for i in result["items"] if i["change"] < -0.01)
    result["up"] = up
    result["down"] = down
    result["flat"] = result["items_count"] - up - down

    # Write output
    output_path = os.path.join(DATA_DIR, "harga-makanan.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! {result['items_count']} items tracked")
    print(f"   Latest date: {latest_date}")
    print(f"   Output: {output_path}")

    # Print summary
    print(f"\n📊 Latest Prices ({latest_date}):")
    for item in sorted(result["items"], key=lambda x: x["price"], reverse=True):
        arrow = "▲" if item["change"] > 0 else "▼" if item["change"] < 0 else "➡"
        print(f"  {item['name']:30s} | RM {item['price']:<7.2f} | {arrow} {item['change']:+.2f} ({item['change_pct']:+.1f}%)")


if __name__ == "__main__":
    main()
