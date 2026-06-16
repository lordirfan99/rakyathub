/**
 * harga-minyak.mjs — Live Malaysian fuel prices (RON95, RON97, Diesel)
 *
 * Source: data.gov.my "fuelprice" dataset (KPDN weekly retail fuel prices, CC BY 4.0).
 * Traffic-driven caching (no cron). Returns latest weekly prices + week-on-week change.
 * URL: /.netlify/functions/harga-minyak
 *
 * CSV columns: date, series_type, ron95, ron97, diesel, diesel_eastmsia
 *   series_type = "level"  -> actual RM/litre for that week
 *   series_type = "change" -> week-on-week delta
 */

const CSV_URL = 'https://storage.data.gov.my/commodities/fuelprice.csv';
const STALE_AFTER_MS = 6 * 60 * 60 * 1000; // refetch after 6h
const CACHE_TTL_MS = 60 * 60 * 1000; // browser/CDN cache: 1h

let cache = { data: null, fetchedAt: null };

function parseCSV(text) {
  const lines = text.trim().split('\n');
  const header = lines[0].replace(/\r/g, '').split(',');
  const idx = (k) => header.indexOf(k);
  const di = idx('date'), si = idx('series_type');
  const r95 = idx('ron95'), r97 = idx('ron97'), dsl = idx('diesel'), dslE = idx('diesel_eastmsia');
  if (di === -1 || si === -1 || r95 === -1) throw new Error('Unexpected fuelprice CSV columns');

  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const c = lines[i].replace(/\r/g, '').split(',');
    if (!c[di]) continue;
    rows.push({
      date: c[di],
      series_type: c[si],
      ron95: parseFloat(c[r95]),
      ron97: parseFloat(c[r97]),
      diesel: parseFloat(c[dsl]),
      diesel_eastmsia: dslE !== -1 ? parseFloat(c[dslE]) : null,
    });
  }
  return rows;
}

async function fetchFuel() {
  const resp = await fetch(CSV_URL, {
    headers: { 'User-Agent': 'RakyatHub/1.0' },
    signal: AbortSignal.timeout(25000),
  });
  if (!resp.ok) throw new Error(`fuelprice CSV: HTTP ${resp.status}`);
  const rows = parseCSV(await resp.text());

  const levels = rows.filter((r) => r.series_type === 'level' && !isNaN(r.ron95)).sort((a, b) => a.date.localeCompare(b.date));
  if (!levels.length) throw new Error('No level rows in fuelprice data');

  const latest = levels[levels.length - 1];
  const prev = levels.length >= 2 ? levels[levels.length - 2] : null;
  const changeRow = rows.find((r) => r.series_type === 'change' && r.date === latest.date);

  const delta = (cur, was) => (was != null && !isNaN(was) ? +(cur - was).toFixed(2) : 0);

  // Weekly history for the chart — last 3 years of "level" rows (date + 3 series).
  const history = levels
    .slice(-156)
    .map((r) => ({
      date: r.date,
      ron95: !isNaN(r.ron95) ? +r.ron95.toFixed(2) : null,
      ron97: !isNaN(r.ron97) ? +r.ron97.toFixed(2) : null,
      diesel: !isNaN(r.diesel) ? +r.diesel.toFixed(2) : null,
    }));

  const result = {
    date: latest.date,
    last_updated: new Date().toISOString(),
    source: 'data.gov.my — KPDN (fuelprice)',
    history,
    prices: {
      ron95: +latest.ron95.toFixed(2),
      ron97: +latest.ron97.toFixed(2),
      diesel: +latest.diesel.toFixed(2),
      diesel_eastmsia: latest.diesel_eastmsia != null && !isNaN(latest.diesel_eastmsia) ? +latest.diesel_eastmsia.toFixed(2) : null,
    },
    change: {
      ron95: changeRow && !isNaN(changeRow.ron95) ? +changeRow.ron95.toFixed(2) : delta(latest.ron95, prev?.ron95),
      ron97: changeRow && !isNaN(changeRow.ron97) ? +changeRow.ron97.toFixed(2) : delta(latest.ron97, prev?.ron97),
      diesel: changeRow && !isNaN(changeRow.diesel) ? +changeRow.diesel.toFixed(2) : delta(latest.diesel, prev?.diesel),
    },
  };

  cache = { data: result, fetchedAt: Date.now() };
  return result;
}

export const handler = async () => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': `public, max-age=${CACHE_TTL_MS / 1000}, s-maxage=${CACHE_TTL_MS / 1000}`,
  };
  try {
    const stale = !cache.data || !cache.fetchedAt || Date.now() - cache.fetchedAt > STALE_AFTER_MS;
    const data = stale ? await fetchFuel() : cache.data;
    return { statusCode: 200, headers, body: JSON.stringify(data) };
  } catch (err) {
    console.error('[harga-minyak]', err.message);
    if (cache.data) {
      return { statusCode: 200, headers: { ...headers, 'X-Cache-Status': 'stale' }, body: JSON.stringify({ ...cache.data, _error: err.message }) };
    }
    return { statusCode: 500, headers, body: JSON.stringify({ error: 'Gagal memuatkan harga minyak' }) };
  }
};
