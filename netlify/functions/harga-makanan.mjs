/**
 * harga-makanan.mjs — Auto-refresh grocery price API
 *
 * FIXED v2: Dynamic item code lookup by name instead of hardcoded codes.
 * No cron needed: traffic-driven caching.
 * Source: KPDN PriceCatcher + DOSM (CC BY 4.0)
 */

// ── Constants ──
const STALE_AFTER_MS = 12 * 60 * 60 * 1000;  // 12 hours
const CACHE_TTL_MS = 30 * 60 * 1000;          // Browser cache: 30 min

// ── In-memory cache ──
let cache = {
  data: null,
  fetchedAt: null,
};

// ── Item definitions: search by keyword, filter by unit ──
const ITEM_DEFS = [
  { name: "Ayam Standard",        keyword: "AYAM BERSIH - STANDARD",     unit: "1kg",   exclude: [] },
  { name: "Ayam Super",           keyword: "AYAM BERSIH - SUPER",        unit: "1kg",   exclude: [] },
  { name: "Daging Lembu Tempatan",keyword: "DAGING LEMBU TEMPATAN",      unit: "1kg",   exclude: [] },
  { name: "Daging Lembu Import",  keyword: "DAGING LEMBU IMPORT",        unit: "1kg",   exclude: [] },
  { name: "Daging Kambing Import",keyword: "DAGING KAMBING BEBIRI IMPORT BERTULANG", unit: "1kg", exclude: [] },
  { name: "Ikan Kembung",         keyword: "IKAN KEMBUNG",               unit: "1kg",   exclude: ["GORENG", "KICAP", "TIGA RASA", "KECIL/PELALING"] },
  { name: "Ikan Keli",            keyword: "IKAN KELI",                  unit: "1kg",   exclude: [] },
  { name: "Ikan Tilapia",         keyword: "IKAN TILAPIA",               unit: "1kg",   exclude: ["GORENG"] },
  { name: "Ikan Haruan",          keyword: "IKAN HARUAN",                unit: "1kg",   exclude: [] },
  { name: "Telur Gred A",         keyword: "TELUR AYAM GRED A",          unit: "",      exclude: [] },
  { name: "Telur Gred B",         keyword: "TELUR AYAM GRED B",          unit: "",      exclude: [] },
  { name: "Telur Gred C",         keyword: "TELUR AYAM GRED C",          unit: "",      exclude: [] },
  { name: "Beras Super (10kg)",   keyword: "BERAS SUPER",                unit: "10 kg", exclude: ["SABAH", "SARAWAK", "TEPUNG"] },
  { name: "Minyak Masak (1kg)",   keyword: "MINYAK MASAK",               unit: "1kg",   exclude: [] },
  { name: "Minyak Masak (5kg)",   keyword: "MINYAK MASAK",               unit: "5 kg",  exclude: [] },
  { name: "Gula Pasir (1kg)",     keyword: "GULA PUTIH",                 unit: "1kg",   exclude: [] },
  { name: "Tepung Gandum (1kg)",  keyword: "TEPUNG GANDUM",              unit: "1kg",   exclude: ["BERAS"] },
  { name: "Santan Kelapa Segar",  keyword: "SANTAN KELAPA SEGAR",        unit: "",      exclude: [] },
  { name: "Bawang Merah",         keyword: "BAWANG KECIL MERAH ROSE IMPORT (INDIA)", unit: "1kg", exclude: [] },
  { name: "Bawang Putih",         keyword: "BAWANG PUTIH IMPORT (CHINA)", unit: "1kg",  exclude: [] },
  { name: "Cili Hijau",           keyword: "CILI HIJAU",                 unit: "1kg",   exclude: [] },
  { name: "Cili Merah",           keyword: "CILI MERAH - KULAI",         unit: "1kg",   exclude: [] },
  { name: "Halia",                keyword: "HALIA BASAH (TUA)",          unit: "1kg",   exclude: [] },
  { name: "Kacang Bendi",         keyword: "KACANG BENDI",               unit: "1kg",   exclude: [] },
  { name: "Kacang Panjang",       keyword: "KACANG PANJANG",             unit: "1kg",   exclude: [] },
  { name: "Kubis Import",         keyword: "KUBIS BULAT IMPORT",         unit: "1kg",   exclude: [] },
  { name: "Kubis Tempatan",       keyword: "KUBIS BULAT (TEMPATAN)",     unit: "1kg",   exclude: [] },
  { name: "Lobak Merah",          keyword: "LOBAK MERAH",                unit: "1kg",   exclude: [] },
  { name: "Timun",                keyword: "TIMUN",                      unit: "1kg",   exclude: [] },
];

