#!/usr/bin/env python3
"""
Scrape gold price from Yahoo Finance (XAU/USD + USD/MYR) and write
to public/data/emas-harga.json for the Emas calculator to consume.

Runs every 4 hours from a cron job.
"""
import json, os, urllib.request
from datetime import datetime
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent
DATA_DIR = SITE_DIR / "public" / "data"
DATA_FILE = DATA_DIR / "emas-harga.json"

YAHOO_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def yahoo_fetch(symbol: str) -> float:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": YAHOO_UA})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return data["chart"]["result"][0]["meta"]["regularMarketPrice"]

def main():
    try:
        gold_usd = yahoo_fetch("GC=F")          # Gold futures (USD/oz)
        usd_myr  = yahoo_fetch("USDMYR=X")       # USD/MYR forex

        # 1 troy oz = 31.1035 grams
        gold_per_gram_myr = (gold_usd / 31.1035) * usd_myr

        # Spread estimates (typical Malaysia market)
        spread_pg      = 5.8    # Public Gold buy/sell spread %
        spread_kedai   = 12.0   # Kedai emas typical spread %

        harga_beli_pg  = round(gold_per_gram_myr, 2)
        harga_jual_pg  = round(gold_per_gram_myr * (1 - spread_pg/100), 2)
        harga_beli_kedai = round(gold_per_gram_myr, 2)
        harga_jual_kedai = round(gold_per_gram_myr * (1 - spread_kedai/100), 2)

        payload = {
            "timestamp": datetime.now().isoformat(),
            "source": "Yahoo Finance (GC=F + USDMYR=X)",
            "gold_usd_per_oz": round(gold_usd, 2),
            "usd_myr": usd_myr,
            "harga_per_gram": harga_beli_pg,
            "public_gold": {
                "beli": harga_beli_pg,
                "jual": harga_jual_pg,
                "spread_pct": spread_pg,
            },
            "kedai_emas": {
                "beli": harga_beli_kedai,
                "jual": harga_jual_kedai,
                "spread_pct": spread_kedai,
            },
        }

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(payload, indent=2))
        print(f"[Scrape Emas] ✅ Written: {DATA_FILE}")
        print(f"   Gold: ${gold_usd}/oz | USD/MYR: {usd_myr}")
        print(f"   Harga/g: RM {harga_beli_pg} | PG Jual: RM {harga_jual_pg} | Kedai Jual: RM {harga_jual_kedai}")

    except Exception as e:
        print(f"[Scrape Emas] ❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
