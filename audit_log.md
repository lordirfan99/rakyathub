# Audit Log

## 2026-06-13 12:41
- **QA Check**: Content-only build — expand resume article for word count (fresh graduate resume tips)
- **Commit**: `8a90e02` — Auto [Student]: expand resume article for word count
- **Changes**: `src/data/post/contoh-resume-fresh-graduate-tiada-pengalaman.md` (word count expansion — added "Contoh untuk student bisnes" section with market research example, more detail on project descriptions with measurable impact, and guidance on team roles)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅; no new images in commit ✅
- **Duplicate Image Detection**: No new images in this commit ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (`hero-test-a.jpg`, `hero-test-b.jpg`, `hero-saham-usa.jpg`, `cta-join-discord.png` in src/assets; 20+ public/images/ and public/root files) — user should `git rm` when convenient
- **Build**: 535 pages built successfully (15.50s) — used cache ✅ (up from 531 pages — new articles from earlier commits now indexed)
- **Content Verification** (curl on port 4000, Node.js static server serving from dist/):
  - `/contoh-resume-fresh-graduate-tiada-pengalaman/` — title "Contoh Resume Fresh Graduate Tiada Pengalaman — RakyatHub" ✅
  - OG Image: `/_astro/hero-contoh-resume-fresh-graduate-tiada-pengalaman.DnW-H7rC_ZuA4M8.jpg` — HTTP 200, 19,499 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-contoh-resume-fresh-graduate-tiada-pengalaman.jpg"` — active (not commented) ✅
  - New content "Contoh untuk student bisnes" present (1 occurrence) ✅
  - New content "kajian pasaran tentang tabiat perbelanjaan" present (1 occurrence) ✅
  - `/category/kerjaya/` — "Category 'Kerjaya' — RakyatHub" ✅
  - `/blog/` — "Blog — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-13 10:22
- **QA Check**: Content-only build — 1 new Kerjaya article (Career Switch — Tukar Kerjaya di Malaysia 2026)
- **Commit**: `338cf2c` — Auto: Kerjaya - Career Switch (Tukar Kerjaya) di Malaysia 2026
- **Changes**: `src/data/post/panduan-lengkap-tukar-kerjaya-malaysia-2026.md` (new post — 169 lines, comprehensive career switch guide in Malaysia including salary comparisons, gaji selepas bertukar, langkah tukar kerjaya); `src/assets/images/hero-panduan-lengkap-tukar-kerjaya-malaysia-2026.jpg` (new hero image, ~1.5MB — hash `4f4d136`, unique ✅); `audit_log.md` (updated by content pipeline)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅; git status clean ✅
- **Duplicate Image Detection**: New image hash `4f4d136413998fe0fe7671a41cd879c80f0cf542` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 531 pages built successfully (13.20s) — clean rebuild ✅ (up from 527 pages — 1 new article + tag/category pages)
- **Content Verification** (direct from built dist/):
  - `/panduan-lengkap-tukar-kerjaya-malaysia-2026/` — title "Career Switch (Tukar Kerjaya) di Malaysia 2026 — Panduan Lengkap & Gaji Selepas Bertukar — RakyatHub" ✅
  - OG Image: `/_astro/hero-panduan-lengkap-tukar-kerjaya-malaysia-2026.BatgAWRd_16NsX2.jpg` — processed by Sharp with 4 variants (2 JPG, 2 WebP) ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-panduan-lengkap-tukar-kerjaya-malaysia-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kerjaya/` — "Category 'Kerjaya' — RakyatHub" ✅
  - `/tag/career-switch/` — new tag page renders ✅
  - `/tag/tukar-kerjaya/` — new tag page renders ✅
  - `/tag/kerjaya-malaysia-2026/` — new tag page renders ✅
  - `/tag/gaji-terkini/` — new tag page renders ✅
  - `/tag/perancangan-kerjaya/` — new tag page renders ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-13 09:13
- **QA Check**: Content-only build — 4 new articles (ASB 2, Bonus ASB, SARA 2026, Versa vs KDI vs TNG GO+)
- **Commit**: `b862ca0` — Auto: 4 new articles - ASB 2, Bonus ASB, SARA 2026, Versa vs KDI vs TNG GO+
- **Changes**: 4 new `.md` posts (`asb-2-panduan-lengkap-simpanan-berkala-2026.md`, `bonus-asb-cara-kira-dan-beza-dengan-dividen.md`, `sara-2026-sumbangan-asas-rahmah-panduan-lengkap.md`, `versa-vs-kdi-vs-tng-go-platform-simpanan-alternatif-2026.md`); 4 new hero images (`hero-asb2-panduan-lengkap.jpg`, `hero-bonus-asb-cara-kira.jpg`, `hero-sara-2026-panduan-lengkap.jpg`, `hero-versa-kdi-tng-go-simpanan-alternatif.jpg`); `audit_log.md` (updated by content pipeline)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅; git status clean ✅
- **Duplicate/Orphaned Image Detection**: All 4 new images unique — no duplicates found ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (previously noted: `hero-test-a.jpg`, `hero-test-b.jpg`, `hero-saham-usa.jpg`, `cta-join-discord.png` in src/assets; 20+ public/images/ and public/root files) — user should `git rm` when convenient
- **Build**: 527 pages built successfully (11.87s) — clean rebuild ✅ (up from 507 pages — 4 new articles + tag/category pages)
- **Content Verification** (curl on port 3500, Node.js static server serving from dist/ with directory→index.html):
  - `/asb-2-panduan-lengkap-simpanan-berkala-2026/` — title "ASB 2 2026 — Panduan Lengkap Simpanan Berkala & Perbandingan dengan ASB Biasa — RakyatHub" ✅
  - OG Image: `/_astro/hero-asb2-panduan-lengkap.HImpS4_o_ZiitYy.jpg` — HTTP 200, 72,744 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-asb2-panduan-lengkap.jpg"` — active (not commented) ✅
  - `/bonus-asb-cara-kira-dan-beza-dengan-dividen/` — title "Bonus ASB 2026 — Cara Kira & Beza Dengan Dividen ASB — RakyatHub" ✅
  - OG Image: `/_astro/hero-bonus-asb-cara-kira.DUTiW6IP_2eqXeW.jpg` — HTTP 200, 26,302 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-bonus-asb-cara-kira.jpg"` — active (not commented) ✅
  - `/sara-2026-sumbangan-asas-rahmah-panduan-lengkap/` — title "SARA 2026 — Sumbangan Asas Rahmah & Panduan Lengkap Guna MyKad — RakyatHub" ✅
  - OG Image: `/_astro/hero-sara-2026-panduan-lengkap.D0Ujxuhi_ZyRT2U.jpg` — HTTP 200, 213,770 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-sara-2026-panduan-lengkap.jpg"` — active (not commented) ✅
  - `/versa-vs-kdi-vs-tng-go-platform-simpanan-alternatif-2026/` — title "Versa vs KDI vs TNG GO+ — Platform Simpanan Alternatif 2026 — RakyatHub" ✅
  - OG Image: `/_astro/hero-versa-kdi-tng-go-simpanan-alternatif.DjrLtoFp_Z1lYYLn.jpg` — HTTP 200, 49,186 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-versa-kdi-tng-go-simpanan-alternatif.jpg"` — active (not commented) ✅
  - `/category/asb/` — "Category 'ASB' — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-12 20:38
- **QA Check**: Text-only component change — related posts 4→8, +20 cross-link keywords for orphan pages
- **Commit**: `ad1e484` — fix: gandakan related posts 4->8, +20 cross-link keywords untuk orphan pages
- **Changes**: `src/components/blog/RelatedPosts.astro` (related count: 4→8), `src/components/blog/SinglePost.astro` (+20 cross-link entries: Saham, Bajet Kahwin, Internship, Slaid Pembentangan, Bisnes Online, Bursa Malaysia, Gaji Bersih, SST, e-Tunai, Kerja Remote, Gaji RM1,800, PTPTN, Tabung Haji, Pajak Gadai Emas, Rule 78, Quishing, Ringgit, Deposit Scam, Insurans Hayat, Takaful)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅; git status clean ✅
- **Duplicate/Orphaned Image Detection**: No new images in this commit ✅
- **Build**: 507 pages built successfully (14.28s) — clean rebuild ✅ (up from 503 pages — more content from earlier commits)
- **Content Verification** (curl on port 3000, Python http.server serving from dist/):
  - Related posts verified: 8 related post cards rendering on blog posts (up from 4) ✅
  - Cross-links verified: 21+ internal links in article body including cross-link keywords ✅
  - Schema.org JSON-LD (BlogPosting) renders correctly on blog posts ✅
  - Homepage: "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - Blog post page with new cross-links: "Cara Beli Saham USA Guna Moomoo Malaysia 2026" ✅
- **Status**: resolved

## 2026-06-12 19:57
- **QA Check**: Full build + curl verification — SinglePost.astro schema markup (BlogPosting JSON-LD) + content upgrade + internal linking expansion
- **Commit**: `7946e90` — Phase 1: Schema markup + content upgrade + internal linking
- **Changes**: `src/components/blog/SinglePost.astro` (+60 lines — added BlogPosting schema.org JSON-LD with `datePublished`, `dateModified`, `author` (Person), `publisher` (Organization with logo), `image` (ImageObject), `mainEntityOfPage` (WebPage); expanded crossLinks from 8→12 MAX_LINKS with 11 new entries: DCA, i-Saraan, Scam, Side Hustle, Kerjaya, Subsidi, Dividen, STR, Robo-advisor, Freelancer, Beli Rumah; updated existing link URLs); 4 blog posts upgraded with expanded content (Pelaburan Asas, Freelancer KWSP, Bantuan Kerajaan, Scam Pinjaman); `audit_log.md` (restructured)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: No new images in this commit ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (24 public/images/root + src/assets/ orphans + `hero-test-a.jpg`, `hero-test-b.jpg`) — user should `git rm` when convenient
- **Build**: 503 pages built successfully (15.49s) — clean rebuild ✅ (up from 495 pages — 4 upgraded posts now indexed, plus new pages from earlier commits)
- **Content Verification** (curl on port 3000, Node.js static server serving from dist/ with directory→index.html):
  - BlogPosting schema.org JSON-LD present on all blog posts:
    - `@type: "BlogPosting"` with `headline`, `description`, `url`, `datePublished`, `dateModified` ✅
    - `author` as `Person` with correct name ✅
    - `publisher` as `Organization` with `logo` ImageObject ✅
    - `image` as `ImageObject` with correct processed _astro URL ✅
    - `mainEntityOfPage` as `WebPage` with canonical `@id` ✅
  - CrossLinks expanded: MAX_LINKS=12, 19 entries (new: DCA, i-Saraan, Scam, Side Hustle, Kerjaya, Subsidi, Dividen, STR, Robo-advisor, Freelancer, Beli Rumah) ✅
  - All 4 upgraded blog posts verified with correct titles and specific OG images ✅
  - `/pelaburan-asas-asb-kwsp-dca-apa-pilihan-terbaik-untuk-rakyat-malaysia/` — title "Pelaburan Asas Malaysia: ASB, KWSP, DCA – Mana Pilihan Terbaik Untuk Anda 2026? — RakyatHub" ✅
  - OG Image: specific hero image (NOT default fallback) — HTTP 200 ✅
  - `/adakah-freelancer-boleh-carum-kwsp-sendiri/` — title "💼 Adakah Freelancer Boleh Carum KWSP Sendiri? Panduan Lengkap i-Saraan 2026 — RakyatHub" ✅
  - OG Image: specific hero image — HTTP 200 ✅
  - `/info-bantuan-rm100-mykad-subsidi-ron95-kemas-kini-rakyathub/` — title "📉 Bantuan Kerajaan Malaysia 2026 – MyKad, Subsidi RON95 & Inisiatif Sara Hidup — RakyatHub" ✅
  - OG Image: specific hero image — HTTP 200 ✅
  - `/cara-elak-scam-pinjaman-online-panduan-lengkap-tips-selamat/` — title "📘 Cara Elak Scam Pinjaman Online – Panduan Lengkap & Tips Selamat Malaysia 2026 — RakyatHub" ✅
  - OG Image: specific hero image — HTTP 200 ✅
  - `/7-kelebihan-simpanan-asb-pelaburan-bijak-pulangan-konsisten-yang-pasti-korang-tak-tahu/` — BlogPosting schema ✅, crossLinks script with 19 entries ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/category/kwsp/` — "Category 'KWSP' — RakyatHub" ✅
- **Status**: resolved

## 2026-06-12 19:19
- **QA Check**: Full build + CDP verification — SinglePost.astro JSON-LD BlogPosting schema (uncommitted component change)
- **Commit**: `ea0180b` (previously documented at 18:13) — 14 articles upgraded to cron SEO format
- **Uncommitted Change**: `src/components/blog/SinglePost.astro` — added `BlogPosting` JSON-LD structured data schema with `datePublished`, `dateModified`, `author` (Person), `publisher` (Organization with logo), `image` (ImageObject), `mainEntityOfPage` (WebPage) — all using `Astro.props` from post frontmatter
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 495 pages built successfully (13.59s) — clean rebuild ✅
- **Content Verification** (curl on port 3000, zombie Node.js static server serving from dist/):
  - All 14 upgraded articles still render with correct titles ✅ (verified: moomoo, shopee, loan-rumah, saman-jpj, minyak-masak)
  - All OG images return specific hero images (not default fallback) ✅
  - BlogPosting JSON-LD schema renders correctly on blog posts:
    - `@type: "BlogPosting"` with `headline`, `description`, `url`, `datePublished`, `dateModified` ✅
    - `author` as `Person` with correct name ✅
    - `publisher` as `Organization` with `logo` ImageObject ✅
    - `image` as `ImageObject` with correct URL ✅
    - `mainEntityOfPage` as `WebPage` with canonical `@id` ✅
  - Homepage renders: "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/kewangan/` renders: "Category 'Kewangan' — RakyatHub" ✅
