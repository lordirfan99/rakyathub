# ============================================================
# MODEL LAYER — All prediction models
# ============================================================
# Dixon-Coles (tau + time decay), Poisson, Dataset Model,
# Polymarket calibration, Ensemble weighting
# ============================================================

import math, json
from datetime import datetime

# ============================================================
# POISSON FUNCTIONS
# ============================================================

def poisson_pmf(k, lam):
    """P(X = k) for Poisson(lam)"""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

def poisson_cdf(k, lam):
    """P(X ≤ k)"""
    return sum(poisson_pmf(i, lam) for i in range(k + 1))

def expected_goals(attack_ratio, defence_ratio, league_avg, home_adv=0):
    """
    Compute expected goals λ using strength ratios.
    λ = league_avg × attack_ratio × defence_ratio × (1 + home_adv)
    """
    return league_avg * attack_ratio * defence_ratio * (1 + home_adv)

# ============================================================
# DIXON-COLES TAU CORRECTION
# ============================================================

def tau_correction(lam_h, lam_a, rho, h_goals, a_goals):
    """
    Dixon-Coles τ correction for low-score dependency.
    When rho < 0: 0-0 and 1-1 inflated, 1-0 and 0-1 deflated.
    """
    if h_goals == 0 and a_goals == 0:
        return 1 - lam_h * lam_a * rho
    elif h_goals == 0 and a_goals == 1:
        return 1 + lam_h * rho
    elif h_goals == 1 and a_goals == 0:
        return 1 + lam_a * rho
    elif h_goals == 1 and a_goals == 1:
        return 1 - rho
    else:
        return 1.0

# ============================================================
# DIXON-COLES FULL MODEL
# ============================================================

def dixon_coles_model(lam_home, lam_away, rho=-0.06, max_goals=7):
    """
    Full Dixon-Coles model: joint scoreline matrix with tau correction.
    Returns dict with all market probabilities.
    """
    # Build joint matrix
    dc_matrix = {}
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            joint = poisson_pmf(h, lam_home) * poisson_pmf(a, lam_away)
            tau = tau_correction(lam_home, lam_away, rho, h, a)
            dc_matrix[(h, a)] = joint * tau
    
    # Renormalize
    total = sum(dc_matrix.values())
    for k in dc_matrix:
        dc_matrix[k] /= total
    
    # Derive market probabilities
    home_win = sum(p for (h, a), p in dc_matrix.items() if h > a)
    draw = sum(p for (h, a), p in dc_matrix.items() if h == a)
    away_win = sum(p for (h, a), p in dc_matrix.items() if h < a)
    
    over = {}
    under = {}
    for line in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]:
        goal_threshold = int(line) + 1
        over[line] = sum(p for (h, a), p in dc_matrix.items() if h + a >= goal_threshold)
        under[line] = 1 - over[line]
    
    btts_yes = sum(p for (h, a), p in dc_matrix.items() if h >= 1 and a >= 1)
    btts_no = 1 - btts_yes
    
    # Team totals
    home_o05 = sum(p for (h, a), p in dc_matrix.items() if h >= 1)
    away_o05 = sum(p for (h, a), p in dc_matrix.items() if a >= 1)
    home_cs = sum(p for (h, a), p in dc_matrix.items() if a == 0)
    away_cs = sum(p for (h, a), p in dc_matrix.items() if h == 0)
    
    # Exact scores (top 12)
    sorted_scores = sorted(dc_matrix.items(), key=lambda x: -x[1])
    exact_scores = {f"{h}-{a}": round(p, 6) for (h, a), p in sorted_scores[:12]}
    
    return {
        "1X2": (home_win, draw, away_win),
        "O/U": {f"O {line}": over[line] for line in [1.5, 2.5, 3.5, 4.5]},
        "U/U": {f"U {line}": under[line] for line in [1.5, 2.5, 3.5, 4.5]},
        "BTTS": (btts_yes, btts_no),
        "Team O 0.5": (home_o05, away_o05),
        "Clean Sheet": (home_cs, away_cs),
        "Exact Scores": exact_scores,
        "lambda": (lam_home, lam_away),
        "matrix_sum": total,
    }

