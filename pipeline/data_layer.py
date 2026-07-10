# ============================================================
# DATA LAYER — Fetch from all sources
# ============================================================
# Polymarket (MCP), 12SPORT (browser), xGscore (web),
# Dataset (HF), Opta (web)
# ============================================================

import json, csv, os, math
from datetime import datetime, timedelta

# ============================================================
# 1. POLYMARKET DATA
# ============================================================

def fetch_polymarket(match_name, mcp_execute_func):
    """
    Fetch Polymarket prices via MCP connection.
    Returns dict: {market_name: probability}
    """
    # Expected markets to check
    markets = {
        "1X2": ["Team A Win", "Draw", "Team B Win"],
        "O/U": ["Over X.5", "Under X.5"],
        "BTTS": ["Yes", "No"],
        "Spread": ["Team A -X.5", "Team B +X.5"],
    }
    # Actual call handled by orchestrator via MCP
    return {}

# ============================================================
# 2. 12SPORT DATA
# ============================================================

def fetch_twelvesport(match_name, browser_snapshot_func):
    """
    Scrape 12SPORT live odds from 12play21.com.
    Returns dict of ALL available markets in MY format:
    {
        "1X2_Spain": {"my": 0.65, "my_type": "pos", "dec": 1.65},
        "1X2_Draw": {"my": -0.346, "my_type": "neg", "dec": 3.89},
        ...
    }
    """
    return {}

def my_to_decimal(odds, my_type):
    """Convert Malaysian odds to decimal."""
    if my_type == "pos":
        return 1 + odds
    else:
        return 1 + (1 / abs(odds))

def decimal_to_my(dec_odds):
    """Convert decimal odds to Malaysian format."""
    if dec_odds >= 2.0:
        return round(dec_odds - 1, 4)
    else:
        return round(-1 / (dec_odds - 1), 4)

# ============================================================
# 3. XGSCORE DATA
# ============================================================

def fetch_xgscore(league_url):
    """
    Fetch team xG data from xgscore.io.
    Returns dict: {team_name: {"xg": float, "xga": float, "matches": int}}
    """
    # Would use web_extract or browser to get the xG table
    return {}

# ============================================================
# 4. DATASET FEATURES
# ============================================================

def load_dataset_teams(dataset_path):
    """
    Load pre-cleaned dataset team features from CSV.
    Returns dict: {team_name: {feature: value}}
    """
    teams = {}
    if not os.path.exists(dataset_path):
        return teams
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            teams[row['team']] = row
    return teams

def get_dataset_probability(team_a, team_b, teams_data):
    """
    Estimate match probability from dataset features using
    ELO, composite strength, form, and MC simulation.
    """
    a = teams_data.get(team_a, {})
    b = teams_data.get(team_b, {})
    
    def sf(val, default=0.0):
        try:
            return float(val) if val and str(val).strip() else default
        except:
            return default
    
    # Extract features
    a_elo = sf(a.get('elo_2025', 0))
    b_elo = sf(b.get('elo_2025', 0))
    a_strength = sf(a.get('composite_strength', 0))
    b_strength = sf(b.get('composite_strength', 0))
    a_form = sf(a.get('recent_form_pts_avg', 0))
    b_form = sf(b.get('recent_form_pts_avg', 0))
    
    # Elo-based probability
    elo_diff = a_elo - b_elo
    elo_prob_a = 1 / (1 + 10 ** (-elo_diff / 400))
    elo_prob_b = 1 - elo_prob_a
    
    # Strength ratio
    strength_ratio = a_strength / (a_strength + b_strength) if (a_strength + b_strength) > 0 else 0.5
    
    # Form ratio
    form_ratio = a_form / (a_form + b_form) if (a_form + b_form) > 0 else 0.5
    
    # MC data
    a_mc_qf = sf(a.get('mc_quarterfinal_pct', 0)) / 100
    b_mc_qf = sf(b.get('mc_quarterfinal_pct', 0)) / 100
    
    # Blended probability
    prob_a = 0.35 * elo_prob_a + 0.35 * strength_ratio + 0.20 * form_ratio
    if (a_mc_qf + b_mc_qf) > 0:
        prob_a += 0.10 * (a_mc_qf / (a_mc_qf + b_mc_qf))
    
    # Draw estimate based on Elo proximity
    draw_prob = 0.20 + 0.08 * (1 - min(1, abs(elo_diff) / 1000))
    
    # Renormalize
    prob_b = 1 - prob_a - draw_prob
    if prob_b < 0:
        prob_b = 0.05
        prob_a = 1 - draw_prob - prob_b
    
    return {
        "Team A Win": prob_a,
        "Draw": draw_prob,
        "Team B Win": prob_b,
        "features": {
            "elo_diff": elo_diff,
            "strength_a": a_strength,
            "strength_b": b_strength,
            "form_a": a_form,
            "form_b": b_form,
        }
    }

# ============================================================
# 5. OPTA DATA
# ============================================================

def fetch_opta(match_name):
    """
    Fetch Opta supercomputer probabilities (from Opta Analyst).
    Returns dict: {"Team A Win": %, "Draw": %, "Team B Win": %}
    """
    # Typically scraped from theanalyst.com articles
    # For now returns empty — populated per match
    return {}

# ============================================================
# 6. MATCH SCHEDULE
# ============================================================

def get_upcoming_matches(league, date=None):
    """
    Get list of upcoming matches for a league.
    Returns list of dicts: [{"home": str, "away": str, "date": str, "time": str}]
    """
    if date is None:
        date = datetime.now()
    
    if league == "world_cup":
        # World Cup QF schedule
        schedule = [
            {"home": "France", "away": "Morocco", "date": "2026-07-09", "time": "22:00"},
            {"home": "Spain", "away": "Belgium", "date": "2026-07-10", "time": "03:00"},
            {"home": "England", "away": "Norway", "date": "2026-07-11", "time": "22:00"},
            {"home": "Argentina", "away": "Switzerland", "date": "2026-07-11", "time": "03:00"},
        ]
        return [m for m in schedule if m["date"] >= date.strftime("%Y-%m-%d")]
    
    elif league == "premier_league":
        # PL would be fetched from an API
        return []
    
    return []