- **CDP Inspection** (Chrome CDP on port 9222):
  - DOM: main(1), header/nav(1), footer/contentinfo(1) — all present ✅
  - Console errors: 0 ✅
  - Broken images: 0 ✅
  - Failed resources: 0 (no 4xx/5xx) ✅
  - Blog post page rendered with correct meta, OG tags, and schema ✅
- **Status**: resolved

## 2026-06-12 18:13
- **QA Check**: Content-only build — 14 articles upgraded to cron SEO format (800-1,100 words, DocuKilat calculators, citations)
- **Commit**: `ea0180b` — fix: upgrade 14 thin articles to cron SEO format — 800-1,100 words, DocuKilat, calculators, citations
- **Changes**: 14 `.md` posts updated with expanded content
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅; git status clean ✅
- **Duplicate Image Detection**: No new images in this commit — all article upgrades are content-only ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (4 src/assets/ + 16 public/images/ + public/root files) — user should `git rm` when convenient
- **Build**: 495 pages built successfully (15.22s) — clean rebuild ✅ (up from 403 pages — new articles from earlier commits now indexed)
- **Content Verification** (curl on port 3000, Python http.server serving from dist/):
  - All 14 upgraded pages verified with correct titles and OG images ✅
  - `/7-rahsia-bijak-beli-saham-usa-guna-moomoo-malaysia-panduan-lengkap/` — "Cara Beli Saham USA Guna Moomoo Malaysia 2026" ✅
  - `/adakah-pinjaman-dari-shopee-boleh-dipercayai-panduan-2025/` — "Pinjaman Shopee (SPinjam & SPayLater) 2026" ✅
  - `/beras-import-vs-tempatan-murah/` — "Beras Import vs Tempatan 2026" ✅
  - `/cara-renew-roadtax-jpj-online-2025-panduan-lengkap/` — "Cara Renew Roadtax JPJ Online 2026" ✅
  - `/cara-semak-baki-kwsp-online-tanpa-pergi-kaunter-2025-panduan-lengkap/` — "Cara Semak Baki KWSP Online 2026" ✅
  - `/carawithdrawkwsp/` — "Cara Buat Pengeluaran KWSP 2026" ✅
  - `/cukai-jualan-cukai-perkhidmatan-malaysia-2025-barang-dan-servis-yang-akan-terjejas/` — "SST Malaysia 2026" ✅
  - `/info-terkini-apa-itu-kwsp-akaun-fleksibel-2025-rakyat-kini-boleh-akses-simpanan-bila-bila-masa/` — "KWSP Akaun Fleksibel 2026" ✅
  - `/kereta-sesuai-untuk-fresh-graduate-malaysia-2025-gaji-bajet/` — "Kereta Untuk Fresh Graduate Malaysia 2026" ✅
  - `/loan-rumah-calculator-kiraan-ansuran-perancangan-kewangan/` — "Loan Rumah Calculator 2026" ✅
  - `/minyak-masak-botol-vs-paket-mana-lebih-jimat/` — "Minyak Masak Botol vs Paket" ✅
  - `/risiko-dan-pulangan-robo-advisor-di-malaysia-2025/` — "Robo-Advisor di Malaysia 2026" ✅
  - `/semakan-saman-jpj-pdrm/` — "Cara Semak Saman JPJ & PDRM Online 2026" ✅
  - `/tebus-bantuan-sara-rm100-guna-ic-pengumuman-pagi-ini-23-julai-2025/` — "Tebus Bantuan SARA RM100 Guna MyKad 2026" ✅
  - All OG images return HTTP 200 (specific hero images, not default fallback) ✅
  - Frontmatter image references active (not commented out) ✅
  - Homepage renders: "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-12 17:19
- **QA Check**: Content-only build — 1 new article (Beli vs Beli: Minyak Masak Botol vs Paket)
- **Commit**: `43178de` — Beli vs Beli: Minyak Masak Botol vs Paket
- **Changes**: `src/data/post/minyak-masak-botol-vs-paket-mana-lebih-jimat.md` (new post — 71 lines, cooking oil bottle vs packet cost comparison); `src/assets/images/hero-beli-minyak-masak.jpg` (new hero image, 442KB — hash `7c2ec2e`, unique ✅); `audit_log.md` (updated)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `7c2ec2e46b95164fe46f7389c7fbd2e76d573060` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (29 orphans across public/images/, public/, and src/assets/) — user should `git rm` when convenient
- **Build**: 403 pages built successfully (12.55s) — clean rebuild ✅
- **Content Verification** (curl on port 3000, Node.js static server serving from dist/ with directory→index.html):
  - `/minyak-masak-botol-vs-paket-mana-lebih-jimat/` — title "Minyak Masak Botol vs Paket — Mana Lagi Berbaloi Untuk Dompet Korang? — RakyatHub" ✅
  - OG Image: `/_astro/hero-beli-minyak-masak.C0xYCXpl_IcIFe.jpg` — HTTP 200, 21,298 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-beli-minyak-masak.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-12 16:41
- **QA Check**: Content-only build — 1 new article (Ringgit RM4.07 - impak belanja anak muda)
- **Commit**: `1b06714` — News React: Ringgit RM4.07 - impak belanja anak muda
- **Changes**: `src/data/post/ringgit-melemah-impak-belanja-anak-muda.md` (new post — 112 lines, Ringgit jatuh ke RM4.07/USD impak pada gaji RM3,000, shopping online dan minyak); `src/assets/images/hero-ringgit-melemah-impak-belanja-anak-muda.jpg` (new hero image, 210KB — hash `c199e40`, unique ✅); `audit_log.md` (updated)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `c199e4093234415ffb3c2989bca0cbab0931fd29` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (29 orphans across public/images/, public/, and src/assets/) — user should `git rm` when convenient
- **Build**: 400 pages built successfully (16.47s) — clean rebuild ✅
- **Content Verification** (curl on port 3000, Node.js static server serving from dist/ with directory→index.html):
  - `/ringgit-melemah-impak-belanja-anak-muda/` — title "Ringgit Jatuh RM4.07 — Gaji RM3,000 Kena Pukul? — RakyatHub" ✅
  - OG Image: `/_astro/hero-ringgit-melemah-impak-belanja-anak-muda.BWUXOkeT_2e5jxR.jpg` — HTTP 200, 145,541 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-ringgit-melemah-impak-belanja-anak-muda.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-12 14:19
