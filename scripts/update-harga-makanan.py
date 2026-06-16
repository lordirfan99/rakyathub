#!/usr/bin/env python3
"""
Update Harga Makanan Asas — Download PriceCatcher data, aggregate food prices.
Run this before build to refresh food price data.

Sources: KPDN PriceCatcher, DOSM CPI
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

# --- Key food items to track (item code → display name) ---
KEY_FOOD_ITEMS = {
    1: "Ayam Standard",
    2: "Ayam Super",
    9: "Daging Kambing Import",
    47: "Daging Lembu Tempatan",
    55: "Daging Lembu Import",
    70: "Ikan Kembung",
    88: "Ikan Keli",
    89: "Ikan Tilapia",
    87: "Ikan Haruan",
    92: "Cili Hijau",
    93: "Cili Merah",
    95: "Halia",
    96: "Kacang Bendi",
    98: "Kacang Panjang",
    104: "Kubis Bulat Import",
    105: "Kubis Bulat Tempatan",
    113: "Timun",
    114: "Terung Panjang",
    108: "Kunyit Hidup",
    109: "Lobak Merah",
    129: "Bayam",
    131: "Sawi",
    137: "Kangkung",
    845: "Beras Super Spesial Tempatan (5kg)",
    847: "Bertas Import (5kg)",
    1109: "Minyak Masak Sawit (5kg)",
    1110: "Minyak Masak Sawit (1kg)",
    1131: "Gula Pasir Kasar (1kg)",
    1132: "Gula Pasir Halus (1kg)",
    1440: "Telur Ayam Gred A (1 biji)",
    1442: "Telur Ayam Gred C (1 biji)",
    1481: "Bawang Merah Kering",
    1555: "Bawang Putih Import China (1kg)",
    1819: "Tepung Gandum (1kg)",
    2045: "Santan Kelapa Segar",
    2047: "Santan Kotak",
    2086: "Garam Kasar (1kg)",
    1916: "Susu Cair Manis (tin)",
    1926: "Milo (tin)",
    1928: "Kopi Serbuk",
}

def download_csv(url):
    """Download a CSV and return parsed rows as list of dicts."""
    print(f"  Downloading {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "RakyatHub/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")
    reader = csv.DictReader(data.splitlines())
    return list(reader)

def main():
    # Step 1: Download item lookup
    print("Step 1: Downloading item lookup...")
    items = download_csv("https://storage.data.gov.my/pricecatcher/lookup_item.csv")
    item_names = {int(r["item_code"]): r["item"].strip() for r in items if r.get("item_code") and r.get("item")}
    item_units = {int(r["item_code"]): r["unit"].strip() for r in items if r.get("item_code") and r.get("unit")}
    print(f"  Loaded {len(items)} items")

    # Step 2: Find latest pricecatcher file
    # Try current month first
    today = datetime.now()
    month_str = today.strftime("%Y-%m")
    csv_url = f"https://storage.data.gov.my/pricecatcher/pricecatcher_{month_str}.csv"
    
    print(f"Step 2: Downloading prices ({csv_url})...")
    try:
        prices = download_csv(csv_url)
    except Exception as e:
        print(f"  Failed: {e}, trying previous month...")
        prev = today.replace(day=1) - timedelta(days=1)
        csv_url = f"https://storage.data.gov.my/pricecatcher/pricecatcher_{prev.strftime('%Y-%m')}.csv"
        prices = download_csv(csv_url)
    
    print(f"  Got {len(prices)} price records")

    # Step 3: Aggregate prices for key food items by date
    print("Step 3: Aggregating prices...")
    # {item_code: {date: [prices]}}
    agg = defaultdict(lambda: defaultdict(list))
    dates_seen = set()
    
    for r in prices:
        try:
            code = int(r["item_code"])
            price = float(r["price"])
            date = r["date"]
        except (ValueError, KeyError):
            continue
        
        if code in KEY_FOOD_ITEMS:
            agg[code][date].append(price)
            dates_seen.add(date)
    
    dates_sorted = sorted(dates_seen)
    latest_date = dates_sorted[-1] if dates_sorted else today.strftime("%Y-%m-%d")
    
    # Compute average prices for latest 3 available dates
    result = {
        "last_updated": today.strftime("%Y-%m-%d %H:%M"),
        "source": "KPDN PriceCatcher",
        "source_url": csv_url,
        "latest_date": latest_date,
        "dates_available": len(dates_sorted),
        "items": [],
        "total_records": len(prices),
    }
    
    for code in sorted(KEY_FOOD_ITEMS.keys()):
        if code not in agg or not agg[code]:
            continue
        
        # Get latest 3 days with data
        item_dates = sorted(agg[code].keys(), reverse=True)[:3]
        
        latest_prices = []
        prev_prices = []
        
        for i, d in enumerate(item_dates):
            prices_list = agg[code][d]
            avg = round(sum(prices_list) / len(prices_list), 2)
            if i == 0:
                latest_prices = prices_list
            elif i == 1:
                prev_prices = prices_list
        
        # Current average
        avg_price = round(sum(latest_prices) / len(latest_prices), 2) if latest_prices else 0
        
        # Previous period average (for trend)
        prev_avg = round(sum(prev_prices) / len(prev_prices), 2) if prev_prices else avg_price
        
        # Change
        change = round(avg_price - prev_avg, 2)
        change_pct = round((change / prev_avg) * 100, 1) if prev_avg > 0 else 0
        
        result["items"].append({
            "code": code,
            "name": KEY_FOOD_ITEMS[code],
            "full_name": item_names.get(code, KEY_FOOD_ITEMS[code]),
            "unit": item_units.get(code, ""),
            "price": avg_price,
            "prev_price": prev_avg,
            "change": change,
            "change_pct": change_pct,
            "sample_size": len(latest_prices),
            "latest_date": item_dates[0] if item_dates else latest_date,
        })
    
    # Also compute CPI context
    result["items_count"] = len(result["items"])
    result["avg_price"] = round(sum(i["price"] for i in result["items"]) / len(result["items"]), 2) if result["items"] else 0
    
    # Write output
    output_path = os.path.join(DATA_DIR, "harga-makanan.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Done! {result['items_count']} items tracked")
    print(f"   Latest date: {latest_date}")
    print(f"   Output: {output_path}")
    
    # Print summary
    print(f"\n📊 Latest Prices ({latest_date}):")
    for item in sorted(result["items"], key=lambda x: x["price"], reverse=True)[:20]:
        arrow = "▲" if item["change"] > 0 else "▼" if item["change"] < 0 else "➡"
        print(f"  {item['name']:30s} | RM {item['price']:<7.2f} | {arrow} {item['change']:+.2f} ({item['change_pct']:+.1f}%)")

if __name__ == "__main__":
    main()
