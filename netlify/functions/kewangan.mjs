// Netlify Function: kewangan
// Returns live financial data (gold price, forex, rates) + optional chart data.
// Primary source: scrapes Public Gold GAP 24K price directly.
// Fallback: Yahoo Finance spot for international reference.
// Chart data: pass ?chart=1M (daily), ?chart=3M (weekly), ?chart=1Y (monthly)
// Called by client-side JS from calculator pages.
// URL: /.netlify/functions/kewangan

const YAHOO_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

async function yahooFetch(symbol) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`;
  const resp = await fetch(url, { headers: { 'User-Agent': YAHOO_UA } });
  if (!resp.ok) throw new Error(`Yahoo ${symbol}: ${resp.status}`);
  const data = await resp.json();
  return data.chart.result[0].meta.regularMarketPrice;
}

// Fetch historical chart data from Yahoo Finance
async function yahooChart(symbol, range, interval) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?range=${range}&interval=${interval}`;
  const resp = await fetch(url, { headers: { 'User-Agent': YAHOO_UA } });
  if (!resp.ok) throw new Error(`Yahoo chart ${symbol}: ${resp.status}`);
  const data = await resp.json();
  const result = data.chart.result[0];
  const timestamps = result.timestamp;
  const quotes = result.indicators.quote[0];
  const usdMyr = await yahooFetch('USDMYR=X'); // convert to RM
  return timestamps.map((t, i) => ({
    date: new Date(t * 1000).toISOString().slice(0, 10),
    usd: +(quotes.close[i] || quotes.close[i - 1] || 0).toFixed(2),
    rm: +(((quotes.close[i] || quotes.close[i - 1] || 0) / 31.1035) * usdMyr).toFixed(2),
  })).filter(p => p.usd > 0);
}

// Scrape actual Public Gold GAP 24K price from goldofficial.me
async function scrapePGGapPrice() {
  const resp = await fetch('https://goldofficial.me/z/harga-emas-hari-ini', {
    headers: { 'User-Agent': YAHOO_UA },
  });
  if (!resp.ok) throw new Error(`PG scrape: ${resp.status}`);
  const html = await resp.text();
  // Match: "harga emas 999 hari ini adalah RM611 per gram"
  const match = html.match(/harga emas 999 hari ini adalah\s*RM(\d+)\s*per\s*gram/i);
  if (!match) throw new Error('PG scrape: could not parse price');
  return parseInt(match[1], 10);
}

export const handler = async (event, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'public, max-age=600, s-maxage=600',  // 10 min CDN cache
  };

  try {
    const params = event.queryStringParameters || {};
    const chartRange = params.chart || null;

    const OPR = 3.0;
    const housingLoan = +(OPR + 2.25).toFixed(2);
    const carLoan = +(OPR + 0.3).toFixed(2);
    const fd3 = +(Math.max(OPR - 0.5, 2.0)).toFixed(2);
    const fd12 = +(Math.max(OPR - 0.1, 2.5)).toFixed(2);

    // Try to get actual PG GAP 24K price first
    let pgGapPrice = null;
    let goldUsd = null;
    let usdMyr = null;
    let goldPerGramMyr = null;

    try {
      pgGapPrice = await scrapePGGapPrice();
    } catch (e) {
      // Fallback: calculate from spot
      console.log('PG scrape failed, falling back to spot:', e.message);
    }

    // Get spot prices for reference
    try {
      [goldUsd, usdMyr] = await Promise.all([
        yahooFetch('GC=F'),
        yahooFetch('USDMYR=X'),
      ]);
      goldPerGramMyr = (goldUsd / 31.1035) * usdMyr;
    } catch (e) {
      // If spot also fails and we have PG price, that's OK — only need it for reference
      console.log('Yahoo fetch failed:', e.message);
    }

    const pgBeli = pgGapPrice || (goldPerGramMyr ? +(goldPerGramMyr * 1.025).toFixed(2) : 611);
    const pgJual = pgGapPrice
      ? pgGapPrice
      : (goldPerGramMyr ? +(goldPerGramMyr * 0.942).toFixed(2) : 560);

    // Fetch chart data if requested
    let chartData = null;
    if (chartRange) {
      const rangeMap = { '1M': ['1mo','1d'], '3M': ['3mo','1wk'], '1Y': ['1y','1mo'] };
      const [range, interval] = rangeMap[chartRange] || ['1mo','1d'];
      try {
        chartData = await yahooChart('GC=F', range, interval);
      } catch (e) {
        console.log('Chart fetch failed:', e.message);
      }
    }

    const payload = {
      timestamp: new Date().toISOString(),
      source: pgGapPrice ? 'Netlify Function → PG GAP 24K (Direct)' : 'Netlify Function → Yahoo Finance',
      emas: {
        harga_per_gram: goldPerGramMyr ? +goldPerGramMyr.toFixed(2) : pgGapPrice,
        harga_pg_beli: pgBeli,
        harga_pg_jual: pgJual,
        gold_usd_per_oz: goldUsd ? +goldUsd.toFixed(2) : null,
        usd_myr: usdMyr || null,
        public_gold: {
          beli: pgBeli,
          jual: pgJual,
        },
      },
      kadar: {
        opr: OPR,
        housing_loan_pct: housingLoan,
        car_loan_pct: carLoan,
        fd_3month_pct: fd3,
        fd_12month_pct: fd12,
      },
      rujukan: {
        asb_dividen_terkini: 5.75,
        kwsp_dividen_terkini: 6.15,
        epf_pekerja_pct: 11.0,
        sst_barang_pct: 8.0,
        sst_perkhidmatan_pct: 6.0,
        str_maksimum: 3700,
        sara_maksimum: 2400,
      },
      zakat: {
        nisab_gram: 85,
        nisab_rm: +(goldPerGramMyr * 85).toFixed(2),
        kadar_pct: 2.5,
      },
    };

    if (chartData) {
      payload.chart = chartData;
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(payload),
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: err.message }),
    };
  }
};
