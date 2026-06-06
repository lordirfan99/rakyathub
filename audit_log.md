# Audit Log

## 2026-06-06 10:19
- **QA Check**: Post-build inspection after chart fallback link fix
- **Commit**: `6ace582` — chart: add fallback link to TradingView
- **Changes**: Added `background:#f1f3f6` to chart div; added fallback link "Graf tak nampak? Buka di TradingView →"
- **Build**: 107 pages built in 4.54s — 0 errors
- **Browser Inspection**: Gold calculator page (`/kalkulator/emas/`) verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 0 broken
  - CSS: all loaded successfully
  - Console: 0 errors, 0 warnings
  - New fallback link renders correctly: "Graf tak nampak? Buka di TradingView →"
  - Chart container has `background:#f1f3f6` fallback color
- **Note**: One XHR 404 for `/.netlify/functions/kewangan` — pre-existing, only works on production Netlify, not a regression
- **Status**: resolved

## 2026-06-05 15:54
- **QA Check**: Build verification passed — 75 pages built successfully
- **Command**: `npm run build`
- **Result**: Build: 0 errors, 0 warnings. 75 pages built in 3.96s + 11.52s total. All images reused from cache. No issues detected.
- **Status**: resolved

## 2026-06-05 15:31
- **QA Check**: Build verification passed — 75 pages built successfully
- **Command**: `npm run build`
- **Result**: Build: 0 errors, 0 warnings. 75 pages built in 3.84s (static gen) + 11.24s total. All images reused from cache. No issues detected.
- **Status**: resolved

## 2026-06-05 15:23
- **QA Check**: Build and lint verification passed — 75 pages built successfully
- **Command**: `npm run build`, `npm run check`
- **Result**: Build: 0 errors, 0 warnings. 75 pages built in 11.3s (up from 67). Astro check: 0 errors, 6 hints (pre-existing). ESLint: 117 pre-existing style suggestions (no-var) — down from 127 last run.
- **Status**: resolved

## 2026-06-05 12:39
- **QA Check**: Build and lint verification passed — 67 pages built successfully
- **Command**: `npm run build`, `npm run check`
- **Result**: Build: 0 errors. ESLint: 127 pre-existing issues, 6 fixed (see below)
- **Status**: resolved

### Fixes Applied
- **Fix**: Removed unused `Icon` import
- **File**: `src/components/blog/ListItem.astro:3`
- **Status**: resolved

- **Fix**: Removed unused `getFormattedDate` import
- **File**: `src/components/blog/ListItem.astro:12`
- **Status**: resolved

- **Fix**: Removed unused `Icon` import
- **File**: `src/components/blog/SinglePost.astro:2`
- **Status**: resolved

- **Fix**: Removed unused `getFormattedDate` import
- **File**: `src/components/blog/SinglePost.astro:11`
- **Status**: resolved

- **Fix**: Removed unused `theme` prop destructuring
- **File**: `src/components/widgets/Footer.astro:26`
- **Status**: resolved

- **Fix**: Removed unused `_index` parameter from map callback
- **File**: `src/components/widgets/AppDashboard.astro:163`
- **Status**: resolved

- **Fix**: Removed unused `Brands` import
- **File**: `src/pages/index.astro:8`
- **Status**: resolved

- **Fix**: Removed unused `label` variable
- **File**: `src/pages/kalkulator/zakat.astro:247`
- **Status**: resolved

- **Fix**: Removed unnecessary escape `\/` in regex character class
- **File**: `src/utils/crosslinks.ts:80`
- **Status**: resolved

## 2026-06-05 09:26
- **QA Check**: Build verification passed — 67 pages built successfully
- **Command**: `npm run build`
- **Result**: 0 errors, 0 warnings (exit code 0)
- **Status**: resolved

## 2026-06-05 07:50
- **Fix**: Replaced `netlify` attribute with `data-netlify="true"` to fix TypeScript error (netlify not a valid HTML form attribute)
- **File**: `src/pages/hubungi.astro:37`
- **Before**: `<form netlify name="contact" ...>`
- **After**: `<form data-netlify="true" name="contact" ...>`
- **Status**: resolved

- **Fix**: Added `as const` to variant property to fix TypeScript type mismatch (string vs literal union)
- **File**: `src/navigation.ts:56`
- **Before**: `variant: 'primary'`
- **After**: `variant: 'primary' as const`
- **Status**: resolved

