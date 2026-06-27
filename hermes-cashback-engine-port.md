# Hermes Task — Port the Tested Cashback Engine into the Live Page

## TL;DR

The Cashback Combo Optimizer at `/kalkulator/cashback-combo/` has **two separate engines**:

1. **`src/utils/calculators/cashback-engine.ts`** — the *correct, unit-tested* engine (14 passing Vitest tests).
2. **An inline copy inside `src/pages/kalkulator/cashback-combo.astro`** (the `<script is:inline>` block) — a *separately hand-written* engine that the browser actually runs.

**The tests pass against #1, but the live page runs #2.** They diverge on 4 things. Your job is to make the live page use the SAME logic as the tested engine, so passing tests actually mean the live page is correct.

⚠️ **Do NOT rewrite the tested `.ts` engine.** It is correct. The work is to make the inline browser code match it.

---

## Files & exact locations

| File | Role |
|---|---|
| `src/pages/kalkulator/cashback-combo.astro` | The page. Frontmatter flattens card data; the `<script is:inline>` block (≈ line 295 onward) is the live engine + UI. **This is what you edit.** |
| `src/utils/calculators/cashback-engine.ts` | The reference engine. `computeCombo()` and `findBestCombos()`. **Read it; copy its logic; do not change it.** |
| `src/utils/calculators/cashback-engine.test.ts` | 14 Vitest tests covering the edge cases. **These define "correct".** |
| `src/data/cashback-cards.ts` | The 50-card database. `CreditCard` + `CardTier` interfaces, `CATEGORIES` list. |

Run the tests with: `npx vitest run src/utils/calculators/cashback-engine.test.ts`
Build with: `npx astro build` (must pass, currently 1804 pages).

---

## The 4 divergences (what's wrong in the inline engine)

Reference the current inline functions in `cashback-combo.astro`:
- `calcCardCategory(card, categoryId, amount, eligibleSpend)` — ~line 353
- `calcCombo(cardIds, allCards, spending)` — ~line 366
- `runOptimizer()` — ~line 387
- The frontmatter `flatCards` mapping — ~line 49
- The `CAT_ID` map — ~line 43

### Divergence 1 — Minimum-spend gate uses TOTAL spend, not PER-CARD allocated spend
**Inline (wrong):** `calcCombo` computes `ts` = sum of ALL spending (line 369) and passes `ts` as `eligibleSpend` to every card (line 376). So a tier whose `min_spend` is RM3,000 is treated as unlocked whenever the user's *total* monthly spend ≥ RM3,000 — even if that specific card only gets RM400 routed to it.
**Tested `.ts` (correct):** `computeCombo` (see its "Step 4", lines ~191-217) checks `allocatedSpend[i] >= tier.minMonthlySpend` — i.e. the spend *actually allocated to that card*. If a card doesn't meet its own minimum, ALL its cashback recalculates at `baseCashbackRate`.
**Effect of the bug:** premium high-min-spend cards (e.g. `maybank-visa-signature` min RM3,000, `citi-prestige` min RM5,000) are over-credited and rank too high.

### Divergence 2 — No greedy spillover across cards
**Inline (wrong):** `calcCombo` (lines 374-378) assigns each category 100% to the single best card, then never spills the overflow to the 2nd-best card when a cap is hit.
**Tested `.ts` (correct):** `computeCombo` (lines ~107-189) does true greedy allocation: for each category it walks cards in rate order, fills the best card until its `categoryCap`/`poolCap` is hit, then **spills the remaining spend to the next card**.
**Test that proves it:** `cashback-engine.test.ts` — the spillover case (RM600 petrol → RM300 earns on card A capped at RM30, remaining RM300 spills to card B). The inline engine just caps at one card and wastes the rest.

### Divergence 3 — Pool cap applied as crude post-hoc scaling
**Inline (wrong):** `calcCombo` line 379 applies `poolCap` by proportionally scaling down a card's already-computed category cashbacks *after* allocation (`ra = pc/ct`).
**Tested `.ts` (correct):** pool cap is enforced *during* allocation as `min(categoryCap_remaining, poolCap_remaining)` so allocation decisions respect it in real time (and spill correctly — see Divergence 2).

