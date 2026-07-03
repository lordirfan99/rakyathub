# Hermes Task — Declutter the RakyatHub Homepage to Pillar Pages Only

## Goal

The homepage (`src/pages/index.astro`) is overcrowded — it links to **~40+ individual (leaf) pages**: every calculator, every featured article, individual food items, etc. Rework it so the homepage surfaces only the **pillar / hub pages**, with each pillar card linking INTO the hub that then lists its own leaf pages. Fewer, bigger, clearer entry points — not a wall of links.

**Do NOT delete any pages or break internal linking.** The leaf links move to their pillar pages (where they belong); the homepage just stops listing them all.

---

## The principle: pillar pages, not leaf pages

Topic-cluster model:
- **Homepage → links to ~8 pillar/hub pages** (broad topics).
- **Each pillar page → links to its leaf/cluster pages** (the individual calculators, articles, items).
- Link equity and user attention flow homepage → pillar → leaf. This is better for SEO AND for humans than dumping every leaf link on the homepage.

**The pillar pages of RakyatHub** (these — and only these — get prominent homepage placement):

| Pillar | URL | What it hubs |
|---|---|---|
| Kalkulator | `/kalkulator/` | all 40+ calculators |
| Harga Barang Runcit | `/harga-makanan-hari-ini/` | live food prices + per-item pages |
| Harga Minyak | `/harga-minyak/` | fuel price tracker |
| Inflasi Malaysia | `/inflasi-malaysia/` | CPI dashboard |
| Bantuan Kerajaan | `/bantuan-kerajaan/` | STR/SARA + aid listings |
| Gaji & Reality Check | `/reality-check/` (and `/gaji-malaysia/`) | salary data, comparisons |
| Pilihan Raya | `/pilihan-raya/` | election hub (Cek Wakil Rakyat, PRU, PRK) |
| Blog / Panduan | `/blog/` | all articles |
| Alat Dokumen | `/docukilat/` | document generator |

---

## Current homepage inventory (what's there now — `src/pages/index.astro`, 382 lines)

1. **Hero** (~line 91) — tagline, headline, CTAs, stats. **Keep** (tighten copy only).
2. **Harga Makanan widget** (~line 154) — 6 food rows + link. **Keep as the ONE flagship live-data teaser**, but compact.
3. **Data Tools** (~line 217) — Inflasi + Bantuan cards. **Keep as pillar cards.**
4. **Reality Tools** (~line 263) — Gaji & comparison. **Keep as ONE pillar card.**
5. **Kalkulator grid** (~line 310) — driven by the `CALCULATORS` array (lines 41–54): **12 individual calculator links**. ← **MAIN OFFENDER. Trim.**
6. **Artikel Pilihan** (~line 335) — driven by the `FEATURED` array (lines 56–67): **10 article links**. ← **SECOND OFFENDER. Trim.**
7. **DocuKilat CTA** (~line 358). **Keep as pillar card.**
8. **BlogLatestPosts** (line 380) — latest posts widget. **Keep but cap at 3.**
9. **CallToAction** (line 381). **Keep.**

---

## Target homepage (do this)

Rebuild the page around this order and link budget. Aim for **~15 primary links total**, not 40+.

