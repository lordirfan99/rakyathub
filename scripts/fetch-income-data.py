#!/usr/bin/env python3
"""Fetch DOSM household income & labour data — run before build."""
import json, os, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "src", "data")
os.makedirs(DATA_DIR, exist_ok=True)

API = "https://api.data.gov.my/opendosm"
UA = "RakyatHub/1.0"

def fetch(id, params=""):
    url = f"{API}?id={id}{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def main():
    print("Fetching DOSM income & labour data...")

    state_data = fetch("hh_income_state", "&limit=400")
    national_data = fetch("hh_income", "&limit=100")
    lf_data = fetch("lfs_state_sex", "&sex=both&limit=200")

    latest_state = {}
    for row in state_data:
        s = row["state"]
        if s not in latest_state or row["date"] > latest_state[s]["date"]:
            latest_state[s] = row

    latest_national = national_data[-1] if national_data else {}
    latest_lf = {}
    for row in lf_data:
        s = row["state"]
        if s not in latest_lf or row["date"] > latest_lf[s]["date"]:
            latest_lf[s] = row

    payload = {
        "last_updated": datetime.now().isoformat(),
        "source": "DOSM OpenDOSM API",
        "latest_national_year": latest_national.get("date", "")[:4] if latest_national else "",
        "latest_national": latest_national,
        "national_income": national_data,
        "states": {},
    }

    for s in sorted(latest_state):
        d = latest_state[s]
        lf = latest_lf.get(s, {})
        payload["states"][s] = {
            "income_year": d["date"][:4],
            "income_mean": d["income_mean"],
            "income_median": d.get("income_median"),
            "lf_participation_rate": lf.get("p_rate"),
            "lf_unemployment_rate": lf.get("u_rate"),
        }

    with open(os.path.join(DATA_DIR, "income-data.json"), "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved {len(payload['states'])} states to income-data.json")
    print("Done.")

if __name__ == "__main__":
    main()