### Divergence 4 — Base cashback rate is not modeled at all
**Inline (wrong):** the frontmatter `flatCards` (line 49) drops `baseCashbackRate` entirely. It only emits per-tier `cashback` rules. There is no `'*'`/base fallback, so:
  - a category not covered by any tier earns **0** on that card (should earn the card's base rate), and
  - the min-spend fallback in Divergence 1 has nothing to fall back *to*.
**Tested `.ts` (correct):** every `CreditCard` has `baseCashbackRate`; uncovered categories and min-spend-failures earn at base.

---

## The fix — port `computeCombo` to the client

The cleanest, lowest-risk approach is: **serialize the raw card data (with tiers intact) to the browser, and port the tested `computeCombo` + `findBestCombos` verbatim into the inline script.** Keep all UI rendering (card badges, modals, spend inputs) exactly as-is.

### Step 1 — Serialize raw cards (not the lossy flat shape)
In the frontmatter of `cashback-combo.astro`, the current `flatCards` loses `baseCashbackRate`, `minMonthlySpend` per tier, `isWeekendOnly`, `categoryCap` vs `poolCap` distinction. Instead, serialize the structure the `.ts` engine expects.

- Keep `flatCards` ONLY for what the UI badges/modals need (`primaryHex`, `network`, `imageUrl`, `annual_fee`, display label). 
- ADD a second serialized payload that mirrors the `CreditCard` schema the engine needs: `id, baseCashbackRate, annualFee, tiers:[{minMonthlySpend, categories:[normalized ids], rate, categoryCap, poolCap, isWeekendOnly}]`.
- **Category IDs must be normalized to the UI ids** using the existing `CAT_ID` map (line 43) — e.g. `'Online Shopping' → 'online'`, `'Telco' → 'telco'`, `'Others' → 'others'`. Apply `CAT_ID[cat] || cat.toLowerCase().replace(/\s+/g,'')` to every tier category AND keep the base rate as a catch-all (the engine applies base to any uncovered category, so you do NOT need a `'*'` pseudo-category — model it as `baseCashbackRate`).

### Step 2 — Port the engine functions verbatim
Copy `computeCombo` and `findBestCombos` from `cashback-engine.ts` into the inline `<script>`, converting TypeScript to plain ES5/ES6 JS (the inline block uses `var` and function declarations — match that style; no `import`, no types). Preserve EXACTLY:
- the priority-list build (sort cards by effective rate per category),
- the greedy allocation with spillover,
- `categoryCap` and `poolCap` tracked as remaining-cashback budgets, `min()` of the two,
- the `isWeekendOnly ? rate*0.5 : rate` effective rate (note: the `.ts` halves at compute time; if you keep the halving in serialization instead, do NOT double-halve),
- **Step 4**: if `allocatedSpend < maxTierMinMonthlySpend` for a card → recompute that card at `baseCashbackRate`,
- `netCashback = totalCashback − annualFee/12`, and **sort `findBestCombos` by `netCashback` descending**.

### Step 3 — Rewire the UI to the ported engine
- Replace the calls to the old `calcCombo` / `calcCardCategory` inside `runOptimizer()` with `findBestCombos(spending, cards, 20)` (or loop `computeCombo` over C(n,3) combos exactly as `findBestCombos` does).
- `runOptimizer` already builds the candidate card list `ac` (handles optimal vs owned mode, the <3-card guard) — keep that. Feed `ac` into the ported optimizer.
- The result objects the UI renders (`renderResults`, the hero, the per-combo breakdown `combo.breakdown[cardId][catId] = {amount, cashback}`, the fee line) must keep the same shape, OR update `renderResults` to read the `.ts` engine's `ComboResult` shape (`cards[].breakdown[]`, `totalCashback`, `monthlyFeeAmortized`, `netCashback`). Pick one and be consistent. The `.ts` `ComboResult` is richer (per-card `metMinSpend`, `cappedBy`) — surfacing `cappedBy` and `metMinSpend` in the breakdown UI would be a nice bonus but is optional.
- Keep `getSpending()`, the spend inputs (`sp-petrol`, `sp-telco`, `sp-others`, etc.), the `CATEGORIES`/`CATEGORY_LABELS` arrays, the card badges (`cardFace`), and the modal (`showCardDetail`) unchanged.

### Step 4 — Make the modal "Min. Spend" truthful
Currently `flatCards.min_spend` is hardcoded to `0` (line 60), so every card's modal shows "Tiada". After the port, surface the real per-tier minimum (e.g. `max(tier.minMonthlySpend)`), so `modalMinSpend` (line 484) reflects reality.

---

## Acceptance criteria (must all hold)

1. `npx vitest run` — all existing tests still pass (you didn't touch the `.ts` engine).
2. `npx astro build` passes (currently 1804 pages).
3. **Behavioural parity check (do this manually):** pick 3 specific cards and a spend profile, compute the result with the `.ts` `computeCombo` (write a tiny throwaway Node/Vitest snippet), then enter the SAME spend on the live page and confirm the top combo's total cashback matches to the cent. Test at least:
   - a combo containing a **high-min-spend card** with total spend BELOW that card's min (must fall back to base — Divergence 1),
   - a category with spend that **exceeds one card's category cap** (must spill to the next card — Divergence 2),
   - a **weekend-only** card (effective rate halved, not full),
   - a combo with a **fee card** (ranked by net, fee shown).
4. No console errors. Reset, optimal mode, owned mode (≥3 cards), and URL-param prefill (`?cards=...&spend=...`) all still work.
5. The serialized payload size is reasonable (50 cards × tiers — should be a few KB; fine inline).

---

## Guardrails

- **Do not** modify `cashback-engine.ts` or `cashback-engine.test.ts` — they are the source of truth.
- **Do not** change the visual design, card badges, colours, or the spend-input grid.
- **Do not** reintroduce the dead categories (Transport/Shopping/Overseas/Hotel) — the inputs are now Telco/Lain-lain/Kerajaan/Hospital to match card data.
- Keep the inline script as `is:inline` (it must run in the browser without a build step).
- Match the existing code style in the inline block (`var`, function declarations, no ES modules).
- Commit to branch `main`, descriptive message, then build once more before pushing.

## Context: what was already fixed (don't redo)
A prior QA pass already fixed, in the inline engine: the `'Online Shopping'→'online'` category-key mismatch, annual-fee net ranking, weekend-rate halving at flatten time, the owned-mode <3-card guard, and aligned the spend inputs with card data. The ONLY remaining work is the 4 algorithmic divergences above (per-card min-spend, spillover, pool-cap-during-allocation, base-rate modelling) — which collectively require porting the real engine rather than patching the approximation.

---

## Owner
irfanthefast@gmail.com · https://rakyathub.my · repo `lordirfan99/rakyathub` (branch `main`)