- **QA Check**: Content-only build — 1 new article (Takaful vs Insurans Hayat)
- **Commit**: `f19496a` — Auto: Insurans - Takaful vs Insurans Hayat — Mana Pilihan Terbaik untuk Perlindungan Anda?
- **Changes**: `src/data/post/takaful-vs-insurans-hayat-mana-pilihan-terbaik-perlindungan-anda.md` (new post — 185 lines, comprehensive comparison of Takaful vs conventional life insurance for Muslims); `src/assets/images/hero-takaful-vs-insurans.jpg` (new hero image, 84KB — hash `da01976`, unique ✅); `audit_log.md` (trimmed/consolidated — 512 lines changed)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `da0197639e4042511e2d8d3f4b2ecabc3c1ad621` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (20 public/images/ + 4 public/ + `hero-saham-usa.jpg` + `cta-join-discord.png` + `hero-test-a.jpg`, `hero-test-b.jpg`) — user should `git rm` when convenient
- **Build**: 396 pages built successfully (12.20s) — clean rebuild ✅
- **Content Verification** (curl on port 3400, Node.js static server serving from dist/ with directory→index.html):
  - `/takaful-vs-insurans-hayat-mana-pilihan-terbaik-perlindungan-anda/` — title "Takaful vs Insurans Hayat — Mana Pilihan Terbaik untuk Perlindungan Anda? — RakyatHub" ✅
  - OG Image: `/_astro/hero-takaful-vs-insurans.PhqnwOL4_1m7P8y.jpg` — HTTP 200, 56,789 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-takaful-vs-insurans.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/insurans/` — "Category 'Insurans' — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-12 12:56
- **QA Check**: Content-only build — 2 new Student articles (Cara Hias Bilik Asrama Aesthetic + Cara Hilangkan Mengantuk Masa Belajar)
- **Commit**: `d6ec37c` — Auto [Student]: Cara hias bilik asrama aesthetic + Cara hilangkan mengantuk masa belajar
- **Changes**: `src/data/post/cara-hias-bilik-asrama-aesthetic.md` (new post — 154 lines, 10 aesthetic dorm decoration ideas under RM50 budget); `src/data/post/cara-hilangkan-mengantuk-masa-belajar.md` (new post — 149 lines, 8 tips to fight sleepiness while studying); `src/assets/images/hero-cara-hias-bilik-asrama-aesthetic.jpg` (new hero image, 327KB — hash `24d454c`, unique ✅); `src/assets/images/hero-cara-hilangkan-mengantuk-masa-belajar.jpg` (new hero image, 245KB — hash `bee2f92`, unique ✅); `topic_tracker_student.md` (updated)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: Both new images have unique hashes — no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior runs (20 public/images/ + 4 public/ + `hero-saham-usa.jpg` + `cta-join-discord.png` + `hero-test-a.jpg`, `hero-test-b.jpg`) — user should `git rm` when convenient
- **Build**: 392 pages built successfully (17.52s) — clean rebuild ✅
- **Content Verification** (curl on port 3000, Python http.server serving from dist/):
  - `/cara-hias-bilik-asrama-aesthetic/` — title "Cara Hias Bilik Asrama Aesthetic — 10 Idea Bajet RM50 — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-hias-bilik-asrama-aesthetic.Bhni8Txo_Z2eYHJd.jpg` — HTTP 200 ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-cara-hias-bilik-asrama-aesthetic.jpg"` — active (not commented) ✅
  - `/cara-hilangkan-mengantuk-masa-belajar/` — title "Cara Hilangkan Mengantuk Masa Belajar — 8 Tips Untuk Student — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-hilangkan-mengantuk-masa-belajar.DwygyM1L_Z1uXRJk.jpg` — HTTP 200 ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-cara-hilangkan-mengantuk-masa-belajar.jpg"` — active (not commented) ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-12 10:22
- **QA Check**: Content-only build — new Kerjaya article (Kerja Remote & Hibrid di Malaysia 2026)
- **Commit**: `fc3d92e` — Auto: Kerjaya - Kerja Remote & Hibrid di Malaysia 2026 — Panduan Lengkap Gaji, Platform & Tips Dapat Kerja
- **Changes**: `src/data/post/kerja-remote-hibrid-malaysia-2026.md` (new post — 217 lines, complete guide to remote/hybrid work in Malaysia 2026 with salary comparison tables, platform recommendations, required skills, and practical tips); `src/assets/images/hero-kerja-remote-hibrid-malaysia-2026.jpg` (new hero image, 141KB — hash `f0bc816`, unique ✅)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `f0bc8165077aec847079cfc95dc7aae59a69eeab` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 26 pre-existing orphans unchanged from prior runs (20 public/images/ + 4 public/ + 2 src/assets/) — user should `git rm` when convenient
- **Build**: 389 pages built successfully (10.96s) — clean rebuild ✅
- **Content Verification** (curl on port 3300, Node.js static server with directory→index.html):
  - `/kerja-remote-hibrid-malaysia-2026/` — title "Kerja Remote & Hibrid di Malaysia 2026 — Panduan Lengkap Gaji, Platform & Tips Dapat Kerja — RakyatHub" ✅
  - OG Image: `/_astro/hero-kerja-remote-hibrid-malaysia-2026.B9yDBfRp_Z1Ws9ru.jpg` — HTTP 200, 92,704 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-kerja-remote-hibrid-malaysia-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kerjaya/` — "Category 'Kerjaya' — RakyatHub" ✅ (new post slug present in category page)
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-11 20:25
- **QA Check**: Content-only build — new Side Hustle article (7 Side Hustle Paling Laku di Malaysia 2026)
- **Commit**: `bdb31cb` — Auto: Side Hustle - 7 Side Hustle Paling Laku di Malaysia 2026
- **Changes**: `src/data/post/7-side-hustle-paling-laku-malaysia-2026.md` (new post — 236 lines, 7 side hustles under RM500 capital); `src/assets/images/hero-side-hustle-2026.jpg` (new hero image, 131KB — hash `45a7545`, unique ✅); `audit_log.md` (updated by content pipeline)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `45a754592741ac63f8dc36cf8a106e7bc31e146f` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 26 pre-existing orphans unchanged from prior runs (20 public/images/ + 4 public/ + 2 src/assets/) — user should `git rm` when convenient
- **Build**: 368 pages built successfully (11.65s) — clean rebuild ✅
- **Content Verification** (curl on port 3200, Node.js static server with directory→index.html):
  - `/7-side-hustle-paling-laku-malaysia-2026/` — title "7 Side Hustle Paling Laku di Malaysia 2026 — Modal Bawah RM500, Boleh Start Hari Ni — RakyatHub" ✅
  - OG Image: `/_astro/hero-side-hustle-2026.D9dAXa3c_Ztsclz.jpg` — HTTP 200, 93,453 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-side-hustle-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/tag/side-hustle/` — "Posts by tag 'side-hustle' — RakyatHub" ✅
  - `/tag/jana-pendapatan/` — "Posts by tag 'jana-pendapatan' — RakyatHub" ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-11 18:44
- **QA Check**: Text-only component change — homepage links to countdown gaji (salary countdown) & quiz kewangan (financial health quiz) + increase postsPerPage to 30
- **Commit**: `ce790e0` — fix: increase postsPerPage to 30 + add homepage links to countdown & quiz
- **Changes**: `src/config.yaml` (postsPerPage: 9→30), `src/pages/index.astro` (+10 lines — added 2 new `<a href>` cards to homepage: Countdown Gaji → `/berapa-hari-lagi-nak-gaji/`, Quiz Kewangan → `/quiz-kesihatan-kewangan/`), `.netlify/functions/manifest.json` (timestamp)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Orphaned Image Detection**: 26 pre-existing orphans unchanged from prior runs (20 public/images/ + 4 public/ + 2 src/assets/) — user should `git rm` when convenient
- **Build**: 365 pages built successfully (10.40s) — clean rebuild ✅
- **Content Verification** (curl on port 3100, Node.js static server with directory→index.html):
  - Homepage (`/`): title "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - "Countdown Gaji" link present on homepage (1 occurrence) ✅
  - "Quiz Kewangan" link present on homepage (1 occurrence) ✅
  - `/berapa-hari-lagi-nak-gaji/` — title "Berapa Hari Lagi Nak Gaji? — Countdown Gaji Malaysia 2026 — RakyatHub" ✅
  - `/quiz-kesihatan-kewangan/` — title "Quiz Kesihatan Kewangan — Semak Skor Kewangan Anda — RakyatHub" ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
- **Status**: resolved

## 2026-06-11 18:09
- **QA Check**: Full build + CDP pipeline — new interactive pages (countdown gaji, quiz kewangan, upgraded gaji-bersih) + image fix for slaid pembentangan (HEAD shifted mid-pipeline)
- **Commit 1**: `735931b` — feat: add countdown gaji, quiz kewangan, upgrade gaji-bersih + indexing fix
- **Commit 2**: `6a8c6cd` — fix: add image to artikel slaid pembentangan (arrived during build)
- **Changes (Commit 1)**: `src/pages/berapa-hari-lagi-nak-gaji.astro` (new — 242 lines, salary countdown page with WhatsApp/Telegram share), `src/pages/quiz-kesihatan-kewangan.astro` (new — 399 lines, 8-question financial health quiz with score & shareable result), `src/pages/kalkulator/gaji-bersih.astro` (upgraded — +78 lines, B40/M40/T20 categories + Bajet 55/15/20/10), `src/pages/kalkulator/index.astro` (updated — +16 lines, added 2 new calculator pages to index), `public/robots.txt` (updated with Sitemap directive), `.netlify/functions/manifest.json` (timestamp)
- **Changes (Commit 2)**: `src/assets/images/hero-cara-buat-slaid-pembentangan-menarik.jpg` (new — 212KB, unique image for slaid pembentangan article), `src/data/post/cara-buat-slaid-pembentangan-menarik.md` (re-activated `image:` frontmatter — was `# image:` commented out after prior duplicate removal, now points to new unique image ✅)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Build**: 385 pages built successfully (12.61s) — clean rebuild ✅
- **CDP Inspection** (browser via Chrome CDP, serving from dist/ on port 3000):
  - **Countdown Page** (`/berapa-hari-lagi-nak-gaji/`): title "Berapa Hari Lagi Nak Gaji? — Countdown Gaji Malaysia 2026 — RakyatHub" ✅; Countdown timer rendering (10 days, 10 hours, 53 min, 45 sec) ✅; Share buttons (WhatsApp, Telegram, Salin Pautan) ✅; Related tools section ✅; Console errors: 0 ✅
  - **Quiz Page** (`/quiz-kesihatan-kewangan/`): title "Quiz Kesihatan Kewangan — Semak Skor Kewangan Anda — RakyatHub" ✅; 8-question interactive quiz with radio buttons and navigation ✅; Quiz advances correctly (answered all 8 questions) ✅; Results screen renders with score, grade breakdown, recommendations, share buttons ✅; Console errors: 0 ✅
  - **Gaji Bersih Calculator** (`/kalkulator/gaji-bersih/`): title "Kalkulator Gaji Bersih Malaysia — Kira Gaji Selepas KWSP, SOCSO, PCB — RakyatHub" ✅; Gaji Pokok RM3,500 → Gaji Bersih RM2,906.00 ✅; KWSP 11% = RM385, SOCSO = RM115, EIS = RM24, PCB = RM70 ✅; B40/M40/T20 Kategori Pendapatan section ✅; Bajet 55/15/20/10 breakdown (RM1,598/RM436/RM581/RM291) ✅; Console errors: 0 ✅
  - **Calculator Index** (`/kalkulator/`): title "Kalkulator RakyatHub — Alat Kewangan Malaysia — RakyatHub" ✅
- **Content Asset Verification**:
  - **Slaid Pembentangan article** (`/cara-buat-slaid-pembentangan-menarik/`): title "Cara Buat Slaid Pembentangan Menarik — 7 Tips Design Untuk Student — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-buat-slaid-pembentangan-menarik.CUV0rXFb_1BYDG6.jpg` — HTTP 200, 182,156 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-cara-buat-slaid-pembentangan-menarik.jpg"` — active (not commented) ✅ (re-activated after prior duplicate removal — this is a fresh unique image from the content pipeline self-correction)
  - robots.txt: `Sitemap: https://rakyathub.my/sitemap-index.xml` directive present ✅
- **HEAD shift noted**: Initial HEAD `735931b` (new interactive pages). During build, HEAD shifted to `6a8c6cd` (image fix). Build output captured both commits. Combined entry written.
- **Status**: resolved

## 2026-06-11 16:22
- **QA Check**: Content-only build — new News React article (Harga Minyak Kekal 11-17 Jun 2026)
- **Commit**: `70cdecb` — Auto: News React - Harga Minyak Kekal 11-17 Jun 2026
- **Changes**: `src/data/post/harga-minyak-kekal-jun-2026.md` (new post — 108 lines, fuel price freeze news for 11-17 Jun 2026), `src/assets/images/hero-harga-minyak-kekal-jun-2026.jpg` (new hero image, 72KB — unique hash `c311712` ✅), `audit_log.md` (updated by content pipeline)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `c3117121a176f2b8b9f25467ed33fcff2cd6c630` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 26 pre-existing orphans (20 public/images/ + 4 public/ + `hero-saham-usa.jpg` + `cta-join-discord.png` + `hero-test-a.jpg`, `hero-test-b.jpg`) — unchanged from prior runs, user should `git rm` when convenient
- **Build**: 383 pages built successfully (10.19s) — incremental build, reused cache for 280 images ✅
- **Content Verification** (curl on port 3002, Python http.server serving from dist/):
  - `/harga-minyak-kekal-jun-2026/` — title "Harga Minyak Kekal Minggu Ini — Apa Maksudnya Untuk Korang? — RakyatHub" ✅
  - OG Image: `/_astro/hero-harga-minyak-kekal-jun-2026.Db_zKS2u_1CDIgr.jpg` — HTTP 200, 45,578 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-harga-minyak-kekal-jun-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/blog/` — "Blog — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-11 15:45
- **QA Check**: Content-only build — new Glossary article (Dividen)
- **Commit**: `8a5d922` — Glossary: Dividen
- **Changes**: `src/data/post/glossary-dividen.md` (new post — 140 lines, simple dividend definition guide covering ASB/KWSP dividends, compounding, and savings tips), `src/assets/images/hero-glossary-dividen.jpg` (new hero image, ~1MB — unique hash `311ebd9` ✅)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `311ebd9dabb81ccd7e701bfc4810492e9f910bbc` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 26 pre-existing orphans (20 public/images/ + 4 public/ + `hero-saham-usa.jpg` + `cta-join-discord.png`) + `hero-test-a.jpg`, `hero-test-b.jpg` (test artifacts) — unchanged from prior runs, user should `git rm` when convenient
- **Build**: 382 pages built successfully (10.89s) — clean rebuild ✅
- **Content Verification** (curl on port 3001, Python http.server serving from dist/):
  - `/glossary-dividen/` — title "Glossary: Apa Itu Dividen? Maksud Mudah & Contoh Untuk Korang — RakyatHub" ✅
  - OG Image: `/_astro/hero-glossary-dividen.DNY4o7FV_Z2hqW90.jpg` — HTTP 200, 54,101 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-glossary-dividen.jpg"` — active (not commented) ✅
  - `/category/kewangan/` — includes new post reference (2 occurrences found) ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- **Status**: resolved

