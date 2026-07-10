import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  AlertTriangle,
  TrendingUp,
  Info,
} from 'lucide-react';
import EdgeBadge from './EdgeBadge';
import TriangulationTable from './TriangulationTable';

/* ---------- helpers ---------- */
function edgeClass(edge) {
  if (edge > 20) return 'text-accent-green font-bold';
  if (edge >= 5) return 'text-green-400';
  if (edge >= -5) return 'text-muted';
  return 'text-accent-red';
}

function edgeStatusLabel(edge) {
  if (edge > 20) return { badge: '🚀', label: 'KELLY' };
  if (edge >= 5) return { badge: '✅', label: 'VALUE' };
  if (edge >= -5) return { badge: '⚪', label: 'PASS' };
  return { badge: '❌', label: 'AVOID' };
}

function fmtLocal(isoString) {
  return new Date(isoString).toLocaleTimeString('en-MY', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

export default function MatchDetail() {
  const { matchId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [maxBankrollPct, setMaxBankrollPct] = useState(10);

  useEffect(() => {
    fetch('/data.json')
      .then((r) => r.json())
      .then((d) => setData(d))
      .catch(() => {});
  }, []);

  if (!data)
    return (
      <div className="flex items-center justify-center h-screen bg-dark-900">
        <div className="text-accent-cyan text-sm animate-pulse">
          LOADING...
        </div>
      </div>
    );

  const match = data.matches.find((m) => m.id === matchId);
  if (!match)
    return (
      <div className="flex items-center justify-center h-screen bg-dark-900">
        <div className="text-accent-red text-sm">MATCH NOT FOUND</div>
      </div>
    );

  const { analysis, home_team, away_team, date, venue, stage } = match;
  const bankroll = data.system_status.bankroll_rm;

  // best edge for the header badge
  const bestEdge =
    analysis.edge_summary?.length
      ? [...analysis.edge_summary].sort((a, b) => b.edge - a.edge)[0]
      : null;

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-6">
      {/* ---- Back + Header ---- */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-muted hover:text-white text-xs mb-4 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> BACK TO DASHBOARD
        </button>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="min-w-0">
            <h1 className="text-xl font-bold text-white tracking-tight">
              {home_team}{' '}
              <span className="text-muted mx-2">vs</span> {away_team}
            </h1>
            <div className="flex flex-wrap gap-x-3 gap-y-1 text-[0.6rem] text-muted mt-1">
              <span>{date}</span>
              {venue && (
                <>
                  <span className="hidden sm:inline">·</span>
                  <span className="truncate max-w-[200px]">{venue}</span>
                </>
              )}
              <span>·</span>
              <span className="text-accent-yellow">{stage}</span>
            </div>
          </div>
          <EdgeBadge edge={bestEdge?.edge ?? null} />
        </div>
      </div>

      {/* ---- 1. 12SPORT Odds & Edge (Kau bet kat sini) ---- */}
      <div className="mb-6">
        <h2 className="section-header">1. 12SPORT MY — Real Betting Odds</h2>

        {/* 12SPORT odds — big, clear, this is where you bet */}
        <div className="card mb-3">
          <div className="text-[0.6rem] text-accent-green mb-3 uppercase tracking-wider font-bold">
            ⚡ 12play.my — Your Betting Odds
          </div>
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="bg-dark-800 rounded-lg p-3 border border-dark-600">
              <div className="text-[0.55rem] text-muted uppercase truncate mb-1">{home_team}</div>
              <div className="text-2xl font-bold text-white num-mono">{match.home_odds?.toFixed(2)}</div>
              <div className="text-[0.5rem] text-muted mt-1">
                Implied: <span className="text-white/70">{match.home_odds ? ((1 / match.home_odds) * 100).toFixed(1) : '-'}%</span>
              </div>
            </div>
            <div className="bg-dark-800 rounded-lg p-3 border border-dark-600">
              <div className="text-[0.55rem] text-muted uppercase mb-1">Draw</div>
              <div className="text-2xl font-bold text-accent-yellow num-mono">{match.draw_odds?.toFixed(2)}</div>
              <div className="text-[0.5rem] text-muted mt-1">
                Implied: <span className="text-white/70">{match.draw_odds ? ((1 / match.draw_odds) * 100).toFixed(1) : '-'}%</span>
              </div>
            </div>
            <div className="bg-dark-800 rounded-lg p-3 border border-dark-600">
              <div className="text-[0.55rem] text-muted uppercase truncate mb-1">{away_team}</div>
              <div className="text-2xl font-bold text-white num-mono">{match.away_odds?.toFixed(2)}</div>
              <div className="text-[0.5rem] text-muted mt-1">
                Implied: <span className="text-white/70">{match.away_odds ? ((1 / match.away_odds) * 100).toFixed(1) : '-'}%</span>
              </div>
            </div>
          </div>
          <div className="mt-2 text-[0.55rem] text-muted text-center">
            Total implied: <span className="text-white/70">
              {match.home_odds && match.draw_odds && match.away_odds
                ? ((1/match.home_odds + 1/match.draw_odds + 1/match.away_odds) * 100).toFixed(2)
                : '-'}%</span>
            · Vig: <span className="text-accent-yellow">
              {match.home_odds && match.draw_odds && match.away_odds
                ? ((1/match.home_odds + 1/match.draw_odds + 1/match.away_odds - 1) * 100).toFixed(2)
                : '-'}%</span>
          </div>
        </div>

        {/* Edge Comparison — 12SPORT vs Polymarket */}
        <div className="card">
          <div className="text-[0.6rem] text-muted mb-3 uppercase tracking-wider">
            📊 Edge Analysis — 12SPORT vs Polymarket (Zero-Vig Ground Truth)
          </div>
          <div className="overflow-x-auto">
            <table className="terminal-grid w-full min-w-[400px]">
              <thead>
                <tr>
                  <th className="text-left">Market</th>
                  <th className="text-right num-mono">12SPORT Implied</th>
                  <th className="text-right num-mono">Polymarket DV</th>
                  <th className="text-right num-mono">Edge %</th>
                  <th className="text-center">Call</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { market: `${home_team} Win`, imp: 1/match.home_odds, dv: analysis.polymarket_devig.home },
                  { market: 'Draw', imp: 1/match.draw_odds, dv: analysis.polymarket_devig.draw },
                  { market: `${away_team} Win`, imp: 1/match.away_odds, dv: analysis.polymarket_devig.away },
                ].map((row, i) => {
                  const edgePct = ((row.dv / row.imp) - 1) * 100;
                  let edgeClass, callLabel, callBadge;
                  if (edgePct > 20)      { edgeClass = 'text-accent-green font-bold'; callLabel = '🚀 KELLY'; callBadge = 'edge-positive-pulse inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-accent-green/20 text-accent-green'; }
                  else if (edgePct >= 5)  { edgeClass = 'text-green-400'; callLabel = '✅ VALUE'; callBadge = 'inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-green-500/15 text-green-400'; }
                  else if (edgePct >= -5) { edgeClass = 'text-muted'; callLabel = '⚪ PASS'; callBadge = 'inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-accent-gray/15 text-muted'; }
                  else                   { edgeClass = 'text-accent-red'; callLabel = '❌ AVOID'; callBadge = 'inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-accent-red/15 text-accent-red'; }
                  return (
                    <tr key={i}>
                      <td className="text-left text-xs text-white/80">{row.market}</td>
                      <td className="text-right num-mono text-white/70">{(row.imp * 100).toFixed(1)}%</td>
                      <td className="text-right num-mono text-accent-cyan">{(row.dv * 100).toFixed(1)}%</td>
                      <td className={`text-right num-mono ${edgeClass}`}>
                        {edgePct > 0 ? '+' : ''}{edgePct.toFixed(1)}%
                      </td>
                      <td className="text-center">
                        <span className={callBadge}>{callLabel}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <div className="mt-2 text-[0.55rem] text-muted text-center">
            Polymarket = zero-vig crowd consensus · 12SPORT = real odds you bet at 12play.my
          </div>
        </div>
      </div>

      {/* ---- 2-4. Triangulation Tables ---- */}
      <div className="mb-6">
        <h2 className="section-header">2-4. Triangulation</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <TriangulationTable
            title="1X2 Match Result"
            sources={analysis.triangulation_1x2}
            headers={[home_team, 'Draw', away_team]}
            decimals={1}
          />
          <TriangulationTable
            title="O/U 2.5 Total Goals"
            sources={analysis.triangulation_ou}
            headers={['Over 2.5', 'Under 2.5']}
            decimals={1}
          />
          <TriangulationTable
            title="BTTS"
            sources={analysis.triangulation_btts}
            headers={['Yes', 'No']}
            decimals={1}
          />
        </div>
      </div>

      {/* ---- 5. Narrative ---- */}
      <div className="mb-6">
        <h2 className="section-header">5. Narrative &amp; Key Factors</h2>
        <div className="card space-y-3">
          {analysis.narrative?.form && (
            <div className="flex gap-3">
              <TrendingUp className="w-4 h-4 text-accent-cyan shrink-0 mt-0.5" />
              <div>
                <div className="text-[0.6rem] text-muted uppercase tracking-wider mb-0.5">
                  Form
                </div>
                <div className="text-xs text-white/80">
                  {analysis.narrative.form}
                </div>
              </div>
            </div>
          )}
          {analysis.narrative?.injuries && (
            <div className="flex gap-3">
              <AlertTriangle className="w-4 h-4 text-accent-yellow shrink-0 mt-0.5" />
              <div>
                <div className="text-[0.6rem] text-muted uppercase tracking-wider mb-0.5">
                  Injuries
                </div>
                <div className="text-xs text-white/80">
                  {analysis.narrative.injuries}
                </div>
              </div>
            </div>
          )}
          {analysis.narrative?.tactical && (
            <div className="flex gap-3">
              <Info className="w-4 h-4 text-accent-green shrink-0 mt-0.5" />
              <div>
                <div className="text-[0.6rem] text-muted uppercase tracking-wider mb-0.5">
                  Tactical
                </div>
                <div className="text-xs text-white/80">
                  {analysis.narrative.tactical}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ---- 6. Edge Summary & Staking ---- */}
      <div className="mb-6">
        <h2 className="section-header">
          6. Edge Summary &amp; Staking
        </h2>
        <div className="card overflow-x-auto">
          <table className="terminal-grid w-full min-w-[500px]">
            <thead>
              <tr>
                <th className="text-left">Market</th>
                <th className="text-right num-mono">Edge %</th>
                <th className="text-center">Status</th>
                <th className="text-right num-mono">Q-Kelly Stake</th>
                <th className="text-right num-mono">Amount (RM)</th>
              </tr>
            </thead>
            <tbody>
              {analysis.edge_summary.map((e, i) => {
                const stakeAmount =
                  bankroll *
                  (maxBankrollPct / 100) *
                  (e.quarter_kelly_stake / 100);
                const stakePct = e.quarter_kelly_stake;
                const sl = edgeStatusLabel(e.edge);
                return (
                  <tr key={i}>
                    <td className="text-left text-xs text-white/80">
                      {e.market}
                    </td>
                    {/* Edge % — coloured by classification */}
                    <td
                      className={`text-right num-mono ${edgeClass(e.edge)}`}
                    >
                      {e.edge > 0 ? '+' : ''}
                      {e.edge.toFixed(1)}%
                    </td>
                    {/* Status badge — computed from edge */}
                    <td className="text-center">
                      {e.edge > 20 && (
                        <span className="edge-positive-pulse inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-accent-green/20 text-accent-green">
                          KELLY
                        </span>
                      )}
                      {e.edge >= 5 && e.edge <= 20 && (
                        <span className="inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-green-500/15 text-green-400">
                          VALUE
                        </span>
                      )}
                      {e.edge >= -5 && e.edge < 5 && (
                        <span className="inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-accent-gray/15 text-muted">
                          PASS
                        </span>
                      )}
                      {e.edge < -5 && (
                        <span className="inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-accent-red/15 text-accent-red">
                          AVOID
                        </span>
                      )}
                    </td>
                    <td className="text-right num-mono text-white/80">
                      {stakePct > 0
                        ? `${stakePct.toFixed(2)}%`
                        : '-'}
                    </td>
                    <td
                      className={`text-right num-mono font-bold ${stakeAmount > 0 ? 'text-accent-green' : 'text-muted'}`}
                    >
                      {stakeAmount > 0
                        ? `RM${stakeAmount.toFixed(2)}`
                        : '-'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-[0.55rem] text-muted">
            <span>
              Max stake per bet: {maxBankrollPct}% of RM{bankroll} = RM
              {(bankroll * (maxBankrollPct / 100)).toFixed(2)}
            </span>
            <div className="flex items-center gap-2">
              <span>Max %</span>
              <input
                type="range"
                min={5}
                max={25}
                value={maxBankrollPct}
                onChange={(e) =>
                  setMaxBankrollPct(parseInt(e.target.value))
                }
                className="w-20 h-1 bg-dark-600 rounded-full appearance-none cursor-pointer accent-accent-cyan"
              />
              <span className="text-white num-mono w-6 text-center">
                {maxBankrollPct}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ---- Footer ---- */}
      <div className="text-[0.55rem] text-muted text-center">
        Match ID: {match.id} &middot; Cron data &middot; 6-Layer Ensemble
        &middot; {fmtLocal(data.system_status.last_updated)}
      </div>
    </div>
  );
}
