# ============================================================
# PREMIER LEAGUE EXTENSION PLAN
# ============================================================
# How to scale the World Cup pipeline to Premier League
# ============================================================

# ─── WHAT CHANGES FROM WORLD CUP ───

# 1. DATA VOLUME
# World Cup: 104 matches, 48 teams, max 7 games/team
# Premier League: 380 matches/season, 20 teams, 38 games/team
# → Need 10× more data throughput

# 2. DATA SOURCES (PL-specific)
dataset:
  source: "eatpizzanot/soccer-dataset"  # 378K matches on GitHub
  features:
    - match_stats.csv (258K rows: xG, shots, corners, cards)
    - odds.csv (220K rows: closing odds from multiple books)
    - fixture_lineups.csv (409K rows: starting XI)
  update: "Daily via API-Football"

# Additional PL sources:
#   - football-data.co.uk → free CSV, updated weekly
#   - Understat → xG per match for top 5 leagues
#   - FBref (until Jan 2026) → historical data cached

# 3. LEAGUE CONFIG
league_avg_xg: 1.50  # PL typical
league_avg_xga: 1.20
home_advantage: 0.21  # Standard PL home edge
time_decay_xi: 0.0065  # 107-day half-life (slower than WC)

# 4. MODEL ADJUSTMENTS
dixon_coles:
  rho: -0.08  # PL typically needs stronger tau correction
  training_window: 38  # Full season
  update_frequency: "Matchweek"

# 5. INFRASTRUCTURE UPGRADE NEEDED
infrastructure:
  - "Historical database: Download 378K match dataset (113MB)"
  - "Feature engineering: Create rolling form features (last 5/10/38 games)"
  - "Model retraining: Weekly CatBoost fit on latest data"
  - "Odds pipeline: football-data.co.uk CSV ingestion"
  - "xG pipeline: Understat scraper for match-level xG"

# 6. WHAT STAYS THE SAME (reusable)
reusable:
  - "Polymarket calibration MCP (same API)"
  - "12SPORT scraping (12play21.com — same platform)"
  - "Dixon-Coles model code (same logic, different params)"
  - "De-vig + Edge calculation (formula unchanged)"
  - "Kelly staking (same fraction)"
  - "match-analysis-template output (same format)"
  - "Cron scheduling (same infrastructure)"

# 7. PIPELINE TIMELINE
timeline:
  phase_1: "Install 378K dataset + configure PL config"
  phase_2: "Build feature engineering pipeline (rolling averages)"
  phase_3: "Train CatBoost model on 5 seasons of PL data"
  phase_4: "Set up weekly cron for matchday scanning"
  phase_5: "Backtest on 2023-24 and 2024-25 PL seasons"

# 8. QUICK START FOR PL
"""
# Switch to PL mode:
python orchestrator.py --league premier_league --scan

# Analyze a PL match:
python orchestrator.py --home "Manchester City" --away "Arsenal" --league premier_league

# Cron for PL matchday:
cronjob action=create name=pl-matchday-scan prompt="..." schedule="0 9 * * 0,6"
"""
