import { useState, useEffect } from 'react';

/**
 * Live countdown timer.
 * targetIso — ISO date string or "YYYY-MM-DD HH:MM" in MYT
 * Returns a compact string like "10h 23m" or "LIVE" or "FINAL"
 */
function calcRemaining(targetDate) {
  const now = Date.now();
  const diff = targetDate.getTime() - now;
  if (diff <= 0) return { text: 'LIVE', expired: true };

  const totalMinutes = Math.floor(diff / 60_000);
  const days = Math.floor(totalMinutes / 1440);
  const hours = Math.floor((totalMinutes % 1440) / 60);
  const mins = totalMinutes % 60;

  if (days > 0) return { text: `${days}d ${hours}h`, expired: false };
  if (hours > 0) return { text: `${hours}h ${mins}m`, expired: false };
  return { text: `${mins}m`, expired: false };
}

export default function Countdown({ targetIso, label = 'Kickoff' }) {
  // Parse target: "2026-07-11 03:00 MYT" → MYT is UTC+8
  let clean = targetIso;
  if (typeof clean === 'string') {
    clean = clean.replace(/\s*MYT\s*$/i, '+08:00').trim();
  }
  const targetDate = new Date(clean);

  const [remaining, setRemaining] = useState(() => calcRemaining(targetDate));

  useEffect(() => {
    const tick = setInterval(() => {
      setRemaining(calcRemaining(targetDate));
    }, 60_000); // tick every minute
    return () => clearInterval(tick);
  }, [targetDate]);

  if (remaining.expired) {
    return (
      <span className="inline-flex items-center gap-1 text-[0.55rem] font-bold text-accent-green">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-green opacity-75" />
          <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-green" />
        </span>
        LIVE
      </span>
    );
  }

  return (
    <span className="num-mono text-[0.55rem] text-accent-yellow/90" title={`${label}: ${targetIso}`}>
      {remaining.text}
    </span>
  );
}