## 2026-06-11 14:57
- **QA Check**: Content-only build — 3 new articles (Insurans, Aplikasi Belajar, Cara Buat Slaid), duplicate image detected & fixed
- **Commit 1**: `24696aa` — Auto: Insurans - Pelan Perlindungan Ikut Tahap Umur
- **Commit 2**: `bb9f906` — fix(qa): Remove duplicate image hero-cara-buat-slaid-pembentangan-menarik.jpg (identical to hero-contoh-pengenalan-kerja-kursus.jpg)
- **Changes (Commit 1)**: `src/data/post/pelan-perlindungan-ikut-tahap-umur-insurans-takaful.md` (new post — 197 lines, comprehensive insurance guide by age group), `src/data/post/aplikasi-belajar-untuk-student.md` (new post — 158 lines, 10 digital tools for students), `src/data/post/cara-buat-slaid-pembentangan-menarik.md` (new post — 146 lines, 7 presentation design tips); `src/assets/images/hero-perlindungan-ikut-umur.jpg` (new hero image, 561KB — hash `678867a` — unique ✅), `src/assets/images/hero-aplikasi-belajar-untuk-student.jpg` (new hero image, 209KB — hash `7efd43c` — unique ✅), `src/assets/images/hero-cara-buat-slaid-pembentangan-menarik.jpg` (new hero image, 362KB — ⚠️ DUPLICATE of hero-contoh-pengenalan-kerja-kursus.jpg), `src/assets/images/hero-test-a.jpg`, `src/assets/images/hero-test-b.jpg` (test artifacts, unreferenced)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**:
  - `hero-cara-buat-slaid-pembentangan-menarik.jpg` (hash `5e625a4`) — ⚠️ **DUPLICATE of `hero-contoh-pengenalan-kerja-kursus.jpg`** (identical content, same git hash). First occurrence (no prior removal history for this filename).
  - All other new images unique ✅
- **Fix Applied**:
  - `git rm src/assets/images/hero-cara-buat-slaid-pembentangan-menarik.jpg` — removed duplicate file from git and working tree
  - Commented out `image:` line in `cara-buat-slaid-pembentangan-menarik.md` frontmatter — post falls back to default OG image
  - Committed as `bb9f906`
- **Orphaned Image Detection**: 27 pre-existing orphans unchanged from prior runs — plus `hero-test-a.jpg`, `hero-test-b.jpg` (test artifacts, unreferenced — user should `git rm` when convenient)
- **Build**: 378 pages built successfully (12.30s) — clean rebuild ✅
- **Content Verification** (curl on port 3000, Node.js static server with directory→index.html):
  - `/pelan-perlindungan-ikut-tahap-umur-insurans-takaful/` — title "Pelan Perlindungan Ikut Tahap Umur — Insurans & Takaful Apa Yang Korang Perlukan Dari 20-an Hingga 50-an? — RakyatHub" ✅
  - OG Image: `/_astro/hero-perlindungan-ikut-umur.btXE_CK7_2ctJ2D.jpg` — HTTP 200, 113,036 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-perlindungan-ikut-umur.jpg"` — active (not commented) ✅
  - `/aplikasi-belajar-untuk-student/` — title "Aplikasi Belajar Untuk Student — 10 Tools Digital Terbaik 2026 — RakyatHub" ✅
  - OG Image: `/_astro/hero-aplikasi-belajar-untuk-student.CLR6EqTg_2eU5Dt.jpg` — HTTP 200, 60,339 bytes ✅ (specific hero image)
  - Frontmatter image line: `image: "~/assets/images/hero-aplikasi-belajar-untuk-student.jpg"` — active (not commented) ✅
  - `/cara-buat-slaid-pembentangan-menarik/` — title "Cara Buat Slaid Pembentangan Menarik — 7 Tips Design Untuk Student — RakyatHub" ✅
  - OG Image: `/_astro/default.BXnHqeYJ_Z1yEx1G.jpg` — falls back to default site image (correct after fix — no duplicate Vite dedup issue) ✅
  - Frontmatter image line: `# image: "..."` — commented out to prevent build failure ✅
  - `/category/insurans/` — "Category 'Insurans' — RakyatHub" ✅
  - `/category/pendidikan/` — "Category 'Pendidikan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-11 10:58
- **QA Check**: Content-only build — restored hero image for Contoh Pengenalan Kerja Kursus (fresh Unsplash ID, previously a duplicate that was removed)
- **Commit**: `9227a0c` — fix: Restore hero image for contoh-pengenalan-kerja-kursus (fresh Unsplash ID)
- **Changes**: `src/assets/images/hero-contoh-pengenalan-kerja-kursus.jpg` (new image, 362KB, hash `5e625a4` — unique, NOT a duplicate of any tracked image ✅); `src/data/post/contoh-pengenalan-kerja-kursus.md` (re-activated `image:` frontmatter line — was `# image:` commented out after prior duplicate removal)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `5e625a491804ca359fc6c7dfa5b9d1a38d3698c0` — unique, no duplicates found against any of 268 tracked images ✅
- **Content pipeline self-correction**: The previously-removed duplicate image was replaced by the pipeline with a unique valid file — no intervention needed ✅
- **Frontmatter Cross-Check**: `image:` line is active (not commented) — `image: "~/assets/images/hero-contoh-pengenalan-kerja-kursus.jpg"` ✅
- **Orphaned Image Detection**: 25 pre-existing orphans unchanged from prior runs (24 public/root + `src/assets/images/hero-saham-usa.jpg`) — user should `git rm` when convenient
- **Build**: 370 pages built successfully (8.85s) — clean rebuild ✅
- **Content Verification** (cat from dist/):
  - `/contoh-pengenalan-kerja-kursus/` — title "Contoh Pengenalan Kerja Kursus Yang Menarik & Tepat — RakyatHub" ✅
  - OG Image: `/_astro/hero-contoh-pengenalan-kerja-kursus.B9bfA-1r_Z4P9D5.jpg` — specific hero image, NOT default fallback ✅
  - Rendered hero image: `<img src="/_astro/hero-contoh-pengenalan-kerja-kursus.B9bfA-1r_2924gX.webp"` with srcset variants and WebP/JPEG formats ✅
  - Schema.org JSON-LD image: correct filename ✅
- **Status**: resolved

## 2026-06-11 10:46
- **QA Check**: Content-only build — 2 new Student articles (Contoh Pengenalan Kerja Kursus + Tips Skor Pointer 4.0), duplicate image detected & fixed
- **Commit 1**: `db9496e` — Auto [Student]: Contoh pengenalan kerja kursus + Tips skor pointer 4.0 universiti
- **Commit 2**: `502c7d9` — fix(qa): Remove duplicate image hero-contoh-pengenalan-kerja-kursus.jpg (identical to hero-idea-bisnes-modal-kecil-untuk-student.jpg)
- **Changes (Commit 1)**: `src/data/post/contoh-pengenalan-kerja-kursus.md` (new post — 112 lines, contoh pengenalan kerja kursus guide with 3 examples), `src/data/post/tips-skor-pointer-40-universiti.md` (new post — 164 lines, 10 strategies for pointer 4.0), `src/assets/images/hero-contoh-pengenalan-kerja-kursus.jpg` (new hero image, 350KB — ⚠️ DUPLICATE of hero-idea-bisnes-modal-kecil-untuk-student.jpg), `src/assets/images/hero-tips-skor-pointer-40-universiti.jpg` (new hero image, 216KB — hash `7cda783` — unique ✅), `topic_tracker_student.md` (updated — 2 topics marked ✅)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: 
  - `hero-contoh-pengenalan-kerja-kursus.jpg` (hash `6f45087`) — ⚠️ **DUPLICATE of `hero-idea-bisnes-modal-kecil-untuk-student.jpg`** (identical content, same git hash). First occurrence (no prior removal history for this filename).
  - `hero-tips-skor-pointer-40-universiti.jpg` (hash `7cda783`) — unique ✅
- **Fix Applied**:
  - `git rm src/assets/images/hero-contoh-pengenalan-kerja-kursus.jpg` — removed duplicate file from git and working tree
  - Commented out `image:` line in `contoh-pengenalan-kerja-kursus.md` frontmatter — post falls back to default OG image
  - Committed as `502c7d9`
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 370 pages built successfully (9.23s) — clean rebuild after duplicate removal ✅
- **Content Verification** (curl on port 5505, Node.js static server with directory→index.html):
  - `/contoh-pengenalan-kerja-kursus/` — title "Contoh Pengenalan Kerja Kursus Yang Menarik & Tepat — RakyatHub" ✅
  - OG Image: `/_astro/default.BXnHqeYJ_Z1yEx1G.jpg` — falls back to default site image (correct after fix — no duplicate Vite dedup issue) ✅
  - Frontmatter image line: `# image: "~/assets/images/hero-contoh-pengenalan-kerja-kursus.jpg" — REMOVED (duplicate of hero-idea-bisnes-modal-kecil-untuk-student.jpg)` — commented out to prevent build failure ✅
  - `/tips-skor-pointer-40-universiti/` — title "Tips Skor Pointer 4.0 Universiti — 10 Strategi Terbukti — RakyatHub" ✅
  - OG Image: `/_astro/hero-tips-skor-pointer-40-universiti.CwdyX605_Z2aRXvg.jpg` — HTTP 200, 70,868 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-tips-skor-pointer-40-universiti.jpg"` — active (not commented) ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/pendidikan/` — "Category 'Pendidikan' — RakyatHub" ✅
  - `/tag/kerja-kursus/` — "Posts by tag 'kerja-kursus' — RakyatHub" ✅
  - `/tag/pointer-40/` — "Posts by tag 'pointer-40' — RakyatHub" ✅
- **Status**: resolved

## 2026-06-11 10:23
- **QA Check**: Content-only build — new Kerjaya article (7 Pekerjaan Paling Laris 2026 di Malaysia)
- **Commit**: `5bd2a1a` — Auto: Kerjaya - 7 Pekerjaan Paling Laris 2026 di Malaysia
- **Changes**: `src/data/post/7-pekerjaan-paling-laris-2026-malaysia.md` (new post — 308 lines, comprehensive guide to 2026 job market in Malaysia), `src/assets/images/hero-7-pekerjaan-paling-laris-2026-malaysia.jpg` (new hero image, 274KB, hash `09a9d8c` — unique ✅), `audit_log.md` (updated by prior commit)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `09a9d8cab20fd46c4e758eb15c1fb95db6401121` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 362 pages built successfully (9.23s) — clean rebuild ✅
- **Content Verification** (curl on port 5504, Python http.server serving from dist/):
  - `/7-pekerjaan-paling-laris-2026-malaysia/` — title "7 Pekerjaan Paling Laris 2026 di Malaysia — Gaji Terkini, Kemahiran Wajib & Tips Mohon — RakyatHub" ✅
  - OG Image: `/_astro/hero-7-pekerjaan-paling-laris-2026-malaysia.BsnXh6Dy_1C1V7L.jpg` — HTTP 200, 96,711 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-7-pekerjaan-paling-laris-2026-malaysia.jpg"` — active (not commented) ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/kerjaya/` — "Category 'Kerjaya' — RakyatHub" ✅
  - `/category/kewangan/2/` — "Category 'Kewangan' — Page 2 — RakyatHub" ✅
  - `/rss.xml` — HTTP 200 ✅
- **Status**: resolved

