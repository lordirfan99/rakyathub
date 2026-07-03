# RakyatHub Article Pipeline — Full System (Jul 2026)

## 📊 System Overview

```
GSC DATA  ──→  TOPIC      ──→  WRITE    ──→  IMAGE     ──→  SEO    ──→  GIT    ──→  BUILD  ──→  DEPLOY  ──→  INDEX
(Isnin     3-tier         1 artikel     screenshot/    validate    push      npm       zip/      IndexNow
 6AM)      priority       per run       banner/                    commit    build     netlify   + sitemap
                                         ai_gen
```

---

## 🔄 Schedule

| Time | Cron | Days | Kategori | Artikel |
|------|------|:----:|----------|:-------:|
| **6AM** | 🔄 Refresh GSC | **Isn** | Data only | — |
| **7AM** | Pagi — Kesihatan, Pendidikan, Student | Harian | Kesihatan, Pendidikan, Student | 1 |
| **8AM** | **Bottom of Funnel** 🎯 | Harian | Cukai, Bantuan, Emas, Bisnes, Insurans | **1 BOF** |
| **10AM** | Kerjaya, Hidup Sewa, Hak Pengguna | Harian | Kerjaya, Sewa, Hak Pengguna | 1 |
| **2PM** | Insurans, Pandu Jalan Raya | Harian | Insurans, Kereta | 1 |
| **4PM** | News React, Teknologi | **Kha** | Teknologi, News | 1 |
| **6PM** | Side Hustle, Bisnes | **Rab** | Bisnes, Side Hustle, Bantuan | 1 |
| **8PM** | Malam — Gov News, Trends | **Jum** | Kerajaan, Trends | 1 |
| **10PM** | Nightly Full Deploy | Harian | Deploy sahaja | — |

**Total: ~5 artikel/hari** (4 daily + 3 weekly rata-rata)

---

## ⚙️ Phase 0: Data Collection (Isnin 6AM)

**Script/tool:** GSC MCP via agent cron
**Output:** `gsc_queries.json`

1. `mcp_advanced_gsc_get_search_analytics(site_url="sc-domain:rakyathub.my", days=30, dimensions="query,page", row_limit=100)`
2. Filter: position 5-15, 0 clicks → **low hanging fruit**
3. Save to `gsc_queries.json`

**Manual trigger:**
```
hermes cron run 94b05559f199
```

---

## 🎯 Phase 1: Topic Selection (3-Tier Priority)

### 🥇 Tier 1 — GSC Data
Baca `gsc_queries.json` → pilih query ikut kategori cron

### 🥈 Tier 2 — Gap Analysis
```bash
grep -h "^category:" src/data/post/*.md | sort | uniq -c | sort -rn
ls src/data/post/*keyword* 2>/dev/null
grep -il "keyword" src/data/post/*.md
```

### 🥉 Tier 3 — Government News
```
site:mof.gov.my | site:kwsp.gov.my | site:hasil.gov.my | etc
```
**Fallback:** Google News RSS

---

## ✍️ Phase 2: Write 1 Article

### YAML Frontmatter Format (WAJIB)

```yaml
---
title: "Cara Daftar eKasih 2026 — Panduan Syarat & Mohon"
description: "Panduan lengkap permohonan..."
publishDate: YYYY-MM-DD
excerpt: "Ringkasan SEO 120-160 chars..."
category: Kerajaan
tags:
  - Tag1
  - "2026"
image: "~/assets/images/hero-<slug>.jpg"
image_strategy: screenshot    # screenshot | banner | ai_gen
agency_logo: ""               # Isi jika banner: "LHDN", "KWSP", "MOF"
image_prompt: ""              # Isi jika ai_gen: prompt English ringkas
---
```

### image_strategy Rules

| Strategy | Untuk | Contoh | Proses |
|----------|-------|--------|--------|
| `screenshot` | BOF/Tutorial — cara mohon, daftar | Cara Daftar eKasih | Puppeteer screenshot portal rasmi |
| `banner` | Info/Berita/Pengumuman Kerajaan | GST, STR, KWSP | Puppeteer render logo + tajuk |
| `ai_gen` | Umum/Kerjaya/Side Hustle | Tips Kerjaya | image_generate tool |

### Content Structure (WAJIB untuk YMYL/BOF)

1. **Jadual Rumusan** — ringkasan topik (penerima, syarat, jumlah, tarikh)
2. **Apa Itu...** — penerangan ringkas
3. **Syarat Kelayakan** — senarai bullet point
4. **Dokumen Diperlukan** — jadual dokumen + tujuan
5. **Langkah Demi Langkah** — minimum 5 langkah bernombor
6. **Jadual Bantuan Berkaitan** — senarai jenis bantuan
7. **FAQ Situasi Sebenar** — minimum 3 FAQ teknikal
8. **Rujukan Rasmi** — URL portal kerajaan (YMYL compliance)
9. **Penafian** — "Sila rujuk portal rasmi untuk kemas kini terbaru"

