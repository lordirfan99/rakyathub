#!/usr/bin/env python3
"""Fetch Malaysian election data from ElectionData.MY Open API — run before build.

Caches dropdowns + key election data as JSON in src/data/election/ for
static consumption by Astro pages. Requires ELECTION_API_KEY env var.
"""
import json, os, sys, urllib.request, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "src", "data", "election")
os.makedirs(DATA_DIR, exist_ok=True)

API_BASE = "https://api.electiondata.my/v1"
API_KEY = os.environ.get("ELECTION_API_KEY", "")
UA = "RakyatHub/1.0 (election widget)"

def fetch(path):
    """GET an API endpoint, return parsed JSON."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ERROR {e.code} {path}: {body[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  EXCEPTION {path}: {e}", file=sys.stderr)
        return None

def save(name, data):
    """Write data to JSON, atomically."""
    path = os.path.join(DATA_DIR, name)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)
    print(f"  ✓ {name} ({len(json.dumps(data))} bytes)" if isinstance(data, list) or isinstance(data, dict) else f"  ✓ {name}")

def main():
    if not API_KEY:
        print("❌ ELECTION_API_KEY not set. Skipping election data fetch.")
        return

    print("\n📡 Fetching election data from ElectionData.MY...\n")

    # 1. Seats dropdown (822 entries — 222 Parlimen + 600 DUN)
    print("  [1/7] Seats dropdown...")
    seats = fetch("/seats/dropdown")
    if seats:
        save("seats.json", seats)

    # 2. Elections dropdown (every PRU ever)
    print("  [2/7] Elections dropdown...")
    elections = fetch("/elections/dropdown")
    if elections:
        save("elections.json", elections)
        # Cache key election results
        elections_list = elections.get("elections", elections.get("data", []))
        # Filter to major PRUs for build-time cache (GE-14, GE-15, latest state elections)
        major = [e for e in elections_list
                 if e.get("type") == "parlimen"
                 and e.get("state") == "Malaysia"
                 and e.get("election", "").startswith("GE-")]
        major.sort(key=lambda x: x.get("election", ""))
        latest_major = major[-3:]  # last 3 GEs
        for e in latest_major:
            slug = e.get("election", "").lower().replace("-", "-")
            state = e.get("state", "Malaysia")
            election_id = e.get("election", "")
            print(f"    → {election_id} ({state})...")
            # by_party
            time.sleep(0.1)
            bp = fetch(f"/elections/by_party?state={urllib.request.quote(state)}&election={urllib.request.quote(election_id)}")
            if bp:
                save(f"election_{slug}_{state.lower().replace(' ', '_')}_by_party.json", bp)
            # by_seat
            time.sleep(0.1)
            bs = fetch(f"/elections/by_seat?state={urllib.request.quote(state)}&election={urllib.request.quote(election_id)}")
            if bs:
                save(f"election_{slug}_{state.lower().replace(' ', '_')}_by_seat.json", bs)
            # stats
            time.sleep(0.1)
            st = fetch(f"/elections/stats?state={urllib.request.quote(state)}&election={urllib.request.quote(election_id)}")
            if st:
                save(f"election_{slug}_{state.lower().replace(' ', '_')}_stats.json", st)

    # 3. By-elections (all PRK ever)
    print("  [3/7] By-elections...")
    byelections = fetch("/byelections")
    if byelections:
        save("byelections.json", byelections)

    # 4. Candidates dropdown (every candidate who ever contested)
    print("  [4/7] Candidates dropdown...")
    candidates = fetch("/candidates/dropdown")
    if candidates:
        # Trim to top-N for build-time (store all, but limit what pages render)
        save("candidates.json", candidates)

    # 5. Parties dropdown
    print("  [5/7] Parties dropdown...")
    parties = fetch("/parties/dropdown")
    if parties:
        save("parties.json", parties)

    # 6. Latest PRK results (fetch top 20 popular by-elections for detail cache)
    print("  [6/7] Flagging key data...")

    # 7. Generate summary index
    print("  [7/7] Building summary index...")
    summary = {
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "seats_count": len(seats.get("seats", [])) if seats else 0,
        "elections_count": len(elections.get("elections", [])) if elections else 0,
        "byelections_count": len(byelections.get("data", [])) if byelections else 0,
        "candidates_count": len(candidates) if isinstance(candidates, list) else len(candidates.get("data", [])),
    }
    save("_index.json", summary)
    print(f"\n✅ Done. Cached to {DATA_DIR}")
    print(f"   Seats: {summary['seats_count']} | Elections: {summary['elections_count']}")
    print(f"   By-elections: {summary['byelections_count']} | Candidates: {summary['candidates_count']}")

if __name__ == "__main__":
    main()