// ── Find item codes from lookup CSV ──
async function fetchItemCodes() {
  const url = 'https://storage.data.gov.my/pricecatcher/lookup_item.csv';
  const resp = await fetch(url, { headers: { 'User-Agent': 'RakyatHub/1.0' }, signal: AbortSignal.timeout(30000) });
  const text = await resp.text();
  const lines = text.split('\n');
  const header = lines[0].replace('\r', '').split(',');
  const codeIdx = header.indexOf('item_code');
  const itemIdx = header.indexOf('item');
  const unitIdx = header.indexOf('unit');
  if (codeIdx === -1 || itemIdx === -1) throw new Error('Unexpected lookup CSV columns');

  const itemMap = {}; // name -> [codes]
  const codeUnit = {}; // code -> unit
  const codeFull = {}; // code -> full_name

  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].replace('\r', '').split(',');
    if (!cols[codeIdx] || !cols[itemIdx]) continue;
    const code = parseInt(cols[codeIdx]);
    const name = cols[itemIdx].toUpperCase().trim();
    const unit = (cols[unitIdx] || '').trim();

    codeUnit[code] = unit;
    codeFull[code] = cols[itemIdx].trim();

    for (const def of ITEM_DEFS) {
      if (!name.includes(def.keyword)) continue;
      if (def.unit && unit.toUpperCase() !== def.unit.toUpperCase()) continue;
      if (def.exclude.some(excl => name.includes(excl))) continue;
      if (!itemMap[def.name]) itemMap[def.name] = [];
      if (!itemMap[def.name].includes(code)) itemMap[def.name].push(code);
    }
  }

  return { itemMap, codeUnit, codeFull };
}

// ── Parse CSV line (handles quoted fields properly) ──
function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      inQuotes = !inQuotes;
    } else if (ch === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  result.push(current);
  return result;
}