## 2026-06-05 09:02
- **QA Check**: Build verification passed — 47 pages built successfully
- **Command**: `npm run build`
- **Result**: 0 errors, 0 warnings (astro check passed; 127 pre-existing ESLint style suggestions ignored — no impact on build or runtime)
- **Status**: resolved

## 2026-06-05 17:43
- **Fix**: SocialShare aria-label "Kongsi di Twitter" → "Kongsi di X"
- **File**: `src/components/common/SocialShare.astro`
- **Fix**: Logo.astro - removed redundant alt text on logo
- **File**: `src/components/Logo.astro`
- **Fix**: Blog posts H1→H2 heading fix to eliminate duplicate H1 (removed CSS hack in SinglePost.astro)
- **Files**: `src/components/blog/SinglePost.astro`, multiple `src/data/post/*.md`
- **Status**: resolved

## 2026-06-05 17:51
- **QA Check**: Build verification after social share contrast fix (WCAG AA)
- **File**: `src/components/common/SocialShare.astro`
- **Commit**: `891b89a` — icons `text-gray-400`→`text-gray-500`, label `text-slate-500`→`text-slate-600`
- **Command**: `npm run build`
- **Result**: 0 errors, 80 pages built in 12.12s
- **Status**: resolved

## 2026-06-05 20:44
- **QA Check**: Post-build browser inspection after new blog post "Beras Import vs Tempatan"
- **Commit**: `ecaf2b5` — added `beras-import-vs-tempatan-murah.md`, `hero-beli-beras.jpg`
- **Build**: 86 pages built in 12.57s — 0 errors
- **Browser Inspection**: Homepage + new blog post verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 6 loaded, 0 broken
  - Resources: 0 failed (no 404s/5xx)
  - Console: 0 errors, 0 warnings
  - New blog post renders correctly with tables, hero image, tags, social share
- **Status**: resolved

## 2026-06-05 20:55
- **QA Check**: Post-build browser inspection after new blog post "Gaji RM1,800 Breakdown Realistik"
- **Commit**: `179fb24` — added `gaji-rm1800-breakdown-realistik.md`, `hero-gaji-rm1800.jpg`
- **Build**: 97 pages built in 13.49s — 0 errors
- **Browser Inspection**: Homepage + new blog post verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 6 loaded, 0 broken (new hero image HTTP 200, 18.5KB)
  - Resources: 0 failed (no 404s/5xx)
  - Console: 0 errors, 0 warnings
  - New blog post renders correctly with budget tables, 50/30/20 breakdown, side-hustle table, tags, and proper OG meta
- **Status**: resolved

## 2026-06-05 21:26
- **QA Check**: Post-removal rebuild — "X Trend: Scammer trending di Malaysia" removed (too short)
- **Commits**: `07515b8` (add), `b51c137` (remove)
- **Changes**: Deleted `src/data/post/trending-scammer-x-malaysia.md`, `src/assets/images/hero-trend-scammer-x.jpg`
- **Build**: 100 pages built in 13.81s — 0 errors
- **Browser Inspection**: Homepage + blog listing verified after removal
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 5 loaded, 0 broken
  - Resources: 0 failed (no 404s/5xx)
  - Console: 0 errors, 0 warnings
  - Removed article correctly returns HTTP 404
- **Status**: resolved

## 2026-06-05 22:22
- **QA Check**: Favicon & logo rebrand — blue diamond icon scheme
- **Commits**: `21d0425` (Fix: RakyatHub favicon & logo schema)
- **Changes**: Updated `favicon.svg` (blue diamond gradient), binary favicons replaced, JSON-LD logo URLs updated to `rakyathub-logo.png`
- **Build**: 100 pages built in 13.60s — 0 errors
- **Browser Inspection**: Homepage, blog listing, and new comparison post verified
  - DOM: main(1), header(1), nav(1), footer(1) — all present
  - Images: 5 total, 0 broken
  - Resources: 6 entries, 0 failed (no 404s/5xx)
  - CSS: 4 sheets, 0 issues
  - Console: 0 errors, 0 warnings
  - Favicon assets all HTTP 200: favicon.svg (702B), favicon.ico (6723B), apple-touch-icon (4957B)
  - rakyathub-logo.png: HTTP 200 (4957B) — new schema logo reference verified
- **Status**: resolved