## 2026-06-11 08:26
- **QA Check**: Content-only build — 4 new articles (PR1MA, Saham Bursa Malaysia, PRS, Tabung Haji)
- **Commit**: `ee36b1d` — Auto: 4 new articles — PRS skim persaraan, PR1MA 2026, cara melabur saham Bursa Malaysia, Tabung Haji panduan
- **Changes**: `src/data/post/cara-mohon-rumah-pr1ma-2026-syarat-kelayakan.md` (new post — 194 lines), `src/data/post/cara-mula-melabur-saham-bursa-malaysia-panduan-pemula-2026.md` (new post — 207 lines), `src/data/post/prs-skim-persaraan-swasta-panduan-lengkap-2026.md` (new post — 176 lines), `src/data/post/tabung-haji-2026-panduan-simpanan-dividen.md` (new post — 207 lines); `src/assets/images/hero-melabur-saham-bursa.jpg` (new — 74KB, hash `2fc373b3` — unique ✅), `src/assets/images/hero-mohon-rumah-pr1ma.jpg` (new — 128KB, hash `b989414a` — unique ✅), `src/assets/images/hero-prs-retirement.jpg` (new — 126KB, hash `4fa00a2e` — unique ✅), `src/assets/images/hero-tabung-haji.jpg` (updated — 124KB, hash `01e381d2` — unique ✅)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: All 3 new + 1 modified images have unique hashes — no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **HEAD shift noted**: Initial HEAD was `0308603` (already documented, early-exit fired). During processing, HEAD shifted to `ee36b1d` (this commit). New commit processed fresh.
- **Build**: 357 pages built successfully (10.17s) — clean rebuild ✅
- **Content Verification** (curl on port 6001, Node.js static server with directory→index.html):
  - `/cara-mohon-rumah-pr1ma-2026-syarat-kelayakan/` — title "PR1MA 2026 — Cara Mohon Rumah Mampu Milik & Syarat Kelayakan — RakyatHub" ✅
  - OG Image: `/_astro/hero-mohon-rumah-pr1ma.BPTPE1MJ_Z1RfDav.jpg` — HTTP 200, 95,396 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-mohon-rumah-pr1ma.jpg"` — active (not commented) ✅
  - `/cara-mula-melabur-saham-bursa-malaysia-panduan-pemula-2026/` — title "Cara Mula Melabur Saham Bursa Malaysia — Panduan Pemula 2026 — RakyatHub" ✅
  - OG Image: `/_astro/hero-melabur-saham-bursa.CvCGxwek_hPGjB.jpg` — HTTP 200, 52,150 bytes ✅ (specific hero image)
  - Frontmatter image line: `image: "~/assets/images/hero-melabur-saham-bursa.jpg"` — active (not commented) ✅
  - `/prs-skim-persaraan-swasta-panduan-lengkap-2026/` — title "PRS 2026 — Skim Persaraan Swasta Untuk Tambah Simpanan Pencen — RakyatHub" ✅
  - OG Image: `/_astro/hero-prs-retirement.C3aTJVI4_1OcC9g.jpg` — HTTP 200, 91,167 bytes ✅ (specific hero image)
  - Frontmatter image line: `image: "~/assets/images/hero-prs-retirement.jpg"` — active (not commented) ✅
  - `/tabung-haji-2026-panduan-simpanan-dividen/` — title "Tabung Haji 2026 — Cara Simpan, Dividen & Panduan Lengkap — RakyatHub" ✅
  - OG Image: `/_astro/hero-tabung-haji.BfGWcRZ4_2tvT2X.jpg` — HTTP 200, 81,293 bytes ✅ (specific hero image, updated file)
  - Frontmatter image line: `image: "~/assets/images/hero-tabung-haji.jpg"` — active (not commented) ✅
- **Broader Verification** (curl):
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/kerajaan/` — "Category 'Kerajaan' — RakyatHub" ✅
  - `/category/pelaburan/` — "Category 'Pelaburan' — RakyatHub" ✅
  - `/side-hustle-content-creator-ugc-malaysia-2026/` — existing post still renders ✅
  - `/category/kewangan/2/` — pagination still works ✅
- **Status**: resolved

## 2026-06-10 20:13
- **QA Check**: Content-only build — new Side Hustle UGC article (content creator side hustle guide)
- **Commit**: `0308603` — Auto: Side Hustle - Content Creator & UGC Artikel Baru
- **Changes**: `src/data/post/side-hustle-content-creator-ugc-malaysia-2026.md` (new post — 230 lines, complete UGC side hustle guide), `src/assets/images/hero-content-creator-ugc-2026.jpg` (new hero image, 29KB — unique hash ✅), `src/data/post/cara-tonton-piala-dunia-2026-malaysia.md` (deleted — old World Cup .md post, now superseded by .astro page)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `da84c16ea668ee5b617d26e4f86c7dc2f447d5e4` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 347 pages built successfully (8.21s) — clean rebuild ✅
- **Content Verification** (curl on port 5503, Node.js static server with directory→index.html):
  - `/side-hustle-content-creator-ugc-malaysia-2026/` — title "Side Hustle Content Creator & UGC — Jana RM3,000 Sebulan Guna Telefon — RakyatHub" ✅
  - OG Image: `/_astro/hero-content-creator-ugc-2026.CFjzfXkf_Za8lTY.jpg` — HTTP 200, 18,883 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-content-creator-ugc-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - Deleted post page `/cara-tonton-piala-dunia-2026-malaysia/` — HTTP 200 (still exists as .astro page) ✅
- **Status**: resolved

## 2026-06-10 17:47
- **QA Check**: Full build pipeline — rebrand Piala Dunia → Pesta Bola to avoid copyright triggers
- **Commit**: `24ba08a` — fix: remove trademarked terms (Piala Dunia → Pesta Bola) to avoid copyright triggers
- **Changes**: `src/pages/cara-tonton-piala-dunia-2026-malaysia/index.astro` — replaced all "Piala Dunia" references with "Pesta Bola", updated metadata (title, description), removed trademarked section labels and comment blocks, consolidated CSS, updated stats labels (Pasukan → Pasukan Bertanding), updated FAQ answers (streaming bola → streaming sukan), replaced comparison table references to competitors
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Build**: 342 pages built successfully (9.25s) — clean rebuild ✅
- **Content Verification** (curl on port 4005, Node.js static server with directory→index.html):
  - Page title: "Pesta Bola 2026 — Streaming HD & Komuniti Online Malaysia — RakyatHub" ✅
  - OG Title: "Pesta Bola 2026 — Streaming HD & Komuniti Online Malaysia" ✅
  - "Piala Dunia" occurrences: 0 (all trademarked terms removed) ✅
  - New content verified: "Pesta Bola", "Kejohanan Terbesar 2026", "streaming sukan" all present ✅
  - CTA banner image `/images/cta-klik-diskon.jpg` — HTTP 200, 108,294 bytes ✅
- **Broader Verification** (curl):
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
- **Status**: resolved

## 2026-06-10 17:36
- **QA Check**: Full CDP pipeline — Convert World Cup article to premium Shopee landing page
- **Commit**: `47008c0` — feat: convert World Cup article to premium Shopee landing page — zero Discord, full funnel
- **Changes**: `src/pages/cara-tonton-piala-dunia-2026-malaysia/index.astro` (new custom landing page — 478 lines, full Premium Shopee funnel with hero, stats, features, pricing table, comparison chart, step-by-step guide, testimonials, FAQ, and CTA sections), `src/data/post/cara-tonton-piala-dunia-2026-malaysia.md.bak` (backup of original .md post, 156 lines). Original `.md` post deleted from disk (` D` in git status) — content now rendered as standalone `.astro` page.
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Build**: 342 pages built successfully (9.51s) — page count decreased from 348 as `.md` post replaced by single `.astro` page ✅
- **CDP Inspection** (port 4000, Node.js static server with directory→index.html):
  - Page title: "Pesta Bola 2026 — Streaming HD & Komuniti Online Malaysia — RakyatHub" ✅
  - OG Title: "Pesta Bola 2026 — Streaming HD & Komuniti Online Malaysia" ✅
  - Console errors: 0 ✅
  - Broken images: 0 (2 images — CTA SVG icon, CTA banner) ✅
  - Resource errors: 0 (no 4xx/5xx on any 127.0.0.1 resource) ✅
  - DOM structure: Banner (header/nav) ✅, Main content section with all sections ✅, Footer (contentinfo) ✅
  - Page sections verified: Hero (stats: 48, 104+, 3, RM20), Features (1080p HD, RM20, Voice & Chat, Trusted Seller), Pricing (Free Trial RM0/Full Access RM20/Komuniti), Comparison table, Steps (Beli di Shopee → Contact Admin → Tonton & Sorak), Testimonials (3 cards), FAQ (6 items), Final CTA ✅
  - CTA banner image `/images/cta-klik-diskon.jpg` — HTTP 200, 108,294 bytes ✅
- **Broader Verification** (curl):
  - `/` — "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
- **Status**: resolved

## 2026-06-10 16:24
- **QA Check**: Content-only build — new news article (PM Anwar Tolak Naikkan Harga Minyak, RON95 Kekal RM1.99)
- **Commit**: `92f1bb8` — Auto: News React — PM Anwar Tolak Naikkan Harga Minyak, RON95 Kekal RM1.99
- **Changes**: `src/assets/images/hero-pm-tolak-naikkan-harga-minyak.jpg` (new hero image, 247KB — hash `d63bd54`), `src/data/post/pm-tolak-naikkan-harga-minyak.md` (new post — 119 lines, PM Anwar's decision to maintain RON95 at RM1.99)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `d63bd54895ed26897571b9c3387da56d5f41d0a2` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 348 pages built successfully (8.36s) — clean rebuild ✅
- **Content Verification** (curl on port 5502, Node.js static server with directory→index.html):
  - `/pm-tolak-naikkan-harga-minyak/` — title "PM Anwar Tolak Naikkan Harga Minyak, RON95 RM1.99 Termurah — RakyatHub" ✅
  - OG Image: `/_astro/hero-pm-tolak-naikkan-harga-minyak.N03fBtGw_Z20W4Bt.jpg` — HTTP 200, 179,543 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-pm-tolak-naikkan-harga-minyak.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - Category page `/category/kewangan/` — includes new post reference ✅
  - Homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-10 14:29
- **QA Check**: Content-only build — content pipeline self-corrected (unique hero image produced for base-mhit article)
- **Commit**: `d3b80f2` — fix: add hero image for Base MHIT article (was commented out)
- **Changes**: `src/assets/images/hero-base-mhit.jpg` (new hero image, 566KB — hash `3fb0c4f` — unique ✅), `src/data/post/base-mhit-plan-insurans-kerajaan-2026.md` (re-activated image frontmatter after prior quarantine — uncommented `image:` line)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `3fb0c4f71ef8289499f42af79ab1cef5406b0e5a` — unique, no duplicates found against any tracked image ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 346 pages built successfully (8.51s) — clean rebuild ✅
- **Content Verification** (curl on port 3050, Node.js static server with directory→index.html):
  - `/base-mhit-plan-insurans-kerajaan-2026/` — title "Pelan Base MHIT 2026 — Insurans Perubatan Mampu Milik RM50 Sebulan, Alternatif Premium Mahal? — RakyatHub" ✅
  - OG Image: `/_astro/hero-base-mhit.C6G1m-h8_Z1lRfpM.jpg` — HTTP 200, 117,695 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-base-mhit.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/insurans/` — "Category 'Insurans' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-10 14:12
- **QA Check**: Content-only build — duplicate image detected & fixed (base-mhit hero identical to hero-str)
- **Commit 1**: `c597333` — Auto: Insurans - Pelan Base MHIT 2026 — Insurans Perubatan Mampu Milik RM50 Sebulan
- **Commit 2**: `60e9bb5` — fix(qa): Remove duplicate image hero-base-mhit.jpg (identical to hero-str.jpg)
- **Changes (Commit 1)**: `src/data/post/base-mhit-plan-insurans-kerajaan-2026.md` (new post — 211 lines, Base MHIT insurance guide), `src/assets/images/hero-base-mhit.jpg` (new hero image, 85KB — ⚠️ DUPLICATE of hero-str.jpg), `src/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` (new hero image, 47KB — unique hash 50571d4 ✅, content pipeline self-corrected from earlier duplicate), `src/data/post/cara-ulangkaji-pelajaran-saat-akhir.md` (re-activated image frontmatter), `.netlify/functions/manifest.json` (timestamp update)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: 
  - `hero-base-mhit.jpg` (hash `5d0bbcf4`) — ⚠️ **DUPLICATE of `hero-str.jpg`** (identical content, 85KB, same git hash). First occurrence (no prior removal history for this filename).
  - `hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` (hash `50571d40`) — unique ✅
