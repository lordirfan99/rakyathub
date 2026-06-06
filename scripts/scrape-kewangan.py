#!/usr/bin/env python3
"""
Scrape Malaysian financial data for all calculators:
- Gold price (XAU/USD + USD/MYR → MYR/g)
- OPR / BNM policy rate
- Derived loan rates, FD estimates

Writes to public/data/kewangan-harga.json
"""
import json, os, urllib.request
from datetime import datetime
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent
DATA_DIR = SITE_DIR / "public" / "data"
DATA_FILE = DATA_DIR / "kewangan-harga.json"

YAHOO_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5a0.0)"

def yahoo_fetch(symbol: str) -> float:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": YAHOO_UA})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return data["chart"]["result"][0]["meta"]["regularMarketPrice"]

def main():
    try:
        # --- Live scraped data ---
        gold_usd = yahoo_fetch("GC=F")          # Gold futures USD/oz
        usd_myr  = yahoo_fetch("USDMYR=X")       # USD/MYR
        opr      = 3.00                          # Fallback OPR (last BNM: 3.00%)
        try:
            opr = yahoo_fetch("MYSVC.DE")        # BNM-linked ETF / fallback
        except:
            pass  # keep fallback

        # --- Derived values ---
        gold_per_gram_myr = (gold_usd / 31.1035) * usd_myr

        # Interest rate estimates (typical Malaysian bank spreads)
        spread_pg     = 5.8
        spread_kedai  = 12.0
        housing_loan  = round(opr + 2.25, 2)
        car_loan      = round(opr + 0.3, 2)
        fd_3month     = round(opr - 0.5, 2) if opr > 0.5 else 2.5
        fd_12month    = round(opr - 0.1, 2) if opr > 0.1 else 3.0

        payload = {
            "timestamp": datetime.now().isoformat(),
            "source": "Yahoo Finance (GC=F, USDMYR=X)",
            "emas": {
                "harga_per_gram": round(gold_per_gram_myr, 2),
                "gold_usd_per_oz": round(gold_usd, 2),
                "usd_myr": usd_myr,
                "public_gold": {
                    "beli": round(gold_per_gram_myr, 2),
                    "jual": round(gold_per_gram_myr * (1 - spread_pg/100), 2),
                    "spread_pct": spread_pg,
                },
                "kedai_emas": {
                    "beli": round(gold_per_gram_myr, 2),
                    "jual": round(gold_per_gram_myr * (1 - spread_kedai/100), 2),
                    "spread_pct": spread_kedai,
                },
            },
            "kadar": {
                "opr": opr,
                "housing_loan_pct": housing_loan,
                "car_loan_pct": car_loan,
                "fd_3month_pct": fd_3month,
                "fd_12month_pct": fd_12month,
            },
            "rujukan": {
                "asb_dividen_terkini": 5.75,
                "kwsp_dividen_terkini": 6.15,
                "epf_pekerja_pct": 11.0,
                "sst_barang_pct": 8.0,
                "sst_perkhidmatan_pct": 6.0,
                "str_maksimum": 3700,
                "sara_maksimum": 2400,
            },
            "zakat": {
                "nisab_gram": 85,
                "nisab_rm": round(gold_per_gram_myr * 85, 2),
                "kadar_pct": 2.5,
            },
        }

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"[Scrape Kewangan] ✅ Written: {DATA_FILE}")
        print(f"   Emas: RM {payload['emas']['harga_per_gram']}/g")
        print(f"   Nisab Zakat: RM {payload['zakat']['nisab_rm']}")
        print(f"   OPR: {opr}% | Loan Rumah: {housing_loan}% | Kereta: {car_loan}%")
        print(f"   FD 3bln: {fd_3month}% | FD 12bln: {fd_12month}%")

    except Exception as e:
        print(f"[Scrape Kewangan] ❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
