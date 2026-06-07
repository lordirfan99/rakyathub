# Audit Log

## 2026-06-07 16:09
- **QA Check**: Content-only build — 1 new blog post + image fix commit
- **Commit**: `6013945` — fix: remove duplicate hero image; plus untracked new post `ringgit-mengukuh-apa-maksud-duit-korang`
- **Changes**: `hero-diskaun-kad-pelajar-malaysia.jpg` deleted (duplicate, same hash as `hero-cara-urus-duit-elaun-belajar`). New untracked post: `ringgit-mengukuh-apa-maksud-duit-korang.md` + `hero-ringgit-mengukuh-2026.jpg`
- **Pre-build**: No untracked `.astro` files in `src/pages/` — clean
- **Proactive Duplicate Image Detection**: `hero-ringgit-mengukuh-2026.jpg` — unique hash, no duplicates found ✅
- **Build**: 187 pages built in 27.84s — 0 errors, 0 warnings (up from 183 pages — +1 post + tag/category auto-generated pages)
- **Content Fast-Path (Step 1d)**: No .astro/.ts/.js changes — skipped CDP browser session. Verified via curl on port 3102 (clean port, Python http.server)
- **Content Asset Verification**:
  - /ringgit-mengukuh-apa-maksud-duit-korang/ — title "Ringgit Mengukuh 3.3% — Apa Maksud Untuk Duit Korang? — RakyatHub" ✅
  - OG Image: `/_astro/hero-ringgit-mengukuh-2026.Bh0ZKFnM_qszPG.jpg` (correct, matches frontmatter) ✅
  - Image asset HTTP 200, 73,546 bytes ✅
  - /category/kewangan/ — title "Category 'Kewangan' — RakyatHub" ✅
- **Cross-Image Check**: Rendered OG image file base (hero-ringgit-mengukuh-2026) matches frontmatter `image:` field — correct image used, no fallback issue ✅
- **Status**: resolved

## 2026-06-07 13:25
- **QA Check**: Content-only build — 2 new student articles
- **Commit**: `76bd981` — Auto [Student]: Idea bisnes modal kecil untuk student, Diskaun kad pelajar Malaysia
- **Changes**: 2 new `.md` posts in `src/data/post/`, 2 new hero images in `src/assets/images/`
- **Pre-build**: No untracked `.astro` files in `src/pages/` — clean
- **Build**: 183 pages built in 29.32s — 0 errors, 0 warnings
- **Content Fast-Path (Step 1d)**: No .astro/.ts/.js changes — skipped CDP browser session. Verified via curl on port 3101 (clean port, Node.js static server)
- **Content Verification**:
  - /idea-bisnes-modal-kecil-untuk-student/ — title "10 Idea Bisnes Modal Kecil Untuk Student (2026) — RakyatHub" ✅
    - OG Image: hero-idea-bisnes-modal-kecil-untuk-student (correct) ✅
  - /diskaun-kad-pelajar-malaysia/ — title "10 Diskaun Kad Pelajar Malaysia Yang Ramai Student Tak Tahu — RakyatHub" ✅
    - OG Image: was wrong (showed `hero-cara-urus-duit-elaun-belajar`) — see fix below
- **Fix**: Duplicate image detected — `hero-diskaun-kad-pelajar-malaysia.jpg` was an exact bit-for-bit copy of `hero-cara-urus-duit-elaun-belajar.jpg` (same git hash `ee4578a`). Vite deduplicates identical-content images, causing the wrong image to render on the page. Removed the duplicate file (`git rm src/assets/images/hero-diskaun-kad-pelajar-malaysia.jpg`). Page now correctly falls back to the default site OG image.
- **File**: `src/assets/images/hero-diskaun-kad-pelajar-malaysia.jpg`
- **Before**: Post showed unrelated hero image (cara-urus-duit-elaun-belajar)
- **After**: Duplicate removed; post uses default site OG image. User needs to upload the correct hero image for this post.
- **Status**: resolved (partial — correct image needs to be uploaded by author)

## 2026-06-07 12:05
- **QA Check**: Content-only build — 4 new blog posts
- **Commit**: `af07c49` — Auto: 4 artikel baharu — i-Saraan KWSP, Emas Fizikal vs Digital, Panduan Medical Card, Bajet Kahwin
- **Changes**: 4 new `.md` posts in `src/data/post/`, 4 new hero images in `src/assets/images/`
- **Pre-build**: No untracked `.astro` files in `src/pages/` — clean
- **Build**: 183 pages built in 31.47s — 0 errors, 0 warnings
- **Content Fast-Path (Step 1d)**: No .astro/.ts/.js changes — skipped CDP browser session
- **Content Asset Verification**:
  - /bajet-kahwin-malaysia-2026-cara-simpan-dan-urus/ — title "Bajet Kahwin Malaysia 2026 — Cara Simpan dan Urus Duit Nikah — RakyatHub" ✅
  - /emas-fizikal-vs-emas-digital-mana-lebih-untung/ — title "Emas Fizikal vs Emas Digital — Mana Strategi Terbaik 2026? — RakyatHub" ✅
  - /i-saraan-kwsp-2026-cara-daftar-insentif-padanan/ — title "i-Saraan KWSP 2026 — Cara Daftar & Dapat Insentif 20% Percuma — RakyatHub" ✅
  - /panduan-medical-card-malaysia-2026-first-time-buyer/ — title "Panduan Medical Card Malaysia 2026 — Untuk First Time Buyer — RakyatHub" ✅
  - All 4 hero images: HTTP 200 ✅ (JPG + WebP variants all served)
  - Category pages: Kewangan, Emas, KWSP, Insurans — all correct titles ✅