- **Fix Applied**: 
  - `git rm src/assets/images/hero-base-mhit.jpg` — removed duplicate file from git and working tree
  - Commented out `image:` line in `base-mhit-plan-insurans-kerajaan-2026.md` frontmatter — post falls back to default OG image
  - Committed as `60e9bb5`
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 346 pages built successfully (11.44s) — clean rebuild ✅
- **Content Verification** (curl on port 5056, Node.js static server with directory→index.html):
  - `/base-mhit-plan-insurans-kerajaan-2026/` — title "Pelan Base MHIT 2026 — Insurans Perubatan Mampu Milik RM50 Sebulan, Alternatif Premium Mahal? — RakyatHub" ✅
  - OG Image: `/_astro/default.BXnHqeYJ_Z1yEx1G.jpg` — falls back to default site image (correct after fix — no duplicate Vite dedup issue) ✅
  - Frontmatter image line: `# image: "~/assets/images/hero-base-mhit.jpg" — REMOVED (duplicate of hero-str.jpg)` — commented out to prevent build failure ✅
  - `/cara-ulangkaji-pelajaran-saat-akhir/` — title "Cara Ulangkaji Pelajaran Saat Akhir — 7 Teknik Power — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-ulangkaji-pelajaran-saat-akhir.B9ipiVQ9_Z1WSd6A.jpg` — HTTP 200, 32,813 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/insurans/` — "Category 'Insurans' — RakyatHub" ✅
  - `/category/pendidikan/` — "Category 'Pendidikan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-10 13:42
- **QA Check**: Content-only scan — content pipeline self-corrected (unique hero image produced for cara-ulangkaji-pelajaran-saat-akhir)
- **Context**: Commit `b59c7ce` (previously documented at 13:21) had removed duplicate image and commented out frontmatter. Between then and now, the content pipeline re-created `hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` as a **unique file** (47KB, hash `50571d40`) — NOT a duplicate of `hero-ptptn.jpg` (hash `8191209`). Frontmatter `image:` line was re-activated.
- **Pre-build**: No untracked `.astro` files ✅; only untracked leftover is the re-created image (unique, not corrupted) ✅; no untracked posts ✅
- **Duplicate Image Detection**: New image hash `50571d40d7cc94847d951f494ebd5e14635a2d73` — unique, no duplicates found against any tracked image ✅
- **Build**: 344 pages built successfully (7.89s) — no cache issues ✅
- **Content Verification** (curl on port 5054, Node.js static server with directory→index.html):
  - `/cara-ulangkaji-pelajaran-saat-akhir/` — title "Cara Ulangkaji Pelajaran Saat Akhir — 7 Teknik Power — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-ulangkaji-pelajaran-saat-akhir.B9ipiVQ9_Z1WSd6A.jpg` — HTTP 200, 32,813 bytes ✅ (specific hero image, NOT default fallback)
  - Frontmatter image line: `image: "~/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/pendidikan/` — "Category 'Pendidikan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Status**: resolved

## 2026-06-10 13:21
- **QA Check**: Content-only build — duplicate image detected & fixed (second occurrence for post cara-ulangkaji-pelajaran-saat-akhir)
- **Commit 1**: `02326b0` — fix: add hero image for cara-ulangkaji-pelajaran-saat-akhir article
- **Commit 2**: `b59c7ce` — fix(qa): Remove duplicate image hero-cara-ulangkaji-pelajaran-saat-akhir.jpg (identical to hero-ptptn.jpg x2)
- **Changes (Commit 1)**: `src/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` (new hero image, 96KB — ⚠️ DUPLICATE of hero-ptptn.jpg x2 — user uploaded same wrong file again), `src/data/post/cara-ulangkaji-pelajaran-saat-akhir.md` (re-activated `image:` frontmatter line after prior quarantine)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: `hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` (hash `8191209`) — ⚠️ **DUPLICATE of `hero-ptptn.jpg`** (identical content — SAME hash as the duplicate removed in commit `5630f84`). User uploaded the same wrong PTPTN image file again instead of a unique hero image for the study tips post.
- **Fix Applied**: 
  - `git rm src/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` — removed duplicate file from git and working tree
  - Commented out `image:` line in `cara-ulangkaji-pelajaran-saat-akhir.md` frontmatter — post falls back to default OG image
  - Committed as `b59c7ce`
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 344 pages built successfully (9.01s) — clean rebuild after fix ✅
- **Content Verification** (curl on port 4004, Node.js static server with directory→index.html):
  - `/cara-ulangkaji-pelajaran-saat-akhir/` — title "Cara Ulangkaji Pelajaran Saat Akhir — 7 Teknik Power — RakyatHub" ✅
  - OG Image: `/_astro/default.BXnHqeYJ_Z1yEx1G.jpg` — falls back to default site image (correct after fix — no duplicate Vite dedup issue) ✅
  - Frontmatter image line: `# image: "~/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg" — REMOVED (duplicate of hero-ptptn.jpg x2)` — commented out to prevent build failure ✅
  - `/category/pendidikan/` — "Category 'Pendidikan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-10 13:03
- **QA Check**: Content-only build — new Gaji RM3,500 breakdown article (Kewangan)
- **Commit**: `42ef7b6` — Gaji x Budget: RM3,500 breakdown
- **Changes**: `src/data/post/gaji-rm3500-breakdown-realistik.md` (new post — 119 lines, Gaji RM3,500 breakdown with 50/30/20 budgeting), `src/assets/images/hero-gaji-rm3500.jpg` (new hero image, 128KB), `audit_log.md` (updated)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅; no untracked dev artifacts ✅
- **Duplicate Image Detection**: `hero-gaji-rm3500.jpg` (hash `67a4cdc`) — unique, no duplicates found ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 344 pages built successfully (8.51s) — clean rebuild ✅
- **Content Verification** (curl on port 5501, Node.js static server with directory→index.html):
  - `/gaji-rm3500-breakdown-realistik/` — title "Gaji RM3,500 Sebulan — Macam Mana Nak Hidup & Jimat Duit? — RakyatHub" ✅
  - OG Image: `/_astro/hero-gaji-rm3500.BLGXP9Id_Z1pUXvO.jpg` — HTTP 200, 87,289 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-gaji-rm3500.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-10 12:18
- **QA Check**: Content-only build — 2 new Student articles + duplicate image detected & fixed
- **Commit 1**: `ba97c52` — Auto [Student]: Cara buat rujukan APA style & Cara ulangkaji pelajaran saat akhir
- **Commit 2**: `5630f84` — fix(qa): Remove duplicate image hero-cara-ulangkaji-pelajaran-saat-akhir.jpg (identical to hero-ptptn.jpg)
- **Commit 3**: `cc318f6` — fix(qa): Comment out image frontmatter for cara-ulangkaji-pelajaran-saat-akhir (duplicate removed)
- **Changes (Commit 1)**: `src/data/post/cara-buat-rujukan-apa-style.md` (new post — 166 lines, APA style guide), `src/data/post/cara-ulangkaji-pelajaran-saat-akhir.md` (new post — 170 lines, last-minute study tips), `src/assets/images/hero-cara-buat-rujukan-apa-style.jpg` (new hero image, 158KB), `src/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` (new hero image, 96KB — ⚠️ DUPLICATE of hero-ptptn.jpg), `topic_tracker_student.md` (2 topics marked ✅)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: 
  - `hero-cara-buat-rujukan-apa-style.jpg` (hash `088f249`) — unique ✅
  - `hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` (hash `8191209`) — ⚠️ **DUPLICATE of `hero-ptptn.jpg`** (same exact content, 96KB, identical hash)
- **Fix Applied**: `git rm src/assets/images/hero-cara-ulangkaji-pelajaran-saat-akhir.jpg` — removed duplicate file. Without this fix, Vite's content-addressable dedup would cause the PTPTN image to silently render on the "Cara Ulangkaji" post, showing wrong visual context.
- **Frontmatter Fix**: Commented out `image:` line in `cara-ulangkaji-pelajaran-saat-akhir.md` — post now gracefully falls back to default OG image (`/_astro/default.BXnHqeYJ_Z1yEx1G.jpg`)
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 341 pages built successfully (46.17s) — clean rebuild ✅
- **Content Verification** (curl on port 5500, Node.js static server with directory→index.html):
  - `/cara-buat-rujukan-apa-style/` — title "Cara Buat Rujukan APA Style — Panduan Lengkap Student — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-buat-rujukan-apa-style.dZCcl2EW_ZodvTw.jpg` — HTTP 200, 108,032 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-cara-buat-rujukan-apa-style.jpg"` — active (not commented) ✅
  - `/cara-ulangkaji-pelajaran-saat-akhir/` — title "Cara Ulangkaji Pelajaran Saat Akhir — 7 Teknik Power — RakyatHub" ✅
  - OG Image: `/_astro/default.BXnHqeYJ_Z1yEx1G.jpg` — falls back to default site image (correct after fix) ✅
  - `/category/pendidikan/` — "Category 'Pendidikan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-10 10:13
- **QA Check**: Content-only build — new Kerjaya article (Industri Paling Prospek)
- **Commit**: `f449fe6` — Auto: Kerjaya - Industri Paling Prospek di Malaysia 2026 — Perbandingan Gaji, Peluang & Prospek Kerjaya
- **Changes**: 1 new `.md` post (`industri-paling-prospek-malaysia-2026.md`), 1 new hero image (`hero-industri-paling-prospek-malaysia-2026.jpg`, 144KB), `.netlify/netlify.toml` (added `/join → Shopee` redirect), `.netlify/functions/manifest.json` (timestamp update)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; git status clean ✅
- **Duplicate Image Detection**: New image hash (`13748061c8e71abfee05a4668e274ef240796754`) is unique — no duplicates found ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: Already built (dist/ included this post as untracked content during prior build for commit `1f28f0a`) — no rebuild needed ✅
- **Content Verification** (curl on port 6000, Node.js static server):
  - `/industri-paling-prospek-malaysia-2026/` — title "Industri Paling Prospek di Malaysia 2026 — Perbandingan Gaji, Peluang & Prospek Kerjaya — RakyatHub" ✅
  - OG Image: `/_astro/hero-industri-paling-prospek-malaysia-2026.Cl3t5hQ1_Z1bnrnJ.jpg` — HTTP 200, 98,399 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-industri-paling-prospek-malaysia-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kerjaya/` — "Category 'Kerjaya' — RakyatHub" ✅
  - `/` — homepage renders with correct OG image ✅
- **Status**: resolved

