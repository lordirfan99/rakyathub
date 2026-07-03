# Hermes Task — DECLUTTER the Homepage (v2, corrected)

## ⚠️ Read this first — direction correction

The last homepage change ("homepage optimised — add missing calculators, glosari, api link", commit `ba99d12`) went the **WRONG way**. It grew `src/pages/index.astro` from 382 → **590 lines** and now the homepage has **~90 links** — it's basically a full sitemap dumped on the front page.

**This task is the OPPOSITE of that. You are REMOVING and CONSOLIDATING links, not adding them.** If you finish and the homepage has *more* than ~15 primary links, you did it wrong. Fewer, bigger, clearer entry points — the homepage links to **pillar/hub pages only**, and each hub lists its own calculators/articles.

**Do NOT delete any actual pages.** Every calculator/article still exists and stays reachable from its hub (`/kalkulator/`, `/blog/`) and the footer. You are only removing the giant link lists from the *homepage*.

---

## Current state — what's on the homepage now (`src/pages/index.astro`, 590 lines)

Frontmatter arrays (all feed the bloated grids):
- `CALCULATORS_MAIN` (lines ~51–76) — **24 calculator links**
- `CALCULATORS_EXTRA` (lines ~78–91) — **12 calculator links**
- `CALCULATORS_ZAKAT` (lines ~93–99) — **5 links**
- `CALCULATORS_KESIHATAN` (lines ~101–108) — **6 links**
- `DATA_TOOLS` (lines ~110–114) — 3 cards (Inflasi, Bantuan, Harga Minyak)
- `REALITY_TOOLS` (lines ~116–120) — 3 cards
- `FEATURED` (lines ~122–138) — **15 article links**
- `CATEGORY_LINKS` (lines ~140–147) — 6 category pills

Body sections (by comment banner):
- `🇲🇾 HERO` (~171) — headline + **3 CTAs** + stats
- `🛒 HARGA MAKANAN` (~236) — 6-row food teaser + link
- `📊 DATA` (~296) — Inflasi + Bantuan + Harga Minyak
- `📊 REALITY TOOLS` (~357) — reality-check, gaji-malaysia, indeks-pasaraya, **+ Pilihan Raya**
- `🧮 KALKULATOR UTAMA` (~418) — renders `CALCULATORS_MAIN` (24)
- `🤲 ZAKAT` (~445) — renders `CALCULATORS_ZAKAT` (5)
- `❤️ KESIHATAN` (~470) — renders `CALCULATORS_KESIHATAN` (6)
- `🧮 LAGI KALKULATOR` (~495) — renders `CALCULATORS_EXTRA` (12)
- `🚀 DocuKilat CTA` (~520)
- `📰 ARTIKEL PILIHAN` (~542) — category pills (6) + `FEATURED` (15) + blog link
- `<BlogLatestPosts />` (~588), `<CallToAction />` (~589)

**Total ≈ 90 links. Target ≈ 15.**

---

## The rule: homepage = pillar pages only

Homepage links to ~8 **hubs**; each hub lists its own leaves. The pillars:

| Pillar card | URL |
|---|---|
| Kalkulator (40+ alat) | `/kalkulator/` |
| Harga Barang Runcit | `/harga-makanan-hari-ini/` |
| Harga Minyak | `/harga-minyak/` |
| Inflasi Malaysia | `/inflasi-malaysia/` |
| Bantuan Kerajaan | `/bantuan-kerajaan/` |
| Gaji & Reality Check | `/reality-check/` |
| Pilihan Raya | `/pilihan-raya/` |
| Blog / Panduan | `/blog/` |
| Alat Dokumen (DocuKilat) | `https://docukilat.rakyathub.my` |

(9 cards is fine; keep it to ≤9.)

---

## Do this — concrete edits to `src/pages/index.astro`

### DELETE outright
1. **The 4 calculator grid sections** and their arrays:
   - Remove sections `🧮 KALKULATOR UTAMA`, `🤲 ZAKAT`, `❤️ KESIHATAN`, `🧮 LAGI KALKULATOR` from the body.
   - Remove the arrays `CALCULATORS_MAIN`, `CALCULATORS_EXTRA`, `CALCULATORS_ZAKAT`, `CALCULATORS_KESIHATAN` from the frontmatter.
   - These are all replaced by the single **"Kalkulator" pillar card** → `/kalkulator/` (which already lists every calculator).
