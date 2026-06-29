#!/usr/bin/env python3
"""
RakyatHub Government Data Fetcher
Downloads datasets from data.gov.my (OpenDOSM + Data-Catalogue APIs)
Saves to src/data/ for use by Astro pages.

Run: python3 scripts/fetch-gov-data.py
Integrated into: netlify build
"""
import json, os, urllib.request, sys, time
from collections import defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "src", "data")
os.makedirs(DATA_DIR, exist_ok=True)

UA = "RakyatHub/1.0"
OPENDOSM = "https://api.data.gov.my/opendosm"
DATA_CAT = "https://api.data.gov.my/data-catalogue"

fetched = 0
failed = 0

def fetch_opendosm(id, params="", limit=500):
    """Fetch from OpenDOSM endpoint (DOSM-sourced datasets: CPI, GDP, LFS, trade, etc.)"""
    url = f"{OPENDOSM}?id={id}&limit={limit}{params}"
    return _fetch(id, url, "opendosm")

def fetch_datacat(id, params="", limit=500):
    """Fetch from Data-Catalogue endpoint (BNM, JPJ, EPF, PDRM, etc.)"""
    url = f"{DATA_CAT}?id={id}&limit={limit}{params}"
    return _fetch(id, url, "data-cat")

def _fetch(id, url, source):
    global fetched, failed
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        if isinstance(data, list):
            print(f"  ✅ {id}: {len(data)} rows (from {source})")
            fetched += 1
            return data
        else:
            print(f"  ⚠️  {id}: unexpected type {type(data).__name__}")
            failed += 1
            return []
    except Exception as e:
        print(f"  ❌ {id}: {e}")
        failed += 1
        return []

def save(name, data):
    path = os.path.join(DATA_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    size = os.path.getsize(path)
    key_count = len(data) if isinstance(data, list) else (len(data) if isinstance(data, dict) else 1)
    print(f"     -> saved {name}.json ({size:,} bytes, {key_count} items)")

def main():
    global fetched, failed
    start = time.time()
    print("=" * 60)
    print(f"  RakyatHub Data Fetcher - {datetime.now().isoformat()}")
    print("=" * 60)

    # -- ECONOMIC DATA (OpenDOSM) --
    print("\n--- ECONOMIC DATA ---")

    gdp_qtr_real = fetch_opendosm("gdp_qtr_real", "&series=abs")
    save("gdp-quarterly-real", gdp_qtr_real)

    gdp_qtr_nominal = fetch_opendosm("gdp_qtr_nominal", "&series=abs")
    save("gdp-quarterly-nominal", gdp_qtr_nominal)

    gdp_annual_nominal = fetch_opendosm("gdp_gni_annual_nominal", "&limit=100")
    save("gdp-annual-nominal", gdp_annual_nominal)

    gdp_annual_real = fetch_opendosm("gdp_gni_annual_real", "&limit=100")
    save("gdp-annual-real", gdp_annual_real)

    trade = fetch_opendosm("trade_sitc_1d")
    save("trade-sitc", trade)

    ipi = fetch_opendosm("ipi")
    save("ipi", ipi)

    electricity = fetch_opendosm("electricity_consumption")
    save("electricity-consumption", electricity)

    wrt = fetch_opendosm("iowrt")
    save("wholesale-retail-trade", wrt)

    # -- FINANCIAL DATA (Data-Catalogue) --
    print("\n--- FINANCIAL DATA ---")

    epf = fetch_datacat("epf_dividend")
    save("epf-dividend", epf)

    fx = fetch_datacat("exchangerates_daily_0900", "&limit=90")
    save("exchange-rates", fx)

    fx_monthly = fetch_datacat("exchangerates", "&limit=200")
    save("exchange-rates-monthly", fx_monthly)

    ir = fetch_datacat("interestrates", "&limit=200")
    save("interest-rates", ir)

    ma = fetch_datacat("monetary_aggregates")
    save("monetary-aggregates", ma)

    pi = fetch_datacat("payment_instruments", "&limit=100")
    save("payment-instruments", pi)

    fpx = fetch_datacat("trnsc_daily_fpx", "&limit=90")
    save("fpx-transactions", fpx)

    jpay = fetch_datacat("trnsc_daily_jompay", "&limit=90")
    save("jompay-transactions", jpay)

    # -- DEMOGRAPHIC DATA --
    print("\n--- DEMOGRAPHIC DATA ---")

    pop_state = fetch_datacat("population_state", "&limit=500")
    save("population-state", pop_state)

    pop_my = fetch_datacat("population_malaysia", "&limit=200")
    save("population-malaysia", pop_my)

    births = fetch_datacat("births_annual", "&limit=100")
    save("births", births)

    fertility = fetch_datacat("fertility", "&limit=200")
    save("fertility", fertility)

    marriages = fetch_datacat("marriages", "&limit=100")
    save("marriages", marriages)

    # -- HOUSEHOLD DATA --
    print("\n--- HOUSEHOLD DATA ---")

    pov_state = fetch_datacat("hh_poverty_state", "&limit=200")
    save("poverty-state", pov_state)

    ineq_state = fetch_datacat("hh_inequality_state", "&limit=200")
    save("inequality-state", ineq_state)

    hh_profile = fetch_datacat("hh_profile", "&limit=100")
    save("household-profile", hh_profile)

    # -- TRANSPORTATION --
    print("\n--- TRANSPORTATION ---")

    cars = fetch_datacat("registration_transactions_car", "&limit=90")
    save("car-registrations", cars)

    veh_fuel = fetch_datacat("registrations_type_fuel", "&limit=200")
    save("vehicle-fuel-registrations", veh_fuel)

    # -- PUBLIC SAFETY --
    print("\n--- PUBLIC SAFETY ---")

    crime = fetch_datacat("crime_district", "&limit=500")
    save("crime-district", crime)

    drug_age = fetch_datacat("drug_arrests_age", "&limit=100")
    save("drug-arrests", drug_age)

    prisoners = fetch_datacat("prisoners_state", "&limit=100")
    save("prisoners", prisoners)

    # -- PUBLIC ADMINISTRATION --
    print("\n--- PUBLIC ADMINISTRATION ---")

    budget_moe = fetch_datacat("federal_budget_moe", "&limit=50")
    save("budget-education", budget_moe)

    budget_moh = fetch_datacat("federal_budget_moh", "&limit=50")
    save("budget-health", budget_moh)

    fed_finance = fetch_datacat("federal_finance_year", "&limit=100")
    save("federal-finance", fed_finance)

    gov_apps = fetch_datacat("government_apps", "&limit=100")
    save("government-apps", gov_apps)

    # -- ENVIRONMENT --
    print("\n--- ENVIRONMENT ---")

    forest = fetch_datacat("forest_reserve_state", "&limit=100")
    save("forest-reserves", forest)

    water = fetch_datacat("water_consumption", "&limit=100")
    save("water-consumption", water)

    # -- HEALTHCARE --
    print("\n--- HEALTHCARE ---")

    beds = fetch_datacat("hospital_beds", "&limit=200")
    save("hospital-beds", beds)

    blood = fetch_datacat("blood_donations", "&limit=200")
    save("blood-donations", blood)

    immun = fetch_datacat("infant_immunisation", "&limit=100")
    save("infant-immunisation", immun)

    # -- EDUCATION --
    print("\n--- EDUCATION ---")

    schools = fetch_datacat("schools_district", "&limit=500")
    save("schools-district", schools)

    # -- SUMMARY --
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"  COMPLETE: {fetched} datasets fetched, {failed} failed")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Output: {DATA_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