### Dilarang Sama Sekali
- ❌ Halusinasi tarikh, jumlah, atau syarat
- ❌ Emoji/CJK dalam body teks
- ❌ Unquoted numeric tags (e.g. `- 2026`)
- ❌ ISO timestamp di publishDate (YYYY-MM-DD sahaja)
- ❌ Imej loremflickr atau Unsplash langsung

---

## 🖼️ Phase 3: Image Generation

### Script: `scripts/generate-article-image.cjs`

```bash
# Screenshot (portal URL)
node scripts/generate-article-image.cjs <slug> screenshot "https://portal.gov.my"

# Banner (agency logo + title)
node scripts/generate-article-image.cjs <slug> banner "LHDN"

# AI Gen (prints prompt for manual use)
node scripts/generate-article-image.cjs <slug> ai_gen "Professional banner..."
```

**Output:** `src/assets/images/hero-<slug>.jpg` (JPEG 1200x630 untuk banner, 1280x720 untuk screenshot)

**Agency colors supported:**
LHDN (blue), KWSP (red), MOF (navy), BNM (teal), JPJ (dark blue), JKM (orange), KPDN (green), KESUMA (purple), ICU (dark green), PTPTN (blue), default (grey)

---

## ✅ Phase 4: SEO Validation

```bash
python3 /c/Users/irfan/AppData/Local/hermes/skills/seo/rakyathub-seo-guardian/scripts/validate-article.py src/data/post/<slug>.md
```

**WAJIB PASS:** R1 (title 50-65), R2 (excerpt 120-160), R3 (no emoji), R8 (publishDate + category), R10 (image field exists + image file)

**Note:** R10 expects `image: "~/assets/images/...jpg"` with double quotes

---

## 🚀 Phase 5: Automated Pipeline

### Script: `scripts/pipeline.py`

**One command does all:**
```bash
# BOF/Tutorial (screenshot from portal)
python3 scripts/pipeline.py cara-daftar-ekasih-2026-syarat-kelayakan \
  --strategy screenshot \
  --url "https://ekasih2.icu.gov.my"

# Info/Berita (banner with agency logo)
python3 scripts/pipeline.py contoh-slug \
  --strategy banner \
  --agency "LHDN"

# Umum (ai_gen — prints prompt, stop)
python3 scripts/pipeline.py contoh-slug \
  --strategy ai_gen \
  --prompt "Professional banner for Malaysian topic"
```

**What it does automatically:**
1. ✅ SEO validation
2. ✅ Generate image (screenshot/banner)
3. ✅ Verify JPEG
4. ✅ Fix image field quotes in frontmatter
5. ✅ Git add → commit → push
6. ✅ npm run build
7. ✅ python3 scripts/deploy_zip.py

**Skip build/deploy:**
```bash
python3 scripts/pipeline.py slug --strategy screenshot --url "..." --skip-build
```

---

## 📈 Phase 6: Indexing

```bash
# IndexNow
curl -sL -X POST "https://api.indexnow.org/indexnow?url=https://rakyathub.my/SLUG&key=4f095c4739c2a1e52d6bdd1ee9129879"

# Sitemap ping
curl -sL "https://www.google.com/ping?sitemap=https://rakyathub.my/sitemap-index.xml"
```

---

## 🔄 The Full Loop

```
ISNIN 6AM ──→ GSC Refresh ──→ gsc_queries.json
                  │
                  ▼
SETIAP PAGI ──→ Cron baca gsc_queries.json
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
  Ada GSC    Tiada GSC    Tiada gap
  query?     query?       + tiada GSC?
      │           │           │
      ▼           ▼           ▼
  Tulis      Gap          Gov News
  artikel    Analysis     check
      │           │           │
      └───────────┼───────────┘
                  │
                  ▼
          pipeline.py
    (validate → image → commit → build → deploy)
                  │
                  ▼
          IndexNow + sitemap
                  │
                  ▼
          Ranking naik → More clicks
                  │
                  ▼
          ISNIN DEPAN → GSC refresh → Repeat 🔄
```

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `src/data/post/<slug>.md` | Artikel |
| `src/assets/images/hero-<slug>.jpg` | Hero image |
| `gsc_queries.json` | GSC data (auto-refresh Isnin 6AM) |
| `scripts/generate-article-image.cjs` | Image generator (screenshot/banner) |
| `scripts/pipeline.py` | Full automation pipeline |
| `ARTICLE_PIPELINE.md` | This document |

---

## ⚠️ Quick Pitfalls

| Issue | Fix |
|-------|-----|
| `image:` needs quotes | `image: "~/assets/images/hero.jpg"` |
| R10 fails | add quotes around image path |
| Git push fails | stored token in `.git-credentials` expired — regenerate |
| Puppeteer not found | `npm install puppeteer` |
| GSC MCP not available | `hermes gateway restart` |
| Screenshot strategy needs URL | pass `--url "https://..."` |