2. **The category pills** (`CATEGORY_LINKS` array + the pills markup in `📰 ARTIKEL PILIHAN`). The Blog pillar card covers this.
3. **Trim `FEATURED` from 15 → 3** (or delete it entirely and rely on `<BlogLatestPosts />` capped at 3). Keep at most 3 evergreen picks + a single "Semua artikel →" to `/blog/`.

### KEEP (but tighten)
- **Hero** — reduce to **ONE primary CTA** (e.g. "Semua Kalkulator" → `/kalkulator/`) plus maybe one secondary text link. Keep the stat chips. Drop the 3-CTA row.
- **Harga Makanan teaser** — keep as the ONE flagship live-data block (6 rows + "Lihat semua →"). This is the only inline data list allowed.
- **DocuKilat CTA** — keep (it's a pillar).
- **`<BlogLatestPosts />`** — keep, cap at 3 posts (check the component's limit prop).
- **`<CallToAction />`** — keep.

### REPLACE the middle of the page with ONE pillar grid
- Fold `DATA_TOOLS` + `REALITY_TOOLS` + Pilihan Raya + the Kalkulator/Blog/DocuKilat entries into a **single section titled e.g. "Terokai RakyatHub"** that renders the **9 pillar cards** from the table above (icon + title + one-line desc, linking to the hub URL).
- 3 columns desktop / 2 tablet / 1 mobile. Reuse the existing card classes already in the file (`premium-card` / `premium-card-hover`) — do not invent new styles.
- After this, the page body is: Hero → Pillar grid → Harga-makanan teaser → (Latest 3 articles) → DocuKilat → CallToAction. ~6 sections, one scrollable screen-worth each.

---

## Target result
- Homepage body ≈ **250–320 lines** (down from 590).
- **≈ 15 primary links total** (down from ~90).
- Exactly **one** pillar grid; **zero** calculator grids; **zero** category pill rows; **≤3** article links.
- Reads in ~3 scrolls, uncluttered on mobile and desktop.

## Guardrails
- **Removing links from the homepage does NOT hurt SEO** — every calculator is still linked from `/kalkulator/`, every article from `/blog/` and the footer (`src/navigation.ts` `footerData`). Confirm no page becomes orphaned (if a leaf was ONLY linked from the homepage, ensure its hub links it — the kalkulator hub and blog index already do).
- Don't touch the header/nav (already 6 items) or the footer long-tail links.
- Keep `orgSchema` JSON-LD and `metadata`.
- Keep the harga-makanan build-time widget working (`foodData`, `foodWidget`, `slugify`, `getEmoji`).
- Reuse existing components/classes; add no dependencies; no new client JS.
- Commit to `main` with `[skip netlify]` and deploy via `scripts/full-deploy.py` (local build + direct upload — Netlify build minutes are constrained).

## Acceptance criteria
1. `grep -c "href=" src/pages/index.astro` drops from ~90 to ~15–20.
2. No `CALCULATORS_MAIN/EXTRA/ZAKAT/KESIHATAN` arrays remain; no 4 calculator-grid sections remain.
3. One "Terokai RakyatHub" pillar grid of ≤9 hub cards is present.
4. Featured/blog links ≤3; category pills removed.
5. Harga-makanan teaser still renders; hero has one primary CTA.
6. `npm run build` passes (1804 pages); homepage looks clean on mobile + desktop.
7. No orphaned pages (spot-check: every calculator still reachable via `/kalkulator/`).

## Files
- `src/pages/index.astro` — all changes. Arrays at lines ~51–147; sections at comment banners ~171/236/296/357/418/445/470/495/520/542.
- `src/components/widgets/BlogLatestPosts.astro` — cap to 3.
- `src/navigation.ts` `footerData` — the long-tail lives here; leave as-is.

## Owner
irfanthefast@gmail.com · https://rakyathub.my · repo `lordirfan99/rakyathub` (branch `main`)
