import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Activity,
  DollarSign,
  Clock,
  TrendingUp,
  BarChart3,
} from 'lucide-react';
import EdgeBadge from './EdgeBadge';
import Countdown from './Countdown';

function fmtLocal(isoString) {
  const d = new Date(isoString);
  return d.toLocaleTimeString('en-MY', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}
function fmtLocalDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleDateString('en-MY', {
    day: 'numeric',
    month: 'short',
  });
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [now, setNow] = useState(new Date());
  const navigate = useNavigate();

  useEffect(() => {
    fetch('/data.json')
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
    const tick = setInterval(() => setNow(new Date()), 60_000);
    return () => clearInterval(tick);
  }, []);

  if (loading) return <div className="flex items-center justify-center h-screen bg-dark-900"><div className="text-accent-cyan text-sm animate-pulse">LOADING SYSTEM...</div></div>;
  if (!data) return <div className="flex items-center justify-center h-screen bg-dark-900"><div className="text-accent-red text-sm">DATA UNAVAILABLE</div></div>;

  const { system_status, matches: allMatches } = data;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const matches = allMatches.filter((m) => new Date(m.date + 'T23:59:59') >= today);
  const bankroll = system_status.bankroll_rm;
  const lastUpdated = system_status.last_updated;
  const nextRun = new Date(new Date(lastUpdated).getTime() + 4 * 60 * 60 * 1000);
  const isStale = now.getTime() - new Date(lastUpdated).getTime() > 4.5 * 60 * 60 * 1000;

  function bestEdge(match) {
    if (!match.analysis?.edge_summary?.length) return null;
    return [...match.analysis.edge_summary].sort((a, b) => b.edge - a.edge)[0];
  }

  return (
    <div className="max-w-7xl mx-auto px-3 sm:px-4 py-6">
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-1">
          <BarChart3 className="w-5 h-5 text-accent-cyan shrink-0" />
          <h1 className="text-lg font-bold tracking-wider text-white">BETTING ENGINE v2.0</h1>
        </div>
        <div className="text-[0.6rem] text-muted tracking-[0.2em] uppercase">6-Layer Ensemble · World Cup 2026 · Cron every 4h</div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 sm:gap-3 mb-8">
        <div className="card flex flex-row items-center justify-between gap-1 sm:gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <Activity className="w-4 h-4 text-accent-green shrink-0" />
            <div className="min-w-0">
              <div className="text-[0.55rem] text-muted uppercase tracking-wider truncate">Last Cron</div>
              <div className="text-xs sm:text-sm font-bold text-white tracking-tight">{fmtLocal(lastUpdated)}</div>
            </div>
          </div>
          <span className="text-[0.5rem] text-muted shrink-0 hidden xs:inline">{fmtLocalDate(lastUpdated)}</span>
        </div>
        <div className="card flex flex-row items-center justify-between gap-1 sm:gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <Clock className="w-4 h-4 text-accent-yellow shrink-0" />
            <div className="min-w-0">
              <div className="text-[0.55rem] text-muted uppercase tracking-wider truncate">Next Run</div>
              <div className="text-xs sm:text-sm font-bold text-white tracking-tight">{fmtLocal(nextRun.toISOString())}</div>
            </div>
          </div>
          {isStale && <span className="text-[0.5rem] text-accent-red font-bold shrink-0 animate-pulse">STALE</span>}
        </div>
        <div className="card flex flex-row items-center justify-between gap-1 sm:gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <DollarSign className="w-4 h-4 text-accent-green shrink-0" />
            <div className="min-w-0">
              <div className="text-[0.55rem] text-muted uppercase tracking-wider truncate">Bankroll</div>
              <div className="text-xs sm:text-sm font-bold text-white tracking-tight">RM{bankroll}</div>
            </div>
          </div>
        </div>
        <div className="card flex flex-row items-center justify-between gap-1 sm:gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <TrendingUp className="w-4 h-4 text-accent-cyan shrink-0" />
            <div className="min-w-0">
              <div className="text-[0.55rem] text-muted uppercase tracking-wider truncate">Matches</div>
              <div className="text-xs sm:text-sm font-bold text-white tracking-tight">{matches.length}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <h2 className="section-header mb-0">Upcoming Matches</h2>
        <div className="flex flex-wrap gap-2 sm:gap-3 text-[0.55rem] sm:text-[0.6rem] text-muted">
          <span>🚀 Kelly</span><span>✅ Value</span><span>⚪ Neutral</span><span>❌ Avoid</span>
        </div>
      </div>

      <div className="grid gap-2">
        <div className="hidden md:grid grid-cols-[1fr_1.5fr_0.7fr_0.7fr_1.2fr_1.2fr_0.7fr] gap-2 px-4 py-2 text-[0.6rem] text-muted uppercase tracking-wider">
          <span /><span>Match</span><span>Stage</span><span>⏱ Countdown</span><span>1xBet</span><span>12Play</span><span>Edge</span>
        </div>

        {matches.map((m) => {
          const top = bestEdge(m);
          return (
            <div key={m.id} onClick={() => navigate(`/match/${m.id}`)}
              className="card cursor-pointer hover:border-accent-cyan/30 transition-all grid grid-cols-1 md:grid-cols-[1fr_1.5fr_0.7fr_0.7fr_1.2fr_1.2fr_0.7fr] gap-2 items-center">
              <div className="md:hidden flex items-center justify-between w-full">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="font-bold text-sm text-white truncate">{m.home_team}</span>
                  <span className="text-muted text-xs shrink-0">vs</span>
                  <span className="font-bold text-sm text-white truncate">{m.away_team}</span>
                </div>
                <EdgeBadge edge={top?.edge ?? null} />
              </div>

              <div className="hidden md:block">
                {top && top.edge > 20 && <span className="edge-positive-pulse inline-block w-2 h-2 rounded-full bg-accent-green" />}
                {top && top.edge >= 5 && top.edge <= 20 && <span className="inline-block w-2 h-2 rounded-full bg-green-500" />}
                {top && top.edge >= -5 && top.edge < 5 && <span className="inline-block w-2 h-2 rounded-full bg-accent-gray" />}
                {top && top.edge < -5 && <span className="inline-block w-2 h-2 rounded-full bg-accent-red" />}
                {!top && <span className="inline-block w-2 h-2 rounded-full bg-accent-gray" />}
              </div>

              <div className="hidden md:flex items-center gap-2">
                <span className="font-bold text-white">{m.home_team}</span>
                <span className="text-muted text-xs">v</span>
                <span className="font-bold text-white">{m.away_team}</span>
              </div>

              <div className="hidden md:text-sm text-muted md:block">{m.stage}</div>
              <div className="hidden md:block"><Countdown targetIso={`${m.date} ${m.time}`} /></div>

              <div className="hidden md:flex gap-2 text-xs num-mono">
                <span className="text-accent-cyan/80 font-bold">{m.bookies?.['1xbet']?.['1x2']?.home?.toFixed(2) ?? m.home_odds?.toFixed(2) ?? '-'}</span>
                <span className="text-muted">|</span>
                <span className="text-accent-yellow/80 font-bold">{m.bookies?.['1xbet']?.['1x2']?.draw?.toFixed(2) ?? m.draw_odds?.toFixed(2) ?? '-'}</span>
                <span className="text-muted">|</span>
                <span className="text-accent-cyan/80 font-bold">{m.bookies?.['1xbet']?.['1x2']?.away?.toFixed(2) ?? m.away_odds?.toFixed(2) ?? '-'}</span>
              </div>

              <div className="hidden md:flex gap-2 text-xs num-mono">
                <span className="text-accent-green/80 font-bold">{m.bookies?.['12play']?.['1x2']?.home?.toFixed(2) ?? '-'}</span>
                <span className="text-muted">|</span>
                <span className="text-accent-yellow/80 font-bold">{m.bookies?.['12play']?.['1x2']?.draw?.toFixed(2) ?? '-'}</span>
                <span className="text-muted">|</span>
                <span className="text-accent-green/80 font-bold">{m.bookies?.['12play']?.['1x2']?.away?.toFixed(2) ?? '-'}</span>
              </div>

              <div className="hidden md:block"><EdgeBadge edge={top?.edge ?? null} /></div>

              <div className="md:hidden flex items-center justify-between gap-1 text-[0.55rem] text-muted mt-1">
                <span className="truncate">{m.stage} · {m.date}</span>
                <Countdown targetIso={`${m.date} ${m.time}`} />
                <span className="shrink-0 num-mono text-[0.5rem]">
                  1xBet: <span className="text-white/70">{m.bookies?.['1xbet']?.['1x2']?.home?.toFixed(2) ?? m.home_odds?.toFixed(2) ?? '-'}</span>
                  <span className="text-muted mx-0.5">·</span>
                  <span className="text-accent-green/80">12P: {m.bookies?.['12play']?.['1x2']?.home?.toFixed(2) ?? '-'}</span>
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-8 text-[0.5rem] sm:text-[0.55rem] text-muted text-center">
        Data refreshes every 4 hours &middot; Last sync: {fmtLocal(lastUpdated)} <span className="opacity-50">({fmtLocalDate(lastUpdated)})</span>
      </div>
    </div>
  );
}
