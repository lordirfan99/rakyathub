"""
pipeline/odds_pipeline.py — Automated odds update + dashboard deploy
Uses the-odds-api (not Selenium — headless Chrome can't handle 12Play bot detection).

Flow:
  1. Fetch live odds from the-odds-api (Pinnacle/Matchbook)
  2. Update data.json with fresh 1xBet-style odds + bookies structure
  3. Preserve manually collected 12Play odds if present
  4. npm build + netlify deploy
"""

import json, os, subprocess, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "public" / "data.json"
API_KEY = "b45c8f0693e8a7912baf2449e98d6fb8"

TEAM_MAP = {
    "Spain": ["Spain"],
    "Belgium": ["Belgium"],
    "Norway": ["Norway"],
    "England": ["England"],
    "Argentina": ["Argentina"],
    "Switzerland": ["Switzerland"],
}

def fmt_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_odds_from_api():
    """Hit the-odds-api for upcoming football matches."""
    # Try both sport keys (World Cup 2026 might be in either)
    sport_keys = ["soccer_fifa_world_cup", "soccer_world_cup"]
    import urllib.request
    for sport_key in sport_keys:
        url = (
            f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
            f"?apiKey={API_KEY}&regions=eu,au&markets=h2h,spreads,totals"
            f"&oddsFormat=decimal"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
            if data:
                print(f"[API] Got {len(data)} matches from {sport_key}")
                return data
            else:
                print(f"[API] No matches from {sport_key}, trying next...")
        except Exception as e:
            print(f"[API] {sport_key}: {e}")
    print("[API] All sport keys failed")
    return []

def parse_api_odds(api_matches):
    """Transform API response into data.json match entries."""
    now_iso = fmt_now()
    
    # Load existing data to preserve 12Play odds
    existing = {}
    if DATA_FILE.exists():
        try:
            existing_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            for m in existing_data.get("matches", []):
                existing[m["id"]] = m
        except Exception:
            pass

    matches = []
    
    for am in api_matches:
        home = am.get("home_team", "")
        away = am.get("away_team", "")
        
        # Match API team names to our match IDs
        matchup = (home.lower(), away.lower())
        match_id = None
        if ("norway" in matchup[0] and "england" in matchup[1]) or \
           ("england" in matchup[0] and "norway" in matchup[1]):
            match_id = "eng_nor_03"
        elif ("argentina" in matchup[0] and "switzerland" in matchup[1]) or \
             ("switzerland" in matchup[0] and "argentina" in matchup[1]):
            match_id = "arg_sui_04"
        elif ("france" in matchup[0] and "spain" in matchup[1]) or \
             ("spain" in matchup[0] and "france" in matchup[1]):
            match_id = "fra_esp_sf"
        elif "spain" in matchup[0] or "spain" in matchup[1]:
            match_id = "esp_bel_01"
        
        if not match_id:
            print(f"[API] Skipping unrecognized match: {home} vs {away}")
            continue

        # Find first bookmaker with h2h market
        h2h_odds = {}
        spread_odds = {}
        total_odds = {}
        bookmaker_name = ""
        for bm in am.get("bookmakers", []):
            for market in bm.get("markets", []):
                key = market.get("key", "")
                outcomes = market.get("outcomes", [])
                if key == "h2h" and not h2h_odds:
                    for o in outcomes:
                        h2h_odds[o.get("name", "")] = o.get("price", 0)
                    bookmaker_name = bm.get("title", "Unknown")
                elif key == "spreads" and not spread_odds:
                    for o in outcomes:
                        spread_odds[o.get("name", "")] = {
                            "point": o.get("point", 0),
                            "price": o.get("price", 0),
                        }
                elif key == "totals" and not total_odds:
                    for o in outcomes:
                        total_odds[o.get("name", "")] = {
                            "point": o.get("point", 0),
                            "price": o.get("price", 0),
                        }
            # If we have h2h, we're good — use this bookmaker
            if h2h_odds:
                break

        home_odd = h2h_odds.get(home, 0)
        away_odd = h2h_odds.get(away, 0)
        # Find draw — the outcome that's neither home nor away
        draw_odd = 0
        for k, v in h2h_odds.items():
            if k != home and k != away:
                draw_odd = v
                break

        if not home_odd:
            continue

        # Find O/U 2.5 specifically
        over_25 = 0
        under_25 = 0
        for name, data in total_odds.items():
            pt = data.get("point", 0)
            if abs(pt - 2.5) < 0.1:
                if "Over" in name:
                    over_25 = data["price"]
                else:
                    under_25 = data["price"]

        # Determine stage
        stage = "Quarterfinal"
        if match_id in ("fra_esp_sf",):
            stage = "Semifinal"

        # Build match entry — preserve 12Play bookies from existing data
        match_entry = {
            "id": match_id,
            "home_team": home,
            "away_team": away,
            "venue": "World Cup 2026",
            "stage": stage,
            "date": am.get("commence_time", "")[:10],
            "time": "",
            "highest_edge_status": "⚪",
            "home_odds": round(home_odd, 3),
            "draw_odds": round(draw_odd, 3),
            "away_odds": round(away_odd, 3),
            "markets": {
                "1x2": {"home": round(home_odd, 3), "draw": round(draw_odd, 3), "away": round(away_odd, 3)},
                "over_under_25": {"over": round(over_25, 3) if over_25 else 1.80, "under": round(under_25, 3) if under_25 else 2.00},
            },
            "bookies": {
                "1xbet": {
                    "1x2": {"home": round(home_odd, 3), "draw": round(draw_odd, 3), "away": round(away_odd, 3)},
                    "over_under_25": {"over": round(over_25, 3) if over_25 else 1.80, "under": round(under_25, 3) if under_25 else 2.00},
                },
            },
            "analysis": {
                "sport_raw": {"home": round(home_odd, 3), "draw": round(draw_odd, 3), "away": round(away_odd, 3), "vig": 0.035},
                "polymarket_devig": {"home": 0.55, "draw": 0.25, "away": 0.20},
                "triangulation_1x2": {
                    "polymarket": [55.0, 25.0, 20.0],
                    "dataset": [55.0, 25.0, 20.0],
                    "opta": [55.0, 25.0, 20.0],
                    "xgscore": [55.0, 25.0, 20.0],
                    "dixon_coles": [55.0, 25.0, 20.0],
                    "ensemble": [55.0, 25.0, 20.0],
                },
                "triangulation_ou": {
                    "polymarket": [52.0, 48.0],
                    "xgscore": [52.0, 48.0],
                    "opta": [52.0, 48.0],
                    "dixon_coles": [52.0, 48.0],
                    "ensemble": [52.0, 48.0],
                },
                "triangulation_btts": {
                    "polymarket": [50.0, 50.0],
                    "xgscore": [50.0, 50.0],
                    "dixon_coles": [50.0, 50.0],
                    "ensemble": [50.0, 50.0],
                },
                "edge_summary": [
                    {"market": f"{home} Win", "edge": -2.0, "status": "⚪", "quarter_kelly_stake": 0},
                    {"market": "Draw", "edge": -4.0, "status": "⚪", "quarter_kelly_stake": 0},
                    {"market": f"{away} Win", "edge": -10.0, "status": "❌", "quarter_kelly_stake": 0},
                    {"market": "O 2.5", "edge": 0.0, "status": "⚪", "quarter_kelly_stake": 0},
                    {"market": "U 2.5", "edge": 0.0, "status": "⚪", "quarter_kelly_stake": 0},
                ],
                "narrative": {
                    "form": f"{home} vs {away} -- World Cup Quarterfinal.",
                    "injuries": "TBD -- check latest team news.",
                    "tactical": "Awaiting lineup confirmation.",
                    "data_source": f"the-odds-api ({bookmaker_name})",
                },
            },
        }

        # Preserve 12Play odds from existing data
        existing_match = existing.get(match_id)
        if existing_match:
            # Copy over bookies from existing data if present
            if existing_match.get("bookies"):
                if "bookies" not in match_entry:
                    match_entry["bookies"] = {}
                if existing_match["bookies"].get("12play"):
                    match_entry["bookies"]["12play"] = existing_match["bookies"]["12play"]
                # Also copy 1xbet bookies from API if our own 1xbet is from API
                if existing_match["bookies"].get("1xbet"):
                    # Keep API odds as 1xbet, but supplement with existing data
                    if "1xbet" not in match_entry["bookies"] or not match_entry["bookies"]["1xbet"].get("1x2"):
                        match_entry["bookies"]["1xbet"] = existing_match["bookies"]["1xbet"]
            # Preserve manually set time, venue, stage
            if existing_match.get("time"): match_entry["time"] = existing_match["time"]
            if existing_match.get("venue"): match_entry["venue"] = existing_match["venue"]
            # Preserve full analysis if available
            if existing_match.get("analysis", {}).get("triangulation_1x2", {}).get("ensemble"):
                match_entry["analysis"] = existing_match["analysis"]
                match_entry["analysis"]["sport_raw"] = {"home": round(home_odd, 3), "draw": round(draw_odd, 3), "away": round(away_odd, 3), "vig": 0.035}
                match_entry["analysis"]["data_source"] = "the-odds-api + existing analysis"
            # Recalculate edges
            edges = match_entry["analysis"].get("edge_summary", [])
            for e in edges:
                if e["market"] == f"{home} Win":
                    dv = existing_match.get("analysis", {}).get("polymarket_devig", {}).get("home", 0.55)
                    imp = 1/home_odd if home_odd else 0.55
                    e["edge"] = round(((dv / imp) - 1) * 100, 1)
                elif e["market"] == "Draw":
                    dv = existing_match.get("analysis", {}).get("polymarket_devig", {}).get("draw", 0.25)
                    imp = 1/draw_odd if draw_odd else 0.25
                    e["edge"] = round(((dv / imp) - 1) * 100, 1)
                elif e["market"] == f"{away} Win":
                    dv = existing_match.get("analysis", {}).get("polymarket_devig", {}).get("away", 0.20)
                    imp = 1/away_odd if away_odd else 0.20
                    e["edge"] = round(((dv / imp) - 1) * 100, 1)

        matches.append(match_entry)
        print(f"[API] {home} vs {away}: {home_odd} / {draw_odd} / {away_odd}")

    # Add any existing matches not in API response (keep 12Play data)
    for mid, em in existing.items():
        if not any(m["id"] == mid for m in matches):
            em["analysis"]["narrative"]["data_source"] = "Cached — no live API update"
            matches.append(em)
            print(f"[API] Preserved cached match: {mid}")

    return matches

def main():
    print(f"{'='*50}")
    print(f"ODDS PIPELINE — {fmt_now()}")
    print(f"{'='*50}")

    # Step 1: Fetch from API
    api_matches = fetch_odds_from_api()
    if not api_matches:
        print("[!] API returned nothing — keeping existing data.json")
        # Still build & deploy to refresh timestamp
        if DATA_FILE.exists():
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            data["system_status"]["last_updated"] = fmt_now()
            data["system_status"]["data_source"] = "Cached (API unavailable)"
            DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        else:
            print("[!] No data.json exists — aborting")
            return 1
    else:
        # Step 2: Parse & build
        matches = parse_api_odds(api_matches)
        
        # Build data
    
        # Determine best bookmaker name from processed matches
        best_bookie = "API"
    
        now_iso = fmt_now()
        data = {
            "system_status": {
                "last_updated": now_iso,
                "bankroll_rm": 30,
                "data_source": f"the-odds-api ({best_bookie}) + 12Play MY",
            },
            "matches": matches,
        }
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[✓] Written {len(matches)} matches to data.json")

    # Step 3: Build
    print("\n[Build] npm run build...")
    build = subprocess.run("npm run build", cwd=str(BASE_DIR), capture_output=True, text=True, timeout=120, shell=True)
    if build.returncode != 0:
        print(f"[!] Build failed: {build.stderr[:300]}")
        return 1
    print(f"[✓] Build OK ({len(build.stdout)} chars)")

    # Step 4: Deploy
    print("\n[Deploy] Deploying to Netlify...")
    deploy = subprocess.run(
        "npx netlify-cli deploy --dir=dist --prod --site 3d225a22-04e0-40fa-9629-0fb0f9cb8d40",
        cwd=str(BASE_DIR), capture_output=True, text=True, timeout=120, shell=True,
    )
    if deploy.returncode == 0:
        print(f"[✓] Deploy complete!")
        for line in deploy.stdout.split("\n"):
            if "Production URL" in line or "Unique deploy" in line:
                print(f"     {line.strip()}")
    else:
        print(f"[!] Deploy failed: {deploy.stderr[:300]}")
        return 1

    print(f"\nDone at {fmt_now()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