1. **Hero** — one clear headline + **one** primary CTA ("Semua Kalkulator" or "Terokai Alat") + the stat chips. Keep it clean.
2. **Pillar grid — "Terokai RakyatHub"** — a single tidy grid of the **8 pillar cards** from the table above (icon + title + one-line desc + the hub URL). This is the heart of the new homepage. 3 columns on desktop, 2 on tablet, 1 on mobile. Each card links to its hub, NOT to a leaf.
3. **Flagship live data — Harga Barang Runcit** — keep the existing 6-row food teaser (it's the site's signature live feature) with a single "Lihat semua harga →" link to `/harga-makanan-hari-ini/`. One teaser only — do not also inline the fuel/inflation data; those are pillar cards above.
4. **Latest articles — max 3** — replace the 10-item `FEATURED` array with the 3 most evergreen (or just render the existing `BlogLatestPosts` capped at 3) + a "Semua artikel →" link to `/blog/`. Remove the hand-maintained 10-link `FEATURED` grid.
5. **DocuKilat CTA band** — keep (it's a product pillar).
6. **Newsletter / CallToAction** — keep.

### Specific edits
- **`CALCULATORS` array (lines 41–54):** either delete the 12-item grid section entirely (the "Kalkulator" pillar card already links to `/kalkulator/`), OR reduce it to **the 4 most-used calculators max** (suggest: KWSP, Gaji Bersih, Loan Rumah, STR & SARA) as a small "Kalkulator popular" strip with a prominent "Lihat 40+ kalkulator →" link. Prefer deleting it — the pillar card covers it.
- **`FEATURED` array (lines 56–67):** cut from 10 to **0–3**. Prefer removing the manual array and letting `BlogLatestPosts` (capped at 3) do the job, so it stays fresh automatically.
- **Data Tools + Reality Tools sections:** fold Inflasi, Bantuan, and Reality Check into the single **pillar grid** (#2 above) instead of separate bespoke sections — this removes 2 whole sections and unifies the visual language.
- Keep the harga-makanan static widget logic (`foodData`, `foodWidget`) — just ensure it's the only inline data teaser.

---

## Design / UX guardrails

- **One primary CTA in the hero.** Secondary links are fine but visually lighter.
- **Every section = one clear purpose + one "see all" link** to its pillar. No section should list more than ~6 links.
- Consistent card style across the pillar grid (reuse the existing flat/premium card classes already in the file — don't invent new ones).
- Generous whitespace between sections; the page should feel scannable in ~3 scrolls, not 8.
- Mobile: pillar grid stacks to 1 column; tap targets ≥44px.
- Keep it fast: the homepage is static/SSG — no new client JS needed for this (it's layout/markup only).

## SEO / internal-linking note (important)

- Removing leaf links from the homepage does **not** hurt SEO **as long as** each pillar page robustly links to its leaves. Before/while trimming, confirm:
  - `/kalkulator/` lists all calculators (it does — `src/pages/kalkulator/index.astro`).
  - `/blog/` paginates all articles.
  - `/harga-makanan-hari-ini/` links to per-item pages.
- The footer (`src/navigation.ts` `footerData`) already carries deeper links — keep it; it's the right place for the long tail.
- Do not orphan any page: if a leaf was ONLY linked from the homepage, make sure its pillar links to it.

## Constraints
- Don't change the header/nav (already de-cluttered to 6 items).
- Don't remove the JSON-LD (`orgSchema`) or metadata.
- Reuse existing components (`BlogLatestPosts`, `CallToAction`, existing card/section classes). Don't add dependencies.
- Keep the harga-makanan build-time data widget working.
- Commit to `main`. Since Netlify build minutes are constrained, tag the commit `[skip netlify]` and deploy via `scripts/full-deploy.py` (local build + direct upload).

## Acceptance criteria
1. Homepage shows a single clean **pillar grid** of ~8 hub cards; no 12-calculator grid, no 10-article grid.
2. Total primary links on the page ≈ 15 (down from ~40+).
3. Each pillar card links to a hub URL from the table; each content section has a single "see all →" link.
4. Harga-makanan teaser still renders (6 rows, live-ish build data) as the one flagship data block.
5. Latest articles capped at 3, auto-populated.
6. No orphaned pages; `/kalkulator/`, `/blog/`, `/harga-makanan-hari-ini/` still link their leaves.
7. Builds clean (`npm run build`, 1804 pages) and looks uncluttered on mobile + desktop.

## Files
- `src/pages/index.astro` — the homepage (all changes here). Key spots: `CALCULATORS` (41–54), `FEATURED` (56–67), section comments at lines 91/154/217/263/310/335/358.
- `src/components/widgets/BlogLatestPosts.astro` — cap to 3 (check its props/limit).
- `src/navigation.ts` — `footerData` holds the long-tail links (leave as-is).

## Owner
irfanthefast@gmail.com · https://rakyathub.my · repo `lordirfan99/rakyathub` (branch `main`)