// ── Fetch + Aggregate ──
async function fetchAndAggregate() {
  const now = new Date();
  const monthStr = now.toISOString().slice(0, 7);
  const csvUrl = `https://storage.data.gov.my/pricecatcher/pricecatcher_${monthStr}.csv`;

  console.log(`[harga-makanan] Fetching item codes...`);
  const { itemMap, codeUnit, codeFull } = await fetchItemCodes();

  const allCodes = new Set();
  Object.values(itemMap).forEach(codes => codes.forEach(c => allCodes.add(c)));
  console.log(`[harga-makanan] Tracking ${Object.keys(itemMap).length} categories across ${allCodes.size} codes`);

  // Try current month, fallback to prev
  let csvText = null;
  let usedMonth = monthStr;
  for (const m of [monthStr, new Date(now.getFullYear(), now.getMonth() - 1, 1).toISOString().slice(0, 7)]) {
    const url = `https://storage.data.gov.my/pricecatcher/pricecatcher_${m}.csv`;
    console.log(`[harga-makanan] Downloading ${m} CSV...`);
    try {
      const resp = await fetch(url, {
        headers: { 'User-Agent': 'RakyatHub/1.0' },
        signal: AbortSignal.timeout(60000)
      });
      if (resp.ok) {
        csvText = await resp.text();
        usedMonth = m;
        break;
      }
    } catch (e) {
      console.log(`[harga-makanan] Failed ${m}: ${e.message}`);
    }
  }

  if (!csvText) throw new Error('Could not fetch price data for current or previous month');

  console.log(`[harga-makanan] Processing ${(csvText.length / 1024 / 1024).toFixed(1)}MB CSV...`);
  const lines = csvText.split('\n');
  const header = parseCSVLine(lines[0]);
  const dateIdx = header.indexOf('date');
  const itemIdx = header.indexOf('item_code');
  const priceIdx = header.indexOf('price');
  if (dateIdx === -1 || itemIdx === -1 || priceIdx === -1) {
    throw new Error(`Unexpected CSV columns: ${header}`);
  }

  // Aggregate: { itemName: { date: [prices] } }
  const catData = {};
  let totalRows = 0;

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].replace('\r', '');
    if (!line.trim()) continue;

    const cols = parseCSVLine(line);
    const code = parseInt(cols[itemIdx]);
    const price = parseFloat(cols[priceIdx]);
    const date = cols[dateIdx];

    if (!allCodes.has(code) || isNaN(price) || !date) continue;

    // Find which category this code belongs to
    let catName = null;
    for (const [name, codes] of Object.entries(itemMap)) {
      if (codes.includes(code)) { catName = name; break; }
    }
    if (!catName) continue;

    if (!catData[catName]) catData[catName] = {};
    if (!catData[catName][date]) catData[catName][date] = [];
    catData[catName][date].push(price);
    totalRows++;
  }

  console.log(`[harga-makanan] Aggregated ${totalRows} records for ${Object.keys(catData).length} categories`);

  // Get sorted dates
  const allDates = new Set();
  Object.values(catData).forEach(dates => Object.keys(dates).forEach(d => allDates.add(d)));
  const sortedDates = [...allDates].sort();
  const latestDate = sortedDates[sortedDates.length - 1] || '';

  // Compute prices per category
  const items = [];
  for (const [name, dates] of Object.entries(catData)) {
    const dateKeys = Object.keys(dates).sort().reverse();
    const latestPrices = dates[dateKeys[0]];
    const prevPrices = dateKeys.length >= 2 ? dates[dateKeys[1]] : latestPrices;

    const avgPrice = Math.round(latestPrices.reduce((a, b) => a + b, 0) / latestPrices.length * 100) / 100;
    const prevAvg = Math.round(prevPrices.reduce((a, b) => a + b, 0) / prevPrices.length * 100) / 100;
    const change = Math.round((avgPrice - prevAvg) * 100) / 100;
    const changePct = prevAvg > 0 ? Math.round((change / prevAvg) * 1000) / 10 : 0;
    const minPrice = Math.round(Math.min(...latestPrices) * 100) / 100;
    const maxPrice = Math.round(Math.max(...latestPrices) * 100) / 100;

    const codes = itemMap[name] || [];
    const unit = codeUnit[codes[0]] || '';

    items.push({
      name,
      unit,
      codes,
      price: avgPrice,
      min_price: minPrice,
      max_price: maxPrice,
      prev_price: prevAvg,
      change,
      change_pct: changePct,
      sample_size: latestPrices.length,
      latest_date: dateKeys[0],
    });
  }

  items.sort((a, b) => b.price - a.price);

  const up = items.filter(i => i.change > 0.01).length;
  const down = items.filter(i => i.change < -0.01).length;
  const avg_all = items.length > 0 ? Math.round(items.reduce((s, i) => s + i.price, 0) / items.length * 100) / 100 : 0;

  const result = {
    last_updated: new Date().toISOString(),
    latest_date: latestDate,
    month: usedMonth,
    total_records: totalRows,
    items_count: items.length,
    up, down,
    flat: items.length - up - down,
    avg_price: avg_all,
    items,
    summary: {
      top_5_most_expensive: items.slice(0, 5).map(i => ({ name: i.name, price: i.price })),
      top_5_cheapest: [...items].sort((a, b) => a.price - b.price).slice(0, 5).map(i => ({ name: i.name, price: i.price })),
      biggest_movers: items.filter(i => Math.abs(i.change_pct) > 2).sort((a, b) => Math.abs(b.change_pct) - Math.abs(a.change_pct)).slice(0, 5).map(i => ({ name: i.name, change_pct: i.change_pct, price: i.price })),
    },
  };

  // Update cache
  cache.data = result;
  cache.fetchedAt = Date.now();

  console.log(`[harga-makanan] Done. ${items.length} categories`);
  return result;
}

// ── Handler ──
export const handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': `public, max-age=${CACHE_TTL_MS / 1000}, s-maxage=${CACHE_TTL_MS / 1000}`,
  };

  try {
    const now = Date.now();
    const isStale = !cache.data || !cache.fetchedAt || (now - cache.fetchedAt > STALE_AFTER_MS);

    let data;
    if (isStale) {
      console.log(`[harga-makanan] ${cache.fetchedAt ? 'Stale' : 'Cold start'} — fetching...`);
      data = await fetchAndAggregate();
    } else {
      console.log(`[harga-makanan] Serving cached (${Math.round((now - cache.fetchedAt) / 60000)}min old)`);
      data = cache.data;
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(data),
    };
  } catch (err) {
    console.error(`[harga-makanan] Error: ${err.message}`);
    if (cache.data) {
      return {
        statusCode: 200,
        headers: { ...headers, 'X-Cache-Status': 'stale' },
        body: JSON.stringify({ ...cache.data, _fromCache: true, _error: err.message }),
      };
    }
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Gagal memuatkan data harga' }),
    };
  }
};
