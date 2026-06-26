import json, urllib.request, sys

def fetch(id):
    url = f"https://api.data.gov.my/data-catalogue?id={id}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

print("=== HIES PERCENTILE ===")
d = fetch("hies_malaysia_percentile")
if isinstance(d, list):
    dates = sorted(set(r["date"] for r in d))
    vars_set = sorted(set(r["variable"] for r in d))
    print(f"Years: {dates}")
    print(f"Vars: {vars_set}")
    print(f"Rows: {len(d)}")
    # Show sample for each variable
    for v in vars_set:
        sample = [r for r in d if r["variable"]==v]
        print(f"  {v}: {len(sample)} rows, sample: {sample[0]}")
else:
    print(f"Unexpected: {d}")

print("\n=== HIES STATE ===")
d2 = fetch("hies_state_percentile")
if isinstance(d2, list):
    dates2 = sorted(set(r["date"] for r in d2))
    states = sorted(set(r.get("state","?") for r in d2))
    print(f"Years: {dates2}")
    print(f"States: {len(states)}")
    print(f"Rows: {len(d2)}")
    if d2:
        print(f"Sample keys: {list(d2[0].keys())}")
        print(f"Sample: {d2[0]}")
else:
    print(f"Unexpected: {d2}")

print("\n=== SALARIES WAGES (2023) ===")
d3 = fetch("salaries_wages_2023")
if isinstance(d3, list):
    print(f"Rows: {len(d3)}")
    if d3:
        print(f"Keys: {list(d3[0].keys())}")
        print(f"Sample: {d3[0]}")
else:
    # Try without year suffix
    d3b = fetch("salaries_wages")
    if isinstance(d3b, list):
        print(f"Rows: {len(d3b)}")
        if d3b:
            print(f"Keys: {list(d3b[0].keys())}")
            print(f"Sample: {d3b[0]}")
    else:
        print(f"No salaries data found: {d3}")