## 2026-06-10 08:21
- **QA Check**: Content-only build — 4 new articles (Pajak Gadai Emas, Insurans Kereta, Urus Duit Rumah Tangga, Persediaan Ibu Bapa Baru)
- **Commit**: `1f28f0a` — Auto: 4 new articles — Pajak Gadai Emas, Panduan Insurans Kereta, Urus Duit Rumah Tangga, Persediaan Ibu Bapa Baru
- **Changes**: 4 new `.md` posts + 4 new hero images (`hero-pajak-gadai-emas.jpg`, `hero-insurans-kereta.jpg`, `hero-kewangan-pasangan.jpg`, `hero-ibu-bapa-baru.jpg`), `audit_log.md` (updated)
- **Pre-build**: No untracked `.astro` files ✅; no untracked leftover images ✅; no untracked posts ✅
- **Duplicate Image Detection**: All 4 new image hashes unique — no duplicates found ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Build**: 329 pages built successfully (43.49s) — no cache issues ✅
- **Content Verification** (curl on port 5052, Node.js static server):
  - `/pajak-gadai-emas-ar-rahnu-panduan-kira-upah-simpan/` — title "Pajak Gadai Emas Ar-Rahnu — Cara Kira Upah Simpan & Tebus — RakyatHub" ✅
  - OG Image: `/_astro/hero-pajak-gadai-emas.whT4NceO_iC0xd.jpg` — HTTP 200, 138,131 bytes ✅
  - `/panduan-insurans-kereta-malaysia-first-time-owner/` — title "Panduan Insurans Kereta Malaysia — Cara Pilih & Jimat Premium — RakyatHub" ✅
  - OG Image: `/_astro/hero-insurans-kereta.BmJHT25B_LcDHm.jpg` — HTTP 200, 99,831 bytes ✅
  - `/cara-urus-duit-rumah-tangga-pasangan-suami-isteri/` — title "Cara Urus Duit Rumah Tangga — Panduan Kewangan Pasangan — RakyatHub" ✅
  - OG Image: `/_astro/hero-kewangan-pasangan.CGEuLR-i_ZqG98i.jpg` — HTTP 200, 41,885 bytes ✅
  - `/persediaan-kewangan-ibu-bapa-baru-malaysia/` — title "Persediaan Kewangan Ibu Bapa Baru — SSPN, Insurans & Tabung Anak — RakyatHub" ✅
  - OG Image: `/_astro/hero-ibu-bapa-baru.DZS0mQ_z_H7bg2.jpg` — HTTP 200, 54,641 bytes ✅
  - Frontmatter image lines: All 4 `image:` lines active (none commented out) ✅
  - `/category/emas/` — "Category 'Emas' — RakyatHub" ✅
  - `/category/insurans/` — "Category 'Insurans' — RakyatHub" ✅
  - `/` — homepage renders with correct OG image ✅
- **Status**: resolved

## 2026-06-09 20:12
- **QA Check**: Content-only build — Redirect /join → Shopee + New Side Hustle frozen food article (HEAD shifted mid-pipeline)
- **Commit 1**: `b7a908e` — Auto: Redirect /join → Shopee
- **Commit 2**: `50cbcb5` — Auto: Side Hustle - Bisnes Makanan Frozen Dari Rumah 2026 (arrived during build)
- **Changes (Commit 1)**: `public/_redirects` — added `/join  https://s.shopee.com.my/Lkj8tCGZ2  301` redirect; `audit_log.md` — updated
- **Changes (Commit 2)**: `src/data/post/bisnes-makanan-frozen-dari-rumah-2026.md` (new post — Side Hustle frozen food business), `src/assets/images/hero-bisnes-frozen-food-2026.jpg` (new hero image, 928KB)
- **Pre-build**: No untracked `.astro` files ✅; 1 untracked post + image detected as dev artifacts (now committed in Commit 2) — noted
- **Build**: 309 pages built successfully (1m 45s) — no cache issues ✅
- **Content Verification** (curl on port 4000):
  - `/bisnes-makanan-frozen-dari-rumah-2026/` — title "Bisnes Makanan Frozen Dari Rumah — Modal Bawah RM500, Side Hustle 2026 — RakyatHub" ✅
  - OG Image: `/_astro/hero-bisnes-frozen-food-2026.CPjRUKZC_2cwwel.jpg` — HTTP 200, 190,504 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-bisnes-frozen-food-2026.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **_redirects Verification**: File present in `dist/` with correct rules:
  - `/join  https://s.shopee.com.my/Lkj8tCGZ2  301` ✅
  - `/94-2  /panduan-kwsp-malaysia-2025  301` ✅
  - `/sitemap.xml  /sitemap-index.xml  301` ✅
- **Orphaned Images** (noted): 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Status**: resolved

## 2026-06-09 19:07
- **QA Check**: Content-only build — Updated World Cup article — zero Discord, Shopee-only funnel
- **Commit**: `f5a66c2` — Auto: World Cup article — zero Discord, Shopee-only funnel
- **Changes**: `src/data/post/cara-tonton-piala-dunia-2026-malaysia.md` — removed all Discord references (watch party setup, Discord download instructions), removed CTA banner images, simplified Kesimpulan
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Build**: 305 pages built successfully (1m 54s) — no cache issues ✅
- **Content Verification** (curl on port 4000, Node.js static server):
  - `/cara-tonton-piala-dunia-2026-malaysia/` — title "Cara Tonton Piala Dunia 2026 Secara Online di Malaysia — Panduan Lengkap — RakyatHub" ✅
  - OG Image: `/_astro/hero-tonton-piala-dunia-2026.O4eU4ih7_Z1MrBLI.jpg` — HTTP 200, 71,628 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-tonton-piala-dunia-2026.jpg"` — active (not commented) ✅
  - Shopee link rendering: 1 instance of `s.shopee.com.my/Lkj8tCGZ2` present in rendered page ✅
  - `/category/hiburan/` — "Category 'Hiburan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Orphaned Images** (noted): 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Status**: resolved

## 2026-06-09 18:50
- **QA Check**: Content-only build — Updated World Cup article — removed Discord guide, added Shopee funnel (trust signal)
- **Commit**: `f483837` — Auto: Update World Cup article — buang Discord guide, tambah Shopee funnel
- **Changes**: `src/data/post/cara-tonton-piala-dunia-2026-malaysia.md` — replaced 3 rakyathub.my/join CTA links with Shopee affiliate links (`s.shopee.com.my/Lkj8tCGZ2`), removed entire Discord guide section (setup instructions, rewritten Kesimpulan), added Shopee trust signals
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Build**: 305 pages built successfully (1m 43s) — no cache issues ✅
- **Content Verification** (curl on port 4003, Node.js static server):
  - `/cara-tonton-piala-dunia-2026-malaysia/` — title "Cara Tonton Piala Dunia 2026 Secara Online di Malaysia — Panduan Lengkap — RakyatHub" ✅
  - OG Image: `/_astro/hero-tonton-piala-dunia-2026.O4eU4ih7_Z1MrBLI.jpg` — HTTP 200, 71,628 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-tonton-piala-dunia-2026.jpg"` — active (not commented) ✅
  - Shopee link rendering: 3 instances of `s.shopee.com.my/Lkj8tCGZ2` present in rendered page ✅
  - `/category/hiburan/` — "Category 'Hiburan' — RakyatHub" ✅
  - `/` — homepage renders with correct title ✅
- **Orphaned Images** (noted): 24 pre-existing orphans unchanged from prior runs — user should `git rm` when convenient
- **Status**: resolved

## 2026-06-09 18:36
- **QA Check**: Content-only build — Added Shopee affiliate links to World Cup 2026 article (trust signal funnel)
- **Commit**: `af9a796` — Auto: Tambah Shopee link artikel Piala Dunia — trust signal funnel
- **Changes**: `src/data/post/cara-tonton-piala-dunia-2026-malaysia.md` — added Shopee affiliate link (`s.shopee.com.my/Lkj8tCGZ2`) and trust signal funnel copy to the Piala Dunia watch party section
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Build**: 305 pages built successfully (1m 42s) — no cache issues ✅
- **Content Verification** (curl on port 3700, Node.js static server):
  - `/cara-tonton-piala-dunia-2026-malaysia/` — title "Cara Tonton Piala Dunia 2026 Secara Online di Malaysia — Panduan Lengkap — RakyatHub" ✅
  - OG Image: `/_astro/hero-tonton-piala-dunia-2026.O4eU4ih7_Z1MrBLI.jpg` — HTTP 200, 71,628 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-tonton-piala-dunia-2026.jpg"` — active (not commented) ✅
  - Shopee link rendering: "Check Shopee" text and "s.shopee.com.my" URL present in rendered page ✅
  - `/` — homepage renders with correct title ✅
- **Status**: resolved

## 2026-06-09 17:42
- **QA Check**: Full CDP pipeline — Featured Articles section on homepage + new Rule 78 article (HEAD shifted mid-pipeline)
- **Commit 1**: `2a3bb58` — Auto: Featured articles section on homepage for better Google crawl depth
- **Commit 2**: `56d0b71` — Auto: News React — Akta Sewa Beli (Pindaan) 2026, Rule 78 mansuh (arrived mid-inspection)
- **Changes (Commit 1)**: `src/pages/index.astro` — added "Panduan & Tips Popular" grid section with 8 direct links to popular articles (HTML/CSS only, no new JS/onclick handlers)
- **Changes (Commit 2)**: `src/data/post/rule-78-mansuh-akta-sewa-beli-2026.md` (new post), `src/assets/images/hero-rule-78-mansuh-akta-sewa-beli-2026.jpg` (new hero image)
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Build**: 299 pages built successfully (1m 51s) — no cache issues ✅
- **Full CDP Inspection** (port 3600, Node.js static server):
  - DOM: main(1), header(1), nav(1), footer(1) — all present ✅
  - Console: 0 errors, 0 warnings ✅
  - Resource errors: 0 (no 4xx/5xx) ✅
  - Broken images: 0 ✅
  - Failed CSS: 0 ✅
  - onclick handlers: 0 — all links are standard `<a href>` tags, no Astro module scope issues ✅
  - H2 headings: "Alat Kewangan Untuk Rakyat Malaysia", "Panduan & Tips Popular", "Artikel Terkini", "Perlu Surat Rasmi, Invois atau Resume?" — new section rendering ✅
  - Featured Articles section contains 8 links matching git diff:
    - `/cadangan-bajet-50-30-20-di-malaysia/` — "Bajet 50/30/20" ✅
    - `/panduan-kwsp-malaysia-2025/` — "Panduan KWSP" ✅
    - `/cara-beli-emas-public-gold/` — "Beli Emas GAP" ✅
    - `/urus-duit-gaji-bawah-rm3000/` — "Urus Gaji Bawah RM3K" ✅
    - `/panduan-medical-card-malaysia-2026-first-time-buyer/` — "Medical Card 2026" ✅
    - `/gaji-graduan-mengikut-industri-2026/` — "Gaji Graduan 2026" ✅
    - `/panduan-e-filing-cukai-pendapatan-2026/` — "E-Filing 2026" ✅
    - `/gxbank-vs-bigpay-vs-tng-ewallet-dompet-digital-terbaik-2026/` — "eWallet Terbaik 2026" ✅
  - All 8 featured article links verified via curl: HTTP 200 with correct titles ✅
- **Content Asset Verification (Commit 2 — Rule 78 post)**:
  - `/rule-78-mansuh-akta-sewa-beli-2026/` — title "Rule of 78 Tamat! Akta Sewa Beli Baharu Berkuat Kuasa 1 Jun — RakyatHub" ✅
  - OG Image: `/_astro/hero-rule-78-mansuh-akta-sewa-beli-2026.a1NQx1Ok_Z9jgqg.jpg` — HTTP 200, 73,276 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-rule-78-mansuh-akta-sewa-beli-2026.jpg"` — active (not commented) ✅
  - Duplicate Image Detection: New image hash (`d32714de`) is unique — no duplicates found ✅
- **Status**: resolved

