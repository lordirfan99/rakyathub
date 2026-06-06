// Netlify Function: kewangan
// Returns live financial data (gold price, forex, rates) by proxying Yahoo Finance.
// Called by client-side JS from calculator pages.
// No API key required — reads public Yahoo Finance endpoints.
// URL: /.netlify/functions/kewangan

const YAHOO_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

async function yahooFetch(symbol) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`;
  const resp = await fetch(url, { headers: { 'User-Agent': YAHOO_UA } });
  if (!resp.ok) throw new Error(`Yahoo ${symbol}: ${resp.status}`);
  const data = await resp.json();
  return data.chart.result[0].meta.regularMarketPrice;
}

export const handler = async (event, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'public, max-age=600, s-maxage=600',  // 10 min CDN cache
  };

  try {
    // Fetch in parallel
    const [goldUsd, usdMyr] = await Promise.all([
      yahooFetch('GC=F'),
      yahooFetch('USDMYR=X'),
    ]);

    const OPR = 3.0;
    const goldPerGramMyr = (goldUsd / 31.1035) * usdMyr;
    const spreadPg = 5.8;
    const spreadKedai = 12.0;
    const housingLoan = +(OPR + 2.25).toFixed(2);
    const carLoan = +(OPR + 0.3).toFixed(2);
    const fd3 = +(Math.max(OPR - 0.5, 2.0)).toFixed(2);
    const fd12 = +(Math.max(OPR - 0.1, 2.5)).toFixed(2);

    const payload = {
      timestamp: new Date().toISOString(),
      source: 'Netlify Function → Yahoo Finance',
      emas: {
        harga_per_gram: +goldPerGramMyr.toFixed(2),
        gold_usd_per_oz: +goldUsd.toFixed(2),
        usd_myr: usdMyr,
        public_gold: {
          beli: +goldPerGramMyr.toFixed(2),
          jual: +(goldPerGramMyr * (1 - spreadPg / 100)).toFixed(2),
          spread_pct: spreadPg,
        },
        kedai_emas: {
          beli: +goldPerGramMyr.toFixed(2),
          jual: +(goldPerGramMyr * (1 - spreadKedai / 100)).toFixed(2),
          spread_pct: spreadKedai,
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
