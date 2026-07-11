import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, AlertTriangle, TrendingUp, Info } from 'lucide-react';
import EdgeBadge from './EdgeBadge';
import TriangulationTable from './TriangulationTable';
import Countdown from './Countdown';

function edgeClass(edge) {
  if (edge > 20) return 'text-accent-green font-bold';
  if (edge >= 5) return 'text-green-400';
  if (edge >= -5) return 'text-muted';
  return 'text-accent-red';
}
function fmtLocal(isoString) {
  return new Date(isoString).toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', hour12: true });
}

export default function MatchDetail() {
  const { matchId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [maxBankrollPct, setMaxBankrollPct] = useState(10);

  useEffect(() => {
    fetch('/data.json').then((r) => r.json()).then((d) => setData(d)).catch(() => {});
  }, []);

  if (!data) return <div className="flex items-center justify-center h-screen bg-dark-900"><div className="text-accent-cyan text-sm animate-pulse">LOADING...</div></div>;
  const match = data.matches.find((m) => m.id === matchId);
  if (!match) return <div className="flex items-center justify-center h-screen bg-dark-900"><div className="text-accent-red text-sm">MATCH NOT FOUND</div></div>;

  const { analysis, home_team, away_team, date, venue, stage } = match;
  const bankroll = data.system_status.bankroll_rm;
  const bestEdge = analysis.edge_summary?.length ? [...analysis.edge_summary].sort((a, b) => b.edge - a.edge)[0] : null;

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-4 py-6">
      <div className="mb-6">
        <button onClick={() => navigate('/')} className="flex items-center gap-1.5 text-muted hover:text-white text-xs mb-4 transition-colors"><ArrowLeft className="w-3.5 h-3.5" /> BACK TO DASHBOARD</button>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="min-w-0">
            <h1 className="text-xl font-bold text-white tracking-tight">{home_team} <span className="text-muted mx-2">vs</span> {away_team}</h1>
            <div className="flex flex-wrap gap-x-3 gap-y-1 text-[0.6rem] text-muted mt-1">
              <span>{date}</span>
              <span className="text-accent-yellow/80 font-bold"><Countdown targetIso={`${match.date} ${match.time}`} /></span>
              {venue && (<><span className="hidden sm:inline">·</span><span className="truncate max-w-[200px]">{venue}</span></>)}
              <span>·</span><span className="text-accent-yellow">{stage}</span>
            </div>
          </div>
          <EdgeBadge edge={bestEdge?.edge ?? null} />
        </div>
      </div>

      {/* 1. Bookies Comparison */}
      <div className="mb-6">
        <h2 className="section-header">1. Odds Comparison - 1xBet Malaysia vs 12Play MY</h2>
        <div className="card mb-3">
          <div className="text-[0.6rem] text-muted mb-3 uppercase tracking-wider">⚡ Match Result (1X2)</div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-dark-800/50 rounded-lg p-3 border border-dark-600">
              <div className="text-[0.55rem] text-accent-cyan uppercase tracking-wider mb-2 font-bold text-center">1xBet Malaysia</div>
              <div className="flex justify-between items-center border-b border-dark-700 pb-1.5 mb-1.5">
                <span className="text-xs text-white/80">{home_team}</span>
                <span className="text-sm font-bold text-white num-mono">{match.bookies?.['1xbet']?.['1x2']?.home?.toFixed(2) ?? match.home_odds?.toFixed(2) ?? '-'}</span>
              </div>
              <div className="flex justify-between items-center border-b border-dark-700 pb-1.5 mb-1.5">
                <span className="text-xs text-muted">Draw</span>
                <span className="text-sm font-bold text-accent-yellow num-mono">{match.bookies?.['1xbet']?.['1x2']?.draw?.toFixed(2) ?? match.draw_odds?.toFixed(2) ?? '-'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-white/80">{away_team}</span>
                <span className="text-sm font-bold text-white num-mono">{match.bookies?.['1xbet']?.['1x2']?.away?.toFixed(2) ?? match.away_odds?.toFixed(2) ?? '-'}</span>
              </div>
            </div>
            <div className="bg-dark-800/50 rounded-lg p-3 border border-accent-green/30">
              <div className="text-[0.55rem] text-accent-green uppercase tracking-wider mb-2 font-bold text-center">12Play MY</div>
              <div className="flex justify-between items-center border-b border-dark-700 pb-1.5 mb-1.5">
                <span className="text-xs text-white/80">{home_team}</span>
                <span className="text-sm font-bold text-white num-mono">{match.bookies?.['12play']?.['1x2']?.home?.toFixed(2) ?? '-'}</span>
              </div>
              <div className="flex justify-between items-center border-b border-dark-700 pb-1.5 mb-1.5">
                <span className="text-xs text-muted">Draw</span>
                <span className="text-sm font-bold text-accent-yellow num-mono">{match.bookies?.['12play']?.['1x2']?.draw?.toFixed(2) ?? '-'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-white/80">{away_team}</span>
                <span className="text-sm font-bold text-white num-mono">{match.bookies?.['12play']?.['1x2']?.away?.toFixed(2) ?? '-'}</span>
              </div>
            </div>
          </div>
        </div>

        {match.bookies?.['1xbet']?.['over_under_25'] && match.bookies?.['12play']?.['over_under_25'] && (
        <div className="card mb-3">
          <div className="text-[0.6rem] text-muted mb-3 uppercase tracking-wider">⚽ Total Goals O/U 2.5</div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-dark-800/50 rounded-lg p-3 border border-dark-600">
              <div className="text-[0.55rem] text-accent-cyan uppercase tracking-wider mb-2 font-bold text-center">1xBet Malaysia</div>
              <div className="flex justify-between items-center border-b border-dark-700 pb-1.5 mb-1.5">
                <span className="text-xs text-white/80">Over 2.5</span>
                <span className="text-sm font-bold text-accent-cyan num-mono">{match.bookies['1xbet']['over_under_25'].over.toFixed(3)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-white/80">Under 2.5</span>
                <span className="text-sm font-bold text-accent-yellow num-mono">{match.bookies['1xbet']['over_under_25'].under.toFixed(3)}</span>
              </div>
            </div>
            <div className="bg-dark-800/50 rounded-lg p-3 border border-accent-green/30">
              <div className="text-[0.55rem] text-accent-green uppercase tracking-wider mb-2 font-bold text-center">12Play MY</div>
              <div className="flex justify-between items-center border-b border-dark-700 pb-1.5 mb-1.5">
                <span className="text-xs text-white/80">Over 2.5</span>
                <span className="text-sm font-bold text-accent-cyan num-mono">{match.bookies['12play']['over_under_25'].over.toFixed(3)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-white/80">Under 2.5</span>
                <span className="text-sm font-bold text-accent-yellow num-mono">{match.bookies['12play']['over_under_25'].under.toFixed(3)}</span>
              </div>
            </div>
          </div>
        </div>
        )}

        {match.bookies && (
        <div className="card">
          <div className="text-[0.6rem] text-muted mb-3 uppercase tracking-wider">📊 Additional Markets</div>
          <div className="overflow-x-auto">
            <table className="terminal-grid w-full min-w-[400px]">
              <thead><tr><th className="text-left">Market</th><th className="text-right num-mono text-accent-cyan">1xBet</th><th className="text-right num-mono text-accent-green">12Play</th><th className="text-center">Best</th></tr></thead>
              <tbody>
                {[
                  { label: 'BTTS Yes', b1: match.bookies?.['1xbet']?.btts?.yes, b2: match.bookies?.['12play']?.btts?.yes },
                  { label: 'BTTS No', b1: match.bookies?.['1xbet']?.btts?.no, b2: match.bookies?.['12play']?.btts?.no },
                  { label: `${home_team} To Qualify`, b1: match.bookies?.['1xbet']?.['team_to_qualify']?.spain, b2: match.bookies?.['12play']?.['team_to_qualify']?.spain },
                  { label: `${away_team} To Qualify`, b1: match.bookies?.['1xbet']?.['team_to_qualify']?.belgium, b2: match.bookies?.['12play']?.['team_to_qualify']?.belgium },
                  { label: 'AH Spain (-1)', b1: match.bookies?.['1xbet']?.['asian_handicap_1']?.['home_-1'], b2: match.bookies?.['12play']?.['goals_handicap_n1']?.['spain_-1'] },
                  { label: 'AH Belgium (+1)', b1: match.bookies?.['1xbet']?.['asian_handicap_1']?.['away_+1'], b2: match.bookies?.['12play']?.['goals_handicap_n1']?.['belgium_+1'] },
                ].filter(r => r.b1 || r.b2).map((r, i) => {
                  const best = Math.max(r.b1 ?? 0, r.b2 ?? 0);
                  const bestLabel = best === r.b1 && best === r.b2 ? '=' : best === r.b1 ? '1xBet' : best === r.b2 ? '12Play' : '-';
                  return (<tr key={i}>
                    <td className="text-left text-xs text-white/80">{r.label}</td>
                    <td className={`text-right num-mono ${r.b1 === best && r.b2 ? 'text-white font-bold' : 'text-white/60'}`}>{r.b1?.toFixed(3) ?? '-'}</td>
                    <td className={`text-right num-mono ${r.b2 === best && r.b1 ? 'text-white font-bold' : 'text-white/60'}`}>{r.b2?.toFixed(3) ?? '-'}</td>
                    <td className="text-center text-[0.55rem]">
                      <span className={`inline-block px-2 py-0.5 rounded font-bold ${bestLabel === '1xBet' ? 'bg-accent-cyan/20 text-accent-cyan' : bestLabel === '12Play' ? 'bg-accent-green/20 text-accent-green' : 'text-muted'}`}>{bestLabel}</span>
                    </td>
                  </tr>);
                })}
              </tbody>
            </table>
          </div>
        </div>
        )}
      </div>

      {/* 2. Edge Analysis */}
      <div className="mb-6">
        <h2 className="section-header">2. Edge Analysis vs Polymarket (Zero-Vig)</h2>
        <div className="card">
          <div className="overflow-x-auto">
            <table className="terminal-grid w-full min-w-[400px]">
              <thead><tr><th className="text-left">Market</th><th className="text-right num-mono">1xBet Implied</th><th className="text-right num-mono">12Play Implied</th><th className="text-right num-mono">Polymarket DV</th><th className="text-right num-mono">1xBet Edge</th><th className="text-center">Call</th></tr></thead>
              <tbody>
                {[
                  { market: `${home_team} Win`, imp1: 1/match.home_odds, dv: analysis.polymarket_devig.home },
                  { market: 'Draw', imp1: 1/match.draw_odds, dv: analysis.polymarket_devig.draw },
                  { market: `${away_team} Win`, imp1: 1/match.away_odds, dv: analysis.polymarket_devig.away },
                ].map((row, i) => {
                  const edgePct1 = ((row.dv / row.imp1) - 1) * 100;
                  let callLabel, callBadge;
                  const be = edgePct1;
                  if (be > 20) { callLabel = '🚀 KELLY'; callBadge = 'edge-positive-pulse inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-accent-green/20 text-accent-green'; }
                  else if (be >= 5) { callLabel = '✅ VALUE'; callBadge = 'inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-green-500/15 text-green-400'; }
                  else if (be >= -5) { callLabel = '⚪ PASS'; callBadge = 'inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-accent-gray/15 text-muted'; }
                  else { callLabel = '❌ AVOID'; callBadge = 'inline-block px-2 py-0.5 rounded text-[0.5rem] font-bold bg-accent-red/15 text-accent-red'; }
                  return (<tr key={i}>
                    <td className="text-left text-xs text-white/80">{row.market}</td>
                    <td className="text-right num-mono text-white/70">{(row.imp1 * 100).toFixed(1)}%</td>
                    <td className="text-right num-mono text-accent-green">-</td>
                    <td className="text-right num-mono text-accent-cyan">{(row.dv * 100).toFixed(1)}%</td>
                    <td className={`text-right num-mono ${be > 0 ? 'text-accent-green' : be < -5 ? 'text-accent-red' : 'text-muted'}`}>{be > 0 ? '+' : ''}{be.toFixed(1)}%</td>
                    <td className="text-center"><span className={callBadge}>{callLabel}</span></td>
                  </tr>);
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* 3-5. Triangulation */}
      <div className="mb-6">
        <h2 className="section-header">3-5. Triangulation</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <TriangulationTable title="1X2 Match Result" sources={analysis.triangulation_1x2} headers={[home_team, 'Draw', away_team]} decimals={1} />
          <TriangulationTable title="O/U 2.5 Total Goals" sources={analysis.triangulation_ou} headers={['Over 2.5', 'Under 2.5']} decimals={1} />
          <TriangulationTable title="BTTS" sources={analysis.triangulation_btts} headers={['Yes', 'No']} decimals={1} />
        </div>
      </div>

      {/* 6. Narrative */}
      <div className="mb-6">
        <h2 className="section-header">6. Narrative & Key Factors</h2>
        <div className="card space-y-3">
          {analysis.narrative?.form && <div className="flex gap-3"><TrendingUp className="w-4 h-4 text-accent-cyan shrink-0 mt-0.5" /><div><div className="text-[0.6rem] text-muted uppercase tracking-wider mb-0.5">Form</div><div className="text-xs text-white/80">{analysis.narrative.form}</div></div></div>}
          {analysis.narrative?.injuries && <div className="flex gap-3"><AlertTriangle className="w-4 h-4 text-accent-yellow shrink-0 mt-0.5" /><div><div className="text-[0.6rem] text-muted uppercase tracking-wider mb-0.5">Injuries</div><div className="text-xs text-white/80">{analysis.narrative.injuries}</div></div></div>}
          {analysis.narrative?.tactical && <div className="flex gap-3"><Info className="w-4 h-4 text-accent-green shrink-0 mt-0.5" /><div><div className="text-[0.6rem] text-muted uppercase tracking-wider mb-0.5">Tactical</div><div className="text-xs text-white/80">{analysis.narrative.tactical}</div></div></div>}
        </div>
      </div>

      {/* 7. Edge Summary */}
      <div className="mb-6">
        <h2 className="section-header">7. Edge Summary & Staking</h2>
        <div className="card overflow-x-auto">
          <table className="terminal-grid w-full min-w-[500px]">
            <thead><tr><th className="text-left">Market</th><th className="text-right num-mono">Edge %</th><th className="text-center">Status</th><th className="text-right num-mono">Q-Kelly Stake</th><th className="text-right num-mono">Amount (RM)</th></tr></thead>
            <tbody>
              {analysis.edge_summary.map((e, i) => {
                const stakeAmount = bankroll * (maxBankrollPct / 100) * (e.quarter_kelly_stake / 100);
                return (<tr key={i}>
                  <td className="text-left text-xs text-white/80">{e.market}</td>
                  <td className={`text-right num-mono ${edgeClass(e.edge)}`}>{e.edge > 0 ? '+' : ''}{e.edge.toFixed(1)}%</td>
                  <td className="text-center">
                    {e.edge > 20 && <span className="edge-positive-pulse inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-accent-green/20 text-accent-green">KELLY</span>}
                    {e.edge >= 5 && e.edge <= 20 && <span className="inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-green-500/15 text-green-400">VALUE</span>}
                    {e.edge >= -5 && e.edge < 5 && <span className="inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-accent-gray/15 text-muted">PASS</span>}
                    {e.edge < -5 && <span className="inline-block px-2 py-0.5 rounded text-[0.55rem] font-bold bg-accent-red/15 text-accent-red">AVOID</span>}
                  </td>
                  <td className="text-right num-mono text-white/80">{e.quarter_kelly_stake > 0 ? `${e.quarter_kelly_stake.toFixed(2)}%` : '-'}</td>
                  <td className={`text-right num-mono font-bold ${stakeAmount > 0 ? 'text-accent-green' : 'text-muted'}`}>{stakeAmount > 0 ? `RM${stakeAmount.toFixed(2)}` : '-'}</td>
                </tr>);
              })}
            </tbody>
          </table>
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-[0.55rem] text-muted">
            <span>Max stake per bet: {maxBankrollPct}% of RM{bankroll} = RM{(bankroll * (maxBankrollPct / 100)).toFixed(2)}</span>
            <div className="flex items-center gap-2">
              <span>Max %</span>
              <input type="range" min={5} max={25} value={maxBankrollPct} onChange={(e) => setMaxBankrollPct(parseInt(e.target.value))} className="w-20 h-1 bg-dark-600 rounded-full appearance-none cursor-pointer accent-accent-cyan" />
              <span className="text-white num-mono w-6 text-center">{maxBankrollPct}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="text-[0.55rem] text-muted text-center">Match ID: {match.id} · Cron data · 6-Layer Ensemble · {fmtLocal(data.system_status.last_updated)}</div>
    </div>
  );
}
