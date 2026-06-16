/**
 * harga-makanan.mjs — Auto-refresh grocery price API
 * 
 * No cron needed: traffic-driven caching.
 * - Warm lambda: serves cached data instantly
 * - Stale > 12h: re-fetches from KPDN PriceCatcher Parquet
 * - Cold start: fetches fresh (first visitor after inactivity pays ~3-6s)
 * 
 * Source: KPDN PriceCatcher + DOSM (CC BY 4.0)
 * Domain: rakyathub.my
 */

// ── Constants ──
const ITEM_LOOKUP_URL = 'https://storage.data.gov.my/pricecatcher/lookup_item.parquet';
const STALE_AFTER_MS = 12 * 60 * 60 * 1000;  // 12 hours
const CACHE_TTL_MS = 30 * 60 * 1000;          // Browser cache: 30 min

// ── In-memory cache (persists across warm lambda invocations) ──
let cache = {
  data: null,
  fetchedAt: null,  // when we last fetched from Parquet
};

// ── KEY FOOD ITEMS ──
const KEY_ITEMS = {
  1: "Ayam Standard", 2: "Ayam Super", 3: "Ayam Hidup",
  47: "Daging Lembu Tempatan", 55: "Daging Lembu Import",
  9: "Daging Kambing Import", 14: "Daging Kerbau",
  70: "Ikan Kembung", 71: "Ikan Selayang", 72: "Ikan Selar",
  87: "Ikan Haruan", 88: "Ikan Keli", 89: "Ikan Tilapia",
  16: "Betik", 18: "Pisang Berangan", 22: "Dragon Fruit",
  92: "Cili Hijau", 93: "Cili Merah", 95: "Halia",
  96: "Kacang Bendi", 98: "Kacang Panjang", 104: "Kubis Import",
  105: "Kubis Tempatan", 109: "Lobak Merah", 113: "Timun",
  114: "Terung Panjang", 129: "Bayam", 131: "Sawi", 137: "Kangkung",
  101: "Kelapa", 845: "Beras Super (5kg)", 847: "Beras Import (5kg)",
  1109: "Minyak Masak (5kg)", 1110: "Minyak Masak (1kg)",
  1131: "Gula Pasir Kasar", 1132: "Gula Pasir Halus",
  1440: "Telur Gred A", 1442: "Telur Gred C",
  1481: "Bawang Merah", 1555: "Bawang Putih",
  1819: "Tepung Gandum", 2047: "Santan Kotak",
  2086: "Garam Kasar", 1916: "Susu Cair Manis",
  1926: "Milo", 1928: "Kopi Serbuk",
};

// ── Fetch + Aggregate ──
async function fetchAndAggregate() {
  const now = new Date();
  const monthStr = now.toISOString().slice(0, 7); // "2026-06"
  const pricesUrl = `https://storage.data.gov.my/pricecatcher/pricecatcher_${monthStr}.parquet`;

  console.log(`[harga-makanan] Fetching from ${pricesUrl}`);

  try {
    // Use node-fetch to stream the parquet via http
    // For simplicity, we use the CSV endpoint which works well
    const csvUrl = `https://storage.data.gov.my/pricecatcher/pricecatcher_${monthStr}.csv`;
    console.log(`[harga-makanan] Downloading CSV...`);
    
    const resp = await fetch(csvUrl, { 
      headers: { 'User-Agent': 'RakyatHub/1.0' },
      signal: AbortSignal.timeout(30000)  // 30s timeout — generous for cold start
    });
    
    if (!resp.ok) {
      // Try previous month if current month doesn't exist (early in month)
      if (resp.status === 404) {
        const prev = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const prevMonth = prev.toISOString().slice(0, 7);
        const fallbackUrl = `https://storage.data.gov.my/pricecatcher/pricecatcher_${prevMonth}.csv`;
        console.log(`[harga-makanan] 404, trying ${fallbackUrl}`);
        const fallbackResp = await fetch(fallbackUrl, {
          headers: { 'User-Agent': 'RakyatHub/1.0' },
          signal: AbortSignal.timeout(30000)
        });
        if (!fallbackResp.ok) throw new Error(`Fallback CSV also failed: ${fallbackResp.status}`);
        return await processCSV(await fallbackResp.text(), prev.toISOString().slice(0, 7));
      }
      throw new Error(`CSV fetch failed: ${resp.status}`);
    }
    
    const csvText = await resp.text();
    return await processCSV(csvText, monthStr);
    
  } catch (err) {
    console.error(`[harga-makanan] Error: ${err.message}`);
    // If we have stale cache, serve it rather than failing
    if (cache.data) {
      console.log(`[harga-makanan] Serving stale cache from ${cache.fetchedAt}`);
      return { ...cache.data, _fromCache: true, _cacheAge: Date.now() - cache.fetchedAt };
    }
    throw err;
  }
}