## 2026-06-09 14:08
- **QA Check**: Content-only build — new Insurans article (Medical Card vs Critical Illness)
- **Commit**: `7576f97` — Auto: Insurans - Medical Card vs Critical Illness: Apa Beza & Mana Satu Korang Perlukan?
- **Changes**: `src/data/post/medical-card-vs-critical-illness-beza-perlukan.md` (new post), `src/assets/images/hero-medical-vs-critical.jpg` (new hero image), `audit_log.md` (updated)
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Duplicate Image Detection**: New image hash (`13dcd9f`) is unique — no duplicates found ✅
- **Orphaned Image Detection**: 24 pre-existing orphans unchanged from prior run (18 public/images/ + 2 public/ + 2 src/assets/images/ + 2 public/root — not regressed by this commit, user should `git rm` when convenient)
- **Build**: 298 pages built successfully (1m 46s) — no cache issues ✅
- **Content Verification** (curl on port 3505):
  - `/medical-card-vs-critical-illness-beza-perlukan/` — title "Medical Card vs Critical Illness Insurance: Apa Beza & Mana Satu Korang Perlukan? — RakyatHub" ✅
  - OG Image: `/_astro/hero-medical-vs-critical.Bv2xB0Md_adGyc.jpg` — HTTP 200, 63,890 bytes ✅
  - WebP variant: HTTP 200, 8,748 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-medical-vs-critical.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/insurans/` — "Category 'Insurans' — RakyatHub" ✅
  - `/` — homepage renders with correct OG image ✅
- **Status**: resolved

## 2026-06-09 12:31
- **QA Check**: Content-only build — 2 new Student articles (Barang Keperluan Universiti + Cara Cari Internship)
- **Commit**: `9a7a7ef` — Auto [Student]: barang-keperluan-masuk-universiti-checklist + cara-cari-tempat-praktikal-internship
- **Changes**: `src/data/post/barang-keperluan-masuk-universiti-checklist.md` (new post), `src/data/post/cara-cari-tempat-praktikal-internship.md` (new post), `src/assets/images/hero-barang-keperluan-masuk-universiti-checklist.jpg` (new hero image), `src/assets/images/hero-cara-cari-tempat-praktikal-internship.jpg` (new hero image), `topic_tracker_student.md` (updated), `audit_log.md` (updated)
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Duplicate Image Detection**: Both new image hashes (`e1c6015`, `b1c6798`) are unique — no duplicates found ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior run — not regressed by this commit ✅
- **Build**: 296 pages built successfully (1m 46s) — no cache issues ✅
- **Content Verification** (curl on port 3504):
  - `/barang-keperluan-masuk-universiti-checklist/` — title "Barang Keperluan Masuk Universiti — Checklist Lengkap — RakyatHub" ✅
  - OG Image: `/_astro/hero-barang-keperluan-masuk-universiti-checklist.CG1O05ce_2fFXom.jpg` — HTTP 200, 205,489 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-barang-keperluan-masuk-universiti-checklist.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/cara-cari-tempat-praktikal-internship/` — title "Cara Cari Tempat Praktikal / Internship — 6 Langkah — RakyatHub" ✅
  - OG Image: `/_astro/hero-cara-cari-tempat-praktikal-internship.DrhQHDQk_cWGqA.jpg` — HTTP 200, 70,874 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-cara-cari-tempat-praktikal-internship.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
  - `/tag/student/` — "Posts by tag 'student' — RakyatHub" ✅
  - `/tag/internship/` — "Posts by tag 'internship' — RakyatHub" ✅
  - `/` — homepage ✅
- **Status**: resolved

## 2026-06-09 11:14
- **QA Check**: Content-only build — new Scam of The Week article (Facebook deposit scam)
- **Commit**: `998bf04` — Scam of The Week: deposit scam Facebook - Ubai kena RM50
- **Changes**: `src/data/post/scam-deposit-facebook-barang-online.md` (new post), `src/assets/images/hero-scam-facebook-deposit.jpg` (new hero image), `audit_log.md` (restructured)
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Duplicate Image Detection**: New image hash (`49fb844`) — unique, no duplicates found ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior run — not regressed by this commit ✅
- **Build**: 289 pages built successfully (1m 4s) — no cache issues ✅
- **Content Verification** (curl on port 3502):
  - `/scam-deposit-facebook-barang-online/` — title "SCAM ALERT: Deposit RM50 Lesap! Ubai Pun Kena Scam Facebook — RakyatHub" ✅
  - OG Image: `/_astro/hero-scam-facebook-deposit.B2hAvlIC_Z1ylBp5.jpg` — HTTP 200, 68,226 bytes ✅
  - Frontmatter image line: `image: "~/assets/images/hero-scam-facebook-deposit.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/blog/` — lists "Scam Facebook" ✅
  - `/` — homepage renders with correct OG image ✅
- **Status**: resolved

## 2026-06-09 10:28
- **QA Check**: Full build pipeline — new career article + gtagSendEvent fix committed
- **Commit**: `7e3f607` — Auto: Kerjaya - 10 Pekerjaan Paling Tinggi Permintaan di Malaysia 2026
- **Changes**: `src/data/post/pekerjaan-high-demand-malaysia-2026.md` (new post), `src/assets/images/hero-pekerjaan-high-demand-malaysia-2026.jpg` (new hero image), `src/pages/join.astro` (gtagSendEvent module-scope fix from prior QA run now committed), `audit_log.md` (updated)
- **Pre-build**: No untracked leftovers, no untracked posts, no corrupted orphan images ✅
- **Duplicate Image Detection**: New image hash (`bbd253f`) is unique — no duplicates found ✅
- **Frontmatter Cross-Check**: `image:` line is active (not commented) — "~/assets/images/hero-pekerjaan-high-demand-malaysia-2026.jpg" ✅
- **Build**: 285 pages built successfully (1m 3s) — no cache issues ✅
- **Content Verification** (curl on port 4041):
  - `/pekerjaan-high-demand-malaysia-2026/` — title "10 Pekerjaan Paling Tinggi Permintaan di Malaysia 2026 — Sektor Mana Paling Banyak Cari Pekerja? — RakyatHub" ✅
  - OG Image: `/_astro/hero-pekerjaan-high-demand-malaysia-2026.Bc6wdvKS_Z1Djiiv.jpg` — HTTP 200, 97,231 bytes ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/join/` — title "Join Watch Party — World Cup 2026 — RakyatHub" ✅
  - `/` — homepage ✅
  - `/category/kerjaya/` — "Category 'Kerjaya' — RakyatHub" ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
- **gtagSendEvent Fix (join.astro)**: `window.gtagSendEvent = function(url)` on line 193 — 3 `onclick` handlers reference it. Prior fix from QA run 2026-06-09 08:30 now committed in this SHA. ✅
- **Status**: resolved

## 2026-06-09 10:10
- **QA Check**: Content-only build — replaced inappropriate featured image for DCA Emas GAP article
- **Commit**: `9b656bc` — fix: replace inappropriate featured image for DCA Emas GAP article with gold bars image
- **Changes**: `src/assets/images/hero-dca-emas-gap.jpg` (binary update, 122994 → 163925 bytes)
- **Pre-build**: No untracked files, no leftover images, no untracked posts ✅
- **Duplicate Image Detection**: Modified image hash (`d3081de`) is unique — no duplicates found ✅
- **Orphaned Image Detection**: Pre-existing orphans unchanged from prior run (22 public/ + 2 src/assets/ — not regressed by this commit, user should `git rm` when convenient)
- **Build**: 279 pages built successfully (1m 4s) ✅
- **Content Verification** (curl on port 3405):
  - `/dca-emas-gap-public-gold-strategi-beli-konsisten/` — title "DCA Emas GAP Public Gold — Strategi Beli Emas Konsisten RM100 Sebulan — RakyatHub" ✅
  - OG Image: `/_astro/hero-dca-emas-gap.BpAQcuD8_1rV0Ra.jpg` — HTTP 200, 85,333 bytes (new hash `BpAQcuD8`, correct gold bars image) ✅
  - Frontmatter image line: `image: "~/assets/images/hero-dca-emas-gap.jpg"` — active (not commented) ✅
  - Rendered image filename matches frontmatter — no Vite dedup or glob miss issue ✅
  - `/` — homepage renders with correct OG image ✅
  - `/category/kewangan/` — "Category 'Kewangan' — RakyatHub" ✅
- **Status**: resolved

## 2026-06-09 08:30
- **QA Check**: Full CDP pipeline — Google Ads conversion tracking on /join + 4 new content articles
- **Commit (initial)**: `dacfecd` — add google ads conversion tracking on /join page
- **Commit (HEAD at build)**: `b96364f` — Auto: 4 new articles — Tabung Haji, PTPTN, SSPN, DCA Emas GAP
- **Changes (dacfecd)**: `src/pages/join.astro` (Google Ads conversion tracking logic), `.netlify/netlify.toml` (security headers, cache control, redirects), `.netlify/functions/manifest.json` (timestamp only)
- **Changes (b96364f)**: 4 new `.md` posts + 4 new hero images (`hero-dca-emas-gap.jpg`, `hero-ptptn.jpg`, `hero-sspn.jpg`, `hero-tabung-haji.jpg`)
- **Pre-build**: 4 untracked leftover images removed (`hero-dca-emas-gap.jpg`, `hero-ptptn.jpg`, `hero-sspn.jpg`, `hero-tabung-haji.jpg` — never in git, unreferenced by any post, removed to prevent future `NoImageMetadata` build failures) ✅
- **Duplicate Image Detection**: No new images in `dacfecd` commit. New images in `b96364f` — unique hashes, no duplicates found ✅
- **Orphaned Image Detection** (noted): Same pre-existing orphans as prior run — not regressed by this commit

### Fix: Astro Module-Scoped gtagSendEvent Not Accessible from onclick Handlers
- **File**: `src/pages/join.astro:193`
- **Before**: `function gtagSendEvent(url) { ... }` — defined in Astro `<script>` block (processed as ES module, function was module-scoped, NOT on `window`). Three `onclick="return gtagSendEvent('...')"` handlers would throw `ReferenceError: gtagSendEvent is not defined` at click time — conversion tracking would silently fail despite clean build, render, and zero console errors at page load.
- **After**: `window.gtagSendEvent = function(url) { ... };` — explicitly assigned to global scope. CDP Runtime.evaluate confirms `typeof window.gtagSendEvent === "function"` ✅
- **Build**: 279 pages built (clean rebuild after clearing stale `.astro` cache which caused `EPERM: rename data-store.json.tmp` error) ✅
- **Browser Inspection**: Full CDP on port 5055 (Node.js static server)
  - DOM: main(1), header/nav(1), footer/contentinfo(1) — all present ✅
  - Images: 0 broken ✅
  - Resources: 0 failed (no 4xx/5xx) ✅
  - Console: 0 errors, 0 warnings ✅
  - Runtime: `window.gtagSendEvent` is `function` (FIX VERIFIED) ✅
  - Page title: "Join Watch Party — World Cup 2026 — RakyatHub" ✅

### Content Asset Verification (4 new posts from b96364f)
All verified via curl on port 5055:
- `/dca-emas-gap-public-gold-strategi-beli-konsisten/` — title "DCA Emas GAP Public Gold — Strategi Beli Emas Konsisten RM100 Sebulan — RakyatHub" ✅
  - OG Image: `/_astro/hero-dca-emas-gap.CVUGSal4_1kCfU0.jpg` — HTTP 200, 79,580 bytes ✅
- `/panduan-bayar-ptptn-2026-diskaun-insentif/` — title "Panduan Bayar PTPTN 2026 — Diskaun, Insentif & Cara Elak Blacklist — RakyatHub" ✅
  - OG Image: `/_astro/hero-ptptn.B4Lklrsy_Z1R4OtL.jpg` — HTTP 200, 64,541 bytes ✅
- `/panduan-sspn-2026-simpanan-pendidikan-pelepasan-cukai/` — title "Panduan SSPN 2026 — Cara Buka Akaun, Dividen & Pelepasan Cukai RM8,000 — RakyatHub" ✅
  - OG Image: `/_astro/hero-sspn.6Pgks8IG_1Xgn8H.jpg` — HTTP 200, 51,131 bytes ✅
- `/panduan-tabung-haji-2026-cara-simpan-daftar-haji/` — title "Panduan Tabung Haji 2026 — Cara Buka Akaun, Hibah & Daftar Haji — RakyatHub" ✅
  - OG Image: `/_astro/hero-tabung-haji.BtaWskAh_Z1cEUNP.jpg` — HTTP 200, 155,107 bytes ✅
- `/` — title "RakyatHub — Panduan Kewangan Rakyat Malaysia" ✅
- `/category/kewangan/` — title "Category 'Kewangan' — RakyatHub" ✅
- Cross-Image Check: All 4 rendered OG image filenames match frontmatter `image:` fields — no Vite dedup or fallback issues ✅
- Frontmatter Cross-Check: All 4 `image:` lines active (none commented out) ✅
- **Status**: resolved
