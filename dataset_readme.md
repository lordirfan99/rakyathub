---
license: mit
task_categories:
- tabular-classification
- tabular-regression
language:
- en
tags:
- football
- soccer
- sports
- predictions
- world-cup
- elo
- match-prediction
size_categories:
- 10K<n<100K
---

# Football Predictions Dataset

International football match dataset used to train an ML prediction system (CatBoost + Poisson/LightGBM ensemble) that predicts win/draw/loss probabilities and expected goals for any match between two national teams.

Used to generate [World Cup 2026 predictions](https://github.com/adibmed/football_predictions) — both pure ML and LLM consensus (Claude, GPT-5.5, Gemini, DeepSeek, Grok, Qwen).

## Dataset contents

### `output/` — ML-ready engineered features

| File | Rows | Description |
|---|---|---|
| `01_matches_all.csv` | ~49,000 | Full feature matrix used for training. All international matches 1872–2026 with 191 engineered features. |
| `02_matches_with_odds.csv` | ~8,000 | Subset with bookmaker odds attached. |
| `03_wc_history.csv` | ~900 | All World Cup matches with full stats. |
| `04_wc2026_teams.csv` | 48 | WC 2026 qualified teams with current squad data. |

### `data/worldcup/` — Raw World Cup data

| File | Description |
|---|---|
| `matches.csv` | All WC matches with scores, venue, attendance |
| `match_stats.csv` | xG, shots, possession, passes, cards per match |
| `lineups.csv` | Starting XIs and substitutes |
| `incidents.csv` | Goals, cards, subs with minute timestamps |
| `players.csv` | Player-level data with ratings |
| `standings.csv` | Group stage standings by tournament |
| `teams.csv` | Team metadata |
| `h2h_records.csv` | Head-to-head records between all WC teams |
| `tournaments.json` | Tournament metadata |

## Features (01_matches_all.csv — 191 columns)

Key feature groups:
- **ELO ratings** — pre-match ELO for both teams, delta over last 5/10 matches
- **FIFA rankings** — monthly rank + points, rank differential
- **Form** — last 3/5/10 match W-D-L, goals for/against
- **Squad** — Transfermarkt market value, squad size, avg caps
- **Player ELO** — top-5 and top-11 player ratings (pelo)
- **H2H** — historical head-to-head record
- **Match context** — neutral venue, tournament type, days rest
- **xG** — expected goals from SofaScore (WC matches)
- **Bookmaker odds** — pre-match odds from ~8 bookmakers (~8k matches)

## Model performance

Trained on ~49,000 matches (1872–2026), backtested on 6 World Cup tournaments:

| Model | Accuracy | Log Loss |
|---|---|---|
| CatBoost (multiclass) | 59.7% | 0.913 |
| Poisson / LightGBM xG | 60.4% | 0.909 |
| Bookmaker baseline | ~58–62% | — |
| Random baseline | 33.3% | — |

## World Cup 2026 predictions

Generated June 2026 using this dataset:

**ML model:** Spain 22.1% 🏆 · Argentina 14.9% · France 9.6%

**LLM consensus** (6 frontier models): Argentina 28.7% 🏆 · Spain 12.0% · England 11.6%

Full results: [github.com/adibmed/football_predictions](https://github.com/adibmed/football_predictions)

## Data sources

| Source | Content |
|---|---|
| International matches | All international results 1872–2026 |
| ELO ratings | eloratings.net |
| FIFA rankings | Monthly rankings + points |
| Transfermarkt | Squad market values, caps |
| SofaScore | xG, lineups, match stats, player ratings |
| Bookmaker odds | Pre-match odds ~8k matches |
