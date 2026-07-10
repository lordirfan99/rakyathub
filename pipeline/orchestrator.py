# ============================================================
# ORCHESTRATOR — Pipeline entry point
# ============================================================
# Usage: python orchestrator.py --match "Spain vs Belgium"
#        python orchestrator.py --league world_cup --scan
#        python orchestrator.py --cron check_odds
# ============================================================

import os, sys, json, yaml, argparse
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_layer import (
    load_dataset_teams, get_dataset_probability,
    get_upcoming_matches, my_to_decimal
)
from model_layer import (
    expected_goals, dixon_coles_model, devig_polymarket,
    calc_edge, quarter_kelly, full_ensemble
)
from output_layer import format_analysis, save_analysis

# ============================================================
# LOAD CONFIG
# ============================================================

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# ============================================================
# MATCH ANALYSIS PIPELINE
# ============================================================

def analyze_match(home, away, date, stage, league_cfg):
    """
    Run full analysis pipeline for a single match.
    Returns dict with all results.
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING: {home} vs {away} ({date})")
    print(f"{'='*60}")
    
    config = load_config()
    models_output = {}
    
    # LAYER 1: Dataset features (49K matches)
    print("\n[1/6] Dataset Model...")
    dataset_path = league_cfg.get("data_path", "./") + "wc_teams.csv"
    # Fallback to root
    if not os.path.exists(dataset_path):
        dataset_path = config.get("data_sources", {}).get("dataset", {}).get("path", "../wc2026_teams.csv")
    
    teams_data = load_dataset_teams(dataset_path)
    if teams_data:
        ds_result = get_dataset_probability(home, away, teams_data)
        models_output["Dataset"] = {
            "1X2": (ds_result["Team A Win"], ds_result["Draw"], ds_result["Team B Win"]),
        }
        models_output["Dataset"]["features"] = ds_result["features"]
        print(f"  → {home} {ds_result['Team A Win']*100:.1f}% | Draw {ds_result['Draw']*100:.1f}% | {away} {ds_result['Team B Win']*100:.1f}%")
    
    # LAYER 2: Polymarket (supplied via MCP or manual)
    print("\n[2/6] Polymarket calibration...")
    poly_1x2 = [0.595, 0.245, 0.170]
    dv_1x2, vig = devig_polymarket(*poly_1x2)
    dv_ou, _ = devig_polymarket(0.5425, 0.46)
    dv_btts, _ = devig_polymarket(0.53, 0.48)
    
    models_output["Polymarket"] = {
        "1X2": (dv_1x2[0], dv_1x2[1], dv_1x2[2]),
        "O/U": {"O 2.5": dv_ou[0]},
        "BTTS": (dv_btts[0], dv_btts[1]),
    }
    print(f"  → {home} {dv_1x2[0]*100:.1f}% | Draw {dv_1x2[1]*100:.1f}% | {away} {dv_1x2[2]*100:.1f}%")
    
    # LAYER 3: 12SPORT (supplied via browser scrape)
    print("\n[3/6] 12SPORT odds...")
    ts_odds = {
        "Spain Win": {"my": 0.65, "my_type": "pos", "dec": 1.65},
        "Draw": {"my": -0.346, "my_type": "neg", "dec": 3.89},
        "Belgium Win": {"my": -0.2326, "my_type": "neg", "dec": 5.30},
        "O 2.5": {"my": 0.80, "my_type": "pos", "dec": 1.80},
        "U 2.5": {"my": -0.9804, "my_type": "neg", "dec": 2.02},
        "BTTS Yes": {"my": 0.81, "my_type": "pos", "dec": 1.81},
        "BTTS No": {"my": -0.9901, "my_type": "neg", "dec": 2.01},
    }
    models_output["12SPORT"] = ts_odds
    print(f"  → {home} @ {ts_odds.get(home + ' Win', {}).get('dec', '?')}")
    
    # LAYER 4: xGscore
    print("\n[4/6] xGscore model...")
    home_xg = 1.98
    home_xga = 0.32
    away_xg = 2.15
    away_xga = 1.27
    league_avg = league_cfg["league_avg_xg"]
    
    home_att = home_xg / league_avg
    home_def = home_xga / league_avg
    away_att = away_xg / league_avg
    away_def = away_xga / league_avg
    
    lam_home = expected_goals(home_att, away_def, league_avg, league_cfg.get("home_advantage", 0))
    lam_away = expected_goals(away_att, home_def, league_avg, 0)
    
    rho = config["models"]["dixon_coles"]["rho"]
    dc_result = dixon_coles_model(lam_home, lam_away, rho, config["models"]["dixon_coles"]["max_goals"])
    models_output["Dixon-Coles"] = dc_result
    print(f"  → λ {home}={lam_home:.3f}, λ {away}={lam_away:.3f}")
    print(f"  → {home} {dc_result['1X2'][0]*100:.1f}% | Draw {dc_result['1X2'][1]*100:.1f}% | {away} {dc_result['1X2'][2]*100:.1f}%")
    
    # LAYER 5: Opta
    print("\n[5/6] Opta supercomputer...")
    opta_home = 0.593
    opta_draw = 0.224
    opta_away = 0.183
    models_output["Opta"] = {
        "1X2": (opta_home, opta_draw, opta_away),
        "O/U": {"O 2.5": 0.52},
    }
    print(f"  → {home} {opta_home*100:.1f}% | Draw {opta_draw*100:.1f}% | {away} {opta_away*100:.1f}%")
    
    # XGSCORE standalone
    xg_home = 0.62
    xg_draw = 0.21
    xg_away = 0.17
    models_output["xGscore"] = {
        "1X2": (xg_home, xg_draw, xg_away),
        "O/U": {"O 2.5": 0.52},
        "BTTS": (0.47, 0.53),
    }
    
    # LAYER 6: Ensemble
    print("\n[6/6] Ensemble consensus...")
    ensemble = full_ensemble(home, away, models_output, config)
    
    h_prob, d_prob, a_prob = ensemble["1X2"]
    ou_o, ou_u = ensemble["O/U 2.5"]
    btts_y, btts_n = ensemble["BTTS"]
    print(f"\n  ✅ FINAL: {home} {h_prob*100:.1f}% | Draw {d_prob*100:.1f}% | {away} {a_prob*100:.1f}%")
    print(f"  ✅ O 2.5: {ou_o*100:.1f}% | BTTS Yes: {btts_y*100:.1f}%")
    
    # Edge calculations
    edges = {}
    kelly = {}
    for market, odds_data in ts_odds.items():
        if isinstance(odds_data, dict) and "dec" in odds_data:
            dec_odds = odds_data["dec"]
            # Map to ensemble probability
            if market == home + " Win":
                prob = h_prob
            elif market == "Draw":
                prob = d_prob
            elif market == away + " Win":
                prob = a_prob
            elif market == "O 2.5":
                prob = ou_o
            elif market == "U 2.5":
                prob = ou_u
            elif market == "BTTS Yes":
                prob = btts_y
            elif market == "BTTS No":
                prob = btts_n
            else:
                continue
            
            edge, implied = calc_edge(prob, dec_odds)
            qk = quarter_kelly(prob, dec_odds)
            fair = 1 / prob if prob > 0 else 999
            
            edges[market] = {"edge": edge, "prob": prob, "odds": dec_odds, "fair": fair, "implied": implied}
            kelly[market] = {"prob": prob, "odds": dec_odds, "kelly": qk/0.25 if qk > 0 else 0, "qkelly": qk}
    
    # Format output
    output = format_analysis(home, away, date, stage, {}, models_output, ensemble, edges, kelly)
    
    # Save
    save_path = config.get("output", {}).get("save_path", "./outputs/")
    filepath = save_analysis(home, away, date, output, save_path)
    print(f"\n  💾 Saved: {filepath}")
    
    return output, filepath, ensemble, edges


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Football Betting Pipeline")
    parser.add_argument("--match", type=str, help="Match name, e.g. 'Spain vs Belgium'")
    parser.add_argument("--home", type=str, help="Home team name")
    parser.add_argument("--away", type=str, help="Away team name")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Match date")
    parser.add_argument("--stage", type=str, default="Quarterfinal", help="Match stage")
    parser.add_argument("--league", type=str, default="world_cup", help="League: world_cup | premier_league")
    parser.add_argument("--scan", action="store_true", help="Scan upcoming matches")
    parser.add_argument("--cron", type=str, help="Cron job: check_odds | daily_scan")
    
    args = parser.parse_args()
    
    config = load_config()
    league_cfg = config["league"][args.league]
    
    if args.scan:
        matches = get_upcoming_matches(args.league)
        print(f"\nUpcoming {args.league.upper()} matches:")
        for m in matches:
            print(f"  {m['date']} {m['time']}: {m['home']} vs {m['away']}")
    
    elif args.cron == "check_odds":
        print(f"[{datetime.now().isoformat()}] CRON: Checking odds...")
        # Would run the browser scrape here
    
    elif args.match:
        parts = args.match.split(" vs ")
        home = parts[0].strip()
        away = parts[1].strip() if len(parts) > 1 else args.away
        analyze_match(home, away, args.date, args.stage, league_cfg)
    
    elif args.home and args.away:
        analyze_match(args.home, args.away, args.date, args.stage, league_cfg)
    
    else:
        print("Usage: python orchestrator.py --home Spain --away Belgium")
        print("       python orchestrator.py --match 'Spain vs Belgium'")
        print("       python orchestrator.py --scan")