- **Pages built**: 183 (up from 155 — +4 posts + tag/category auto-generated pages)
- **Status**: resolved

## 2026-06-06 21:48
- **QA Check**: Post-build browser inspection — emas calculator reference price fix
- **Commit**: `0c41e71` — fix(emas): harga rujukan now follows harga semasa input in real-time
- **Changes**: Added 3 lines to `src/pages/kalkulator/emas.astro` in `calc()` — `rujPgBeli` and `rujPgJual` now update with current `harga`
- **Pre-build**: No untracked `.astro` files in `src/pages/` — clean
- **Build**: 155 pages built in 27.08s — 0 errors, 0 warnings
- **Browser Inspection**: Full CDP on port 3015 (Node.js fallback static server)
  - DOM structure: main(1), header(1), nav(1), footer(1), cookie banner — all present
  - Images: 0 broken
  - CSS: all loaded (0 failed stylesheets)
  - Console: 0 errors, 0 warnings
  - JS: `calc()` function defined, `harga` and `berat` inputs present, `rujPgBeli`/`rujPgJual` elements present
  - **Fix verified**: Changing harga from 420 → 500 updated `rujPgBeli` to "RM 500.00" and `rujPgJual` to "RM 500.00" in real-time ✅
- **Pages verified**: homepage, /kalkulator/emas/, /category/kewangan/ — all correct titles
- **Note**: Two XHR 404s for `/.netlify/functions/kewangan` — pre-existing, production-only Netlify functions, handled gracefully
- **Status**: resolved

## 2026-06-06 21:37
- **QA Check**: Content-only build — new blog post "Inflasi Malaysia Cecah 1.9% — 5 Langkah Lindung Duit Korang"
- **Commit**: `4bfab88` — Auto: News React — Inflasi Malaysia Cecah 1.9%, 5 Langkah Lindung Duit (6 Jun 2026)
- **Changes**: New post `inflasi-malaysia-april-1.9-peratus-lindung-duit-2026.md`, new hero image `hero-inflasi-malaysia.jpg`, 5 parse scripts
- **Build**: 155 pages built in 9.30s — 0 errors, 0 warnings
- **Content Fast-Path (Step 1d)**: No .astro/.ts/.js changes — skipped CDP browser session
- **Content Asset Verification**:
  - New post page: title "Inflasi Malaysia Cecah 1.9% — 5 Langkah Bijak Lindung Duit Korang — RakyatHub" ✅
  - Hero image JPG (OG variant): HTTP 200, 79994 bytes ✅
  - Hero image WebP (Astro-processed): HTTP 200, 9846 bytes ✅
  - Canonical URL: `https://rakyathub.my/inflasi-malaysia-april-19-peratus-lindung-duit-2026` ✅
  - Tag page /tag/inflasi/ — title "Posts by tag 'inflasi' — RakyatHub" ✅ (auto-created)
- **Status**: resolved

## 2026-06-06 11:17
- **QA Check**: Post-build inspection after blog images fix (Vite glob key path correction)
- **Commit**: `c2cf9ac` — fix: blog images broken — findImage() key path /src/ vs ./src/ (Vite glob format)
- **Changes**: `debug_images.mjs` deleted, `debug_key.mjs` deleted, `src/utils/images.ts` changed (./src/ → /src/)
- **Build**: 137 pages built in 18.71s — 0 errors, 0 warnings
- **Browser Inspection**: Full CDP inspection on port 3009 via Node.js static server (dist/)
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 0 broken
  - Resources: 0 failed (no 404s/4xx/5xx)
  - Console: 0 errors, 0 warnings
- **Subdirectory pages verified**:
  - /category/kewangan/ — title "Category 'Kewangan' — RakyatHub"
  - /blog/ — title "Blog — RakyatHub"
  - /quishing-scam-qr-code-malaysia-cara-lindung-diri/ — title "⚠️ Quishing Dah Sampai Malaysia! Jangan Scan QR Sembarangan — RakyatHub"
- **Content Asset Verification**:
  - Hero image OG variant: HTTP 200, 51607 bytes
- **Node.js fallback server** used on port 3009 (ports 3000-3008 had zombie listeners)
- **Status**: resolved

