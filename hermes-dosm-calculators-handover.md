# Hermes Handover — DOSM Data Calculators (RakyatHub)

## Context

RakyatHub (https://rakyathub.my) has three new DOSM-powered calculators built at:
- `/kalkulator/pendapatan-percentile/` — Income Percentile (B40/M40/T20)
- `/kalkulator/kuasa-beli/` — Purchasing Power / Inflation Tracker
- `/kalkulator/benchmark-gaji/` — Salary Benchmark by Sector

These pages use **static JSON data files** embedded at build time (no live API calls). All three data files live in `src/data/`:

| File | Purpose | Source | Year |
|---|---|---|---|
| `hies-percentile.json` | Income percentile thresholds + state medians | DOSM HIES | 2022 |
| `salary-data.json` | Sector wage data (median, P25, P75, growth %) + state multipliers | DOSM Salaries & Wages Survey + EPF/SOCSO | 2023 |
| `cpi.json` | CPI by year + category indexes | DOSM CPI | Updated monthly |

---

## Your Tasks

### Task 1 — Refresh DOSM Data (Annual)

When DOSM publishes new HIES or Salaries & Wages data, update the JSON files:

#### `src/data/hies-percentile.json`
Update from: https://open.dosm.gov.my/data-catalogue/hies_malaysia_percentile
API: `https://api.data.gov.my/data-catalogue?id=hies_malaysia_percentile`

Fields to update:
- `year` — change to new survey year
- `b40_cutoff` — bottom 40th percentile threshold
- `m40_upper` — 80th percentile threshold (T20 cutoff)
- `median` — national median monthly household income
- `mean` — national mean monthly household income
- `national_percentiles` — array of {p, income} for p = 5,10,15,...,95,99
- `states` — each state's `median` and `mean` from `hies_state_percentile`

State data API: `https://api.data.gov.my/data-catalogue?id=hies_state_percentile`

#### `src/data/salary-data.json`
Update from: https://open.dosm.gov.my/data-catalogue (search "salaries wages")
API: `https://api.data.gov.my/data-catalogue?id=salaries_wages_2023` (update year suffix)

Fields to update:
- `year` — new publication year
- `national_median` — national median employee salary
- `national_mean` — national mean employee salary
- For each sector: `median`, `mean`, `p25`, `p75`, `growth_pct`
- For each state: `median` and recalculate `multiplier` = state_median / national_median

State multiplier formula: `multiplier = state.median / national_median`

#### `src/data/cpi.json`
This is already updated monthly by existing scripts. No action needed unless the category structure changes.

---

### Task 2 — SEO Quality Check on New Pages

Run these checks on each new calculator page:

#### `/kalkulator/pendapatan-percentile/`
Expected metadata:
- Title: `Kalkulator Tangga Pendapatan Malaysia — B40, M40 atau T20?` (≤49 chars for brand-free)
- Meta description: 140-160 chars, includes keywords: tangga pendapatan, B40 M40 T20, DOSM HIES 2022
- H1 must be present and match intent
- No broken links

#### `/kalkulator/kuasa-beli/`
Expected metadata:
- Title: `Kalkulator Kuasa Beli — Inflasi & Nilai Wang Malaysia`
- Meta description: includes keywords: kuasa beli, inflasi, CPI Malaysia
- No broken links

#### `/kalkulator/benchmark-gaji/`
Expected metadata:
- Title: `Kalkulator Benchmark Gaji Malaysia 2024 — Setimpal Pasaran?`
- Meta description: includes keywords: benchmark gaji, median gaji, DOSM 2023
- No broken links

Verify the `src/pages/kalkulator/index.astro` has all three new calculators in the `newCalcs` array.

---

### Task 3 — Validate Data Freshness

For each data file, check if newer data is available:

1. Check https://open.dosm.gov.my/data-catalogue for HIES updates (usually every 2-3 years)
2. Check https://open.dosm.gov.my/publications for latest Salaries & Wages report
3. Check `cpi.json` — `latest_date` should be within 60 days of today

If CPI `latest_date` is older than 60 days, flag it. The `cpi.json` update script is likely broken.

---

### Task 4 — Add JSON-LD Structured Data

Each calculator needs a `WebApplication` JSON-LD schema. For each page, add inside `<Layout>`:

```astro
<script type="application/ld+json" set:html={JSON.stringify({
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "PAGE_TITLE",
  "url": "https://rakyathub.my/kalkulator/PAGE_SLUG/",
  "description": "PAGE_DESCRIPTION",
  "applicationCategory": "FinanceApplication",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "MYR" },
  "operatingSystem": "Web"
})} />
```

Replace PAGE_TITLE, PAGE_SLUG, PAGE_DESCRIPTION for each page.

---

### Task 5 — Link Interlinking

Each new calculator should link to relevant existing calculators. Verify these cross-links exist:

**pendapatan-percentile** should link to:
- `/kalkulator/gaji-bersih/` (Kira gaji bersih anda)
- `/kalkulator/pcb-cukai-pendapatan/` (Kira cukai pendapatan)
- `/kalkulator/str-sara/` (STR SARA semak kelayakan)

**kuasa-beli** should link to:
- `/inflasi-malaysia/` (Papan pemuka inflasi)
- `/kalkulator/interest-compound/` (Kesan compounding vs inflasi)
- `/kalkulator/fd/` (FD vs inflasi)

**benchmark-gaji** should link to:
- `/kalkulator/gaji-bersih/` (Kira gaji bersih selepas potongan)
- `/kalkulator/kenaikan-gaji/` (Unjur kenaikan gaji)
- `/kalkulator/pcb-cukai-pendapatan/` (Kira cukai pendapatan)

---

## File Locations Reference

```
src/
  data/
    hies-percentile.json     ← HIES 2022 percentile + state data
    salary-data.json         ← Sector wage benchmarks + state multipliers
    cpi.json                 ← CPI by year + category indexes (monthly update)
  pages/
    kalkulator/
      pendapatan-percentile.astro
      kuasa-beli.astro
      benchmark-gaji.astro
      index.astro              ← Calculator hub (has all three in newCalcs[])
```

---

## Priority Order

1. **Task 3** — Data freshness check (do first, before any SEO work)
2. **Task 2** — SEO quality on new pages
3. **Task 4** — JSON-LD structured data
4. **Task 5** — Cross-links
5. **Task 1** — Only when DOSM publishes new data

---

## Contact

Owner: irfanthefast@gmail.com
Site: https://rakyathub.my
Repo: lordirfan99/rakyathub (branch: main)