# ============================================================
# TIME-DECAY WEIGHTING
# ============================================================

def time_weight(days_ago, xi=0.0065):
    """Exponential time-decay weight."""
    return math.exp(-xi * days_ago)

# ============================================================
# DE-VIG & EDGE CALCULATION
# ============================================================

def devig_polymarket(*probs):
    """Proportional de-vig: normalize to sum 100%."""
    total = sum(probs)
    vig = total - 1.0
    devigged = [p / total for p in probs]
    return devigged, vig * 100

def calc_edge(poly_prob, dec_odds):
    """
    Edge% = ((Polymarket_Prob / 12SPORT_Implied_Prob) - 1) × 100
    Positive = value (Polymarket says more likely than odds suggest)
    """
    implied = 1 / dec_odds
    edge = ((poly_prob / implied) - 1) * 100
    return edge, implied

def classify_edge(edge):
    if edge > 20:
        return "🚀", "Significant"
    elif edge > 5:
        return "✅", "Good"
    elif edge > -5:
        return "⚪", "Neutral"
    else:
        return "❌", "Negative"

# ============================================================
# KELLY STAKING
# ============================================================

def quarter_kelly(p, dec_odds):
    """Quarter Kelly Criterion for stake sizing."""
    b = dec_odds - 1
    if b <= 0:
        return 0.0
    q = 1 - p
    k = (p * b - q) / b
    return max(0.0, k) * 0.25

# ============================================================
# ENSEMBLE / CONSENSUS
# ============================================================

def weighted_consensus(source_probs, weights):
    """
    Weighted ensemble of multiple probability sources.
    source_probs: [{"Polymarket": 0.59, ...}, ...]
    weights: {"Polymarket": 0.40, ...}
    """
    normalized_weights = {}
    total_w = sum(weights.get(s, 0.05) for s in source_probs)
    
    weighted = 0.0
    for source, prob in source_probs.items():
        w = weights.get(source, 0.05) / total_w
        weighted += prob * w
    
    return weighted

def full_ensemble(home, away, models_output, weights_cfg):
    """
    Combine all model outputs into final consensus probabilities.
    """
    weights = weights_cfg["models"]["weights"]
    
    # Extract 1X2 from each model
    spain_sources = {}
    draw_sources = {}
    belgium_sources = {}
    
    for source, data in models_output.items():
        if "1X2" in data:
            spain_sources[source] = data["1X2"][0]
            draw_sources[source] = data["1X2"][1]
            belgium_sources[source] = data["1X2"][2]
    
    # Weighted consensus
    home_prob = weighted_consensus(spain_sources, weights)
    draw_prob = weighted_consensus(draw_sources, weights)
    away_prob = weighted_consensus(belgium_sources, weights)
    
    # Renormalize
    total = home_prob + draw_prob + away_prob
    home_prob, draw_prob, away_prob = home_prob/total, draw_prob/total, away_prob/total
    
    # O/U consensus
    ou_sources = {}
    for source, data in models_output.items():
        if "O/U" in data and "O 2.5" in data["O/U"]:
            ou_sources[source] = data["O/U"]["O 2.5"]
    
    ou_weights = {"Polymarket": 0.50, "Opta": 0.20, "xGscore": 0.15, "Dixon-Coles": 0.15}
    ou_consensus = weighted_consensus(ou_sources, ou_weights)
    
    # BTTS consensus
    btts_sources = {}
    for source, data in models_output.items():
        if "BTTS" in data:
            btts_sources[source] = data["BTTS"][0]
    
    btts_weights = {"Polymarket": 0.50, "xGscore": 0.20, "Dixon-Coles": 0.30}
    btts_consensus = weighted_consensus(btts_sources, btts_weights)
    
    return {
        "1X2": (home_prob, draw_prob, away_prob),
        "O/U 2.5": (ou_consensus, 1 - ou_consensus),
        "BTTS": (btts_consensus, 1 - btts_consensus),
        "sources": {
            "1X2": {"home": spain_sources, "draw": draw_sources, "away": belgium_sources},
            "O/U": ou_sources,
            "BTTS": btts_sources,
        }
    }