async function processCSV(csvText, monthStr) {
  console.log(`[harga-makanan] Processing ${(csvText.length / 1024 / 1024).toFixed(1)}MB CSV...`);
  
  const lines = csvText.split('\n');
  const header = lines[0].replace('\r', '').split(',');
  console.log(`[harga-makanan] Header: ${header.join(', ')}`);
  console.log(`[harga-makanan] ${lines.length - 1} rows`);
  
  // Find column indices
  const dateIdx = header.indexOf('date');
  const itemIdx = header.indexOf('item_code');
  const priceIdx = header.indexOf('price');
  
  if (dateIdx === -1 || itemIdx === -1 || priceIdx === -1) {
    throw new Error(`Unexpected CSV columns: ${header}`);
  }
  
  // Aggregate prices per item per day
  const itemData = {};  // { itemCode: { date: [prices], ... }, ... }
  let totalRows = 0;
  const keyCodes = new Set(Object.keys(KEY_ITEMS).map(Number));
  
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].replace('\r', '');
    if (!line.trim()) continue;
    
    const cols = line.split(',');
    const code = parseInt(cols[itemIdx]);
    const price = parseFloat(cols[priceIdx]);
    const date = cols[dateIdx];
    
    if (!keyCodes.has(code) || isNaN(price) || !date) continue;
    
    if (!itemData[code]) itemData[code] = {};
    if (!itemData[code][date]) itemData[code][date] = [];
    itemData[code][date].push(price);
    totalRows++;
  }
  
  console.log(`[harga-makanan] Aggregated ${totalRows} records for ${Object.keys(itemData).length} items`);
  
  // Get sorted dates
  const allDates = new Set();
  Object.values(itemData).forEach(dates => Object.keys(dates).forEach(d => allDates.add(d)));
  const sortedDates = [...allDates].sort();
  const latestDate = sortedDates[sortedDates.length - 1] || '';
  
  // Compute latest and previous period averages
  const items = [];
  
  for (const [codeStr, dates] of Object.entries(itemData)) {
    const code = parseInt(codeStr);
    const dateKeys = Object.keys(dates).sort().reverse();
    
    // Latest available prices (use most recent 1-3 days)
    let latestPrices = [];
    let prevPrices = [];
    
    if (dateKeys.length >= 2) {
      latestPrices = dates[dateKeys[0]];
      const prevDay = new Date(dateKeys[0]);
      prevDay.setDate(prevDay.getDate() - 1);
      const prevDateStr = prevDay.toISOString().slice(0, 10);
      prevPrices = dates[dateKeys[1]] || []; // previous available date
    } else if (dateKeys.length === 1) {
      latestPrices = dates[dateKeys[0]];
      prevPrices = [];
    }
    
    const avgPrice = latestPrices.length > 0 
      ? Math.round(latestPrices.reduce((a, b) => a + b, 0) / latestPrices.length * 100) / 100 
      : 0;
    
    const prevAvg = prevPrices.length > 0
      ? Math.round(prevPrices.reduce((a, b) => a + b, 0) / prevPrices.length * 100) / 100
      : avgPrice;
    
    const change = Math.round((avgPrice - prevAvg) * 100) / 100;
    const changePct = prevAvg > 0 ? Math.round((change / prevAvg) * 1000) / 10 : 0;
    
    // Min/max in latest period
    const minPrice = Math.round(Math.min(...latestPrices) * 100) / 100;
    const maxPrice = Math.round(Math.max(...latestPrices) * 100) / 100;
    
    items.push({
      code,
      name: KEY_ITEMS[code] || `Item ${code}`,
      price: avgPrice,
      min_price: minPrice,
      max_price: maxPrice,
      prev_price: prevAvg,
      change,
      change_pct: changePct,
      sample_size: latestPrices.length,
      latest_date: dateKeys[0] || latestDate,
    });
  }
  
  // Compute up/down counts
  const up = items.filter(i => i.change > 0.01).length;
  const down = items.filter(i => i.change < -0.01).length;
  const flat = items.filter(i => Math.abs(i.change) <= 0.01).length;
  
  const result = {
    last_updated: new Date().toISOString(),
    latest_date: latestDate,
    month: monthStr,
    total_records: totalRows,
    items_count: items.length,
    up,
    down,
    flat,
    avg_price: items.length > 0 ? Math.round(items.reduce((s, i) => s + i.price, 0) / items.length * 100) / 100 : 0,
    items: items.sort((a, b) => b.price - a.price),
    summary: {
      top_5_most_expensive: items.sort((a, b) => b.price - a.price).slice(0, 5).map(i => ({ name: i.name, price: i.price })),
      top_5_cheapest: items.sort((a, b) => a.price - b.price).slice(0, 5).map(i => ({ name: i.name, price: i.price })),
      biggest_movers: items.filter(i => Math.abs(i.change_pct) > 2).sort((a, b) => Math.abs(b.change_pct) - Math.abs(a.change_pct)).slice(0, 5).map(i => ({ name: i.name, change_pct: i.change_pct, price: i.price })),
    },
  };
  
  // Update cache
  cache.data = result;
  cache.fetchedAt = Date.now();
  
  console.log(`[harga-makanan] Done. ${items.length} items, latest: ${latestDate}`);
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
    // Check if cache is stale or missing
    const now = Date.now();
    const isStale = !cache.data || !cache.fetchedAt || (now - cache.fetchedAt > STALE_AFTER_MS);
    const isColdStart = !cache.fetchedAt;
    
    let data;
    
    if (isStale) {
      console.log(`[harga-makanan] ${isColdStart ? 'Cold start' : 'Stale'} — fetching fresh data...`);
      data = await fetchAndAggregate();
    } else {
      console.log(`[harga-makanan] Serving cached data (age: ${Math.round((now - cache.fetchedAt) / 60000)}min)`);
      data = cache.data;
    }
    
    // Check if client wants a specific item
    const params = event.queryStringParameters || {};
    if (params.item) {
      const itemCode = parseInt(params.item);
      const itemData = data.items.find(i => i.code === itemCode);
      if (itemData) {
        data = { ...data, item: itemData };
      }
    }
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(data),
    };
    
  } catch (err) {
    console.error(`[harga-makanan] Handler error: ${err.message}`);
    
    // Serve stale cache on error
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
      body: JSON.stringify({ error: 'Gagal memuatkan data harga', _message: err.message }),
    };
  }
};
