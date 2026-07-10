# ============================================================
# OUTPUT LAYER — Format analysis for delivery
# ============================================================
# Follows match-analysis-template (10 sections)
# Output: Telegram-ready markdown + local file save
# ============================================================

import json, os
from datetime import datetime

def format_analysis(home, away, date, stage, data, model_outputs, ensemble, edges, kelly):
    """
    Format full analysis following match-analysis-template.
    Returns markdown string ready for delivery.
    """
    sections = []
    
    # SECTION 1: Match Header
    sections.append(f"""# 🏆 {home} vs {away} — FULL ANALYSIS

## 📅 Match Info
- **Date:** {date}
- **Peringkat:** {stage}
- **Pipeline v2.0** — 6 layers: Dataset (49K) × Polymarket × 12SPORT × xGscore × Opta × Dixon-Coles
""")
    
    # SECTION 2: 12SPORT Raw Odds & Edge
    if "twelvesport" in model_outputs:
        ts = model_outputs["twelvesport"]
        sections.append("## 1️⃣ 12SPORT — RAW ODDS & EDGE\n")
        sections.append("| Market | MY Odds | Decimal | Implied | Polymarket (DV) | Edge | Call |")
        sections.append("|--------|:-:|:-:|:-:|:-:|:-:|:-:|")
        
        for m, odds in ts.items():
            if isinstance(odds, dict) and "dec" in odds:
                implied = 1 / odds["dec"]
                poly = ensemble.get("source_prob", {}).get(m, None)
                if poly:
                    edge = ((poly / implied) - 1) * 100
                    call = "🚀" if edge > 20 else ("✅" if edge > 5 else ("⚪" if edge > -5 else "❌"))
                else:
                    edge, call = None, "❓"
                
                edge_str = f"{edge:+.2f}%" if edge is not None else "N/A"
                sections.append(f"| {m:20s} | {odds.get('my_str', 'N/A'):>10s} | {odds['dec']:.2f} | {implied*100:.2f}% | {edge_str} | {call} |")
    
    # SECTION 3: 1X2 Triangulation
    sections.append("\n## 2️⃣ TRIANGULATION — 1X2\n")
    sections.append(f"| Source | {home} | Draw | {away} | Method |")
    sections.append("|--------|:-:|:-:|:-:|--------|")
    
    sources_1x2 = [
        ("Polymarket (DV)", "Zero-vig"),
        ("Dataset (49K)", "CatBoost/ELO"),
        ("Opta", "25K sims"),
        ("xGscore", "xG model"),
        ("Dixon-Coles", "τ+decay"),
    ]
    
    for src, method in sources_1x2:
        if src in ensemble["sources"]["1X2"]["home"]:
            h = ensemble["sources"]["1X2"]["home"][src] * 100
            d = ensemble["sources"]["1X2"]["draw"][src] * 100
            a = ensemble["sources"]["1X2"]["away"][src] * 100
            sections.append(f"| **{src}** | {h:.1f}% | {d:.1f}% | {a:.1f}% | {method} |")
    
    h, d, a = ensemble["1X2"]
    sections.append(f"| **Consensus** | **{h*100:.1f}%** | **{d*100:.1f}%** | **{a*100:.1f}%** | Weighted ensemble |")
    
    # SECTION 4: O/U Triangulation
    sections.append(f"\n## 3️⃣ TRIANGULATION — O/U 2.5\n")
    sections.append(f"| Source | Over 2.5 | Under 2.5 | Method |")
    sections.append(f"|--------|:-:|:-:|--------|")
    
    for src, prob in ensemble["sources"]["O/U"].items():
        sections.append(f"| **{src}** | {prob*100:.1f}% | {(1-prob)*100:.1f}% | |")
    
    ou_o, ou_u = ensemble["O/U 2.5"]
    sections.append(f"| **Consensus** | **{ou_o*100:.1f}%** | **{ou_u*100:.1f}%** | Weighted |")
    
    # SECTION 5: BTTS
    btts_y, btts_n = ensemble["BTTS"]
    sections.append(f"\n## 4️⃣ BTTS\n")
    sections.append(f"| Source | Yes | No |")
    sections.append(f"|--------|:-:|:-:|")
    for src, prob in ensemble["sources"]["BTTS"].items():
        sections.append(f"| **{src}** | {prob*100:.1f}% | {(1-prob)*100:.1f}% |")
    sections.append(f"| **Consensus** | **{btts_y*100:.1f}%** | **{btts_n*100:.1f}%** |")
    
    # SECTION 6: Dataset Insights
    if "dataset" in model_outputs:
        feat = model_outputs["dataset"].get("features", {})
        sections.append(f"\n## 5️⃣ DATASET INSIGHTS (49K matches)\n")
        sections.append(f"- **ELO Differential:** {feat.get('elo_diff', 0):+.0f} {home if feat.get('elo_diff',0) > 0 else away}")
        sections.append(f"- **Composite Strength:** {feat.get('strength_a', 0):.1f} vs {feat.get('strength_b', 0):.1f}")
        sections.append(f"- **Recent Form:** {feat.get('form_a', 0):.1f} pts/g vs {feat.get('form_b', 0):.1f} pts/g")
    
    # SECTION 7: Narrative
    sections.append(f"\n## 6️⃣ KEY FACTORS\n")
    if "narrative" in data:
        for bullet in data["narrative"]:
            sections.append(f"- {bullet}")
    
    # SECTION 8: Edge Analysis
    sections.append(f"\n## 7️⃣ EDGE vs 12SPORT\n")
    sections.append(f"| Market | Consensus | Fair Odds | 12SPORT | Edge | Call |")
    sections.append(f"|--------|:-:|:-:|:-:|:-:|:-:|")
    
    for market, edge_data in edges.items():
        call_sym, call_txt = classify_edge(edge_data.get("edge", 0))
        sections.append(f"| {market:20s} | {edge_data['prob']*100:.2f}% | {edge_data['fair']:.2f} | {edge_data['odds']:.2f} | {edge_data['edge']:+.2f}% | {call_sym} |")
    
    # SECTION 9: Kelly
    sections.append(f"\n## 8️⃣ KELLY STAKING\n")
    sections.append(f"| Market | Prob | Odds | Kelly | Q-Kelly |")
    sections.append(f"|--------|:-:|:-:|:-:|:-:|")
    for market, k in kelly.items():
        sections.append(f"| {market:20s} | {k['prob']*100:.2f}% | {k['odds']:.2f} | {k['kelly']*100:.2f}% | {k['qkelly']*100:.2f}% |")
    
    # SECTION 10: Verdict
    sections.append(f"\n## 9️⃣ VERDICT\n")
    h, d, a = ensemble["1X2"]
    ou_o, ou_u = ensemble["O/U 2.5"]
    btts_y, btts_n = ensemble["BTTS"]
    
    # Count edges
    pos_edges = sum(1 for e in edges.values() if e.get("edge", 0) > 5)
    neg_edges = sum(1 for e in edges.values() if e.get("edge", 0) < -5)
    neutral = sum(1 for e in edges.values() if -5 <= e.get("edge", 0) <= 5)
    
    verdict = f"""📊 FINAL CONSENSUS:
   {home}: {h*100:.1f}% | Draw: {d*100:.1f}% | {away}: {a*100:.1f}%
   O 2.5: {ou_o*100:.1f}% | U 2.5: {ou_u*100:.1f}%
   BTTS: {btts_y*100:.1f}% | No BTTS: {btts_n*100:.1f}%

📈 EDGE SUMMARY:
   ✅ Positive: {pos_edges} | ⚪ Neutral: {neutral} | ❌ Negative: {neg_edges}"""
    
    if pos_edges > 0:
        verdict += "\n\n💰 VALUE BETS:"
        for market, e in sorted(edges.items(), key=lambda x: -x[1].get("edge", 0)):
            if e.get("edge", 0) > 5:
                verdict += f"\n   {market} @ {e['odds']:.2f} — edge {e['edge']:+.2f}%"
    
    sections.append(verdict)
    
    return "\n".join(sections)


def classify_edge(edge):
    if edge > 20:
        return "🚀", "Significant"
    elif edge > 5:
        return "✅", "Good"
    elif edge > -5:
        return "⚪", "Neutral"
    else:
        return "❌", "Negative"


def save_analysis(home, away, date, markdown, save_path="./outputs/"):
    """Save analysis to local file."""
    os.makedirs(save_path, exist_ok=True)
    filename = f"{date}_{home}_vs_{away}.md".replace(" ", "_").replace(":", "")
    filepath = os.path.join(save_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    return filepath