## 2026-06-06 11:05
- **QA Check**: Post-build inspection after new Quishing article + debug file cleanup
- **Commit**: `c0f8222` — Auto: News React - Quishing QR code scam Malaysia cara lindung diri
- **Fix**: Removed untracked debug file `src/pages/test-images.astro` (missing frontmatter, blocked build with `Expected "}" but found ";"` esbuild syntax error)
- **File**: `src/pages/test-images.astro`
- **Build**: 137 pages built in 21.70s — 0 errors (after fix)
- **Browser Inspection**: Homepage, new quishing article, Kewangan category page verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 10 total, 0 broken
  - Resources: 0 failed (no 404s/5xx)
  - Console: 0 errors, 0 warnings
  - Hero image assets all HTTP 200: JPG (77KB), WebP variants (7KB, 19KB), OG JPG (52KB)
  - OG meta tags correctly reference processed hero image
  - New article renders correctly on homepage, category page, and standalone page
- **Content Asset Verification**:
  - /quishing-scam-qr-code-malaysia-cara-lindung-diri/ — title "⚠️ Quishing Dah Sampai Malaysia! Jangan Scan QR Sembarangan — RakyatHub"
  - /category/kewangan/ — title "Category 'Kewangan' — RakyatHub"
  - Hero image OG variant: HTTP 200, 51607 bytes
  - Subcategory page /category/kewangan/ — correct title
- **Status**: resolved

## 2026-06-06 10:58
- **QA Check**: Post-build inspection after takaful article crosslinks + MAX_LINKS 2→8
- **Commit**: `5315355` — fix: tambah link pada bold keywords artikel takaful + naikkan had crosslink 2->8
- **Build**: 107 pages built in 16.29s — 0 errors
- **Browser Inspection**: Homepage + takaful article + subdirectory pages verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 5 total, 0 broken
  - Resources: 7 entries, 0 failed (no 404s/5xx)
  - CSS: 4 sheets, 0 issues
  - Console: 0 errors, 0 warnings
  - New crosslinks verified in takaful article: /cadangan-bajet-50-30-20-di-malaysia/, /kalkulator/kwsp/, external PolicyStreet/Qoala links, /kalkulator/zakat-pendapatan/
  - Subdirectory pages verified:
    - /category/insurans/ — title "Category 'Insurans' — RakyatHub"
    - /kalkulator/kwsp/ — title "Kalkulator KWSP — Simulasi Caruman & Persaraan — RakyatHub"
    - /kalkulator/zakat-pendapatan/ — title "Kalkulator Zakat Pendapatan — 2.5% — RakyatHub"
    - /cadangan-bajet-50-30-20-di-malaysia/ — title "Panduan Bajet 50/30/20 di Malaysia — Cara Urus Gaji Setiap Bulan — RakyatHub"
  - Hero image: HTTP 200, 63KB
- **Status**: resolved

## 2026-06-06 10:46
- **QA Check**: Post-build inspection after chart zero-dependency rewrite (pure Canvas API)
- **Commit**: `0556791` — fix(chart): pure Canvas API chart, zero dependencies, no CDN
- **Build**: 107 pages built in 16.00s — 0 errors, 0 warnings
- **Browser Inspection**: Gold calculator page (`/kalkulator/emas/`) verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 1 total, 0 broken
  - CSS: 3 sheets, 0 issues
  - JS: 10 scripts loaded (inline + ClientRouter), no CDN scripts
  - Console: 0 errors, 0 warnings
  - No more Chart.js CDN dependency — chart renders via pure Canvas API
  - Chart handles API fetch failure gracefully ("Gagal muat data.")
- **Subdirectory pages verified**:
  - /category/kewangan/ — title "Category 'Kewangan' — RakyatHub"
  - /blog/ — title "Blog — RakyatHub"
  - / — title "RakyatHub — Panduan Kewangan Rakyat Malaysia"
- **Note**: Two XHR 404s for `/.netlify/functions/kewangan` — expected (production-only Netlify functions, handled gracefully)
- **Status**: resolved

## 2026-06-06 10:33
- **QA Check**: Post-build inspection after broken footer link fix
- **Commit**: `5a0c2f6` — remove broken /category/asb and /category/emas footer links, replace with working categories (Kewangan, Kerajaan, Insurans)
- **Build**: 107 pages built in 16.07s — 0 errors
- **Browser Inspection**: Homepage + new category pages verified
  - DOM structure: main(1), header(1), nav(1), footer(1) — all present
  - Images: 5 total, 0 broken
  - Resources: 7 entries, 0 failed (no 404s)
  - CSS: 4 sheets, 0 issues
  - Console: 0 errors, 0 warnings
  - New category links verified HTTP 200:
    - /category/kewangan/ — title "Category 'Kewangan' — RakyatHub"
    - /category/kerajaan/ — title "Category 'Kerajaan' — RakyatHub"
    - /category/insurans/ — title "Category 'Insurans' — RakyatHub"
  - Old broken links (/category/asb, /category/emas) removed from footer
- **Status**: resolved

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
