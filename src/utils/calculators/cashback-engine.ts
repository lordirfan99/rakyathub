/**
 * Cashback Combo Allocation Engine
 *
 * Implements a "Greedy Allocation Algorithm" to find the best distribution
 * of monthly spending across a combination of up to 3 credit cards.
 *
 * Key invariants:
 *  - A card earns the tier rate ONLY if total allocated spend meets minMonthlySpend.
 *    Otherwise it falls back to baseCashbackRate.
 *  - categoryCap limits cashback earned for a single category on one card.
 *  - poolCap limits the total cashback across all categories in one tier.
 *  - isWeekendOnly cards are evaluated at 50% of rate (approximation; actual
 *    varies with spend patterns — we use 50% as a conservative estimate for
 *    monthly projections).
 */

import type { CreditCard, Category } from '~/data/cashback-cards';

// ─────────────────────────────────────────────────────────────
// PUBLIC TYPES
// ─────────────────────────────────────────────────────────────

export interface SpendInput {
  category: Category;
  amount: number; // RM per month
}

export interface CardAllocationDetail {
  cardId: string;
  cardName: string;
  bank: string;
  hexColor: string;
  allocatedSpend: number;         // Total RM spend allocated to this card
  earnedCashback: number;         // RM cashback earned (after all caps)
  breakdown: CategoryBreakdown[]; // Per-category detail
  metMinSpend: boolean;           // Did this card meet its minMonthlySpend?
}

export interface CategoryBreakdown {
  category: Category;
  spend: number;       // RM spend for this category on this card
  rate: number;        // Effective rate applied
  cashback: number;    // RM cashback earned for this category (after caps)
  cappedBy: 'none' | 'categoryCap' | 'poolCap';
}

export interface ComboResult {
  cards: CardAllocationDetail[];
  totalCashback: number;
  monthlyFeeAmortized: number; // Annual fee / 12 — subtract for net comparison
  netCashback: number;         // totalCashback - monthlyFeeAmortized
}

// ─────────────────────────────────────────────────────────────
// ALGORITHM: computeCombo
//
// Complexity: O(C × T × K) where C = categories (≤15), T = tiers per card (≤5),
//             K = cards in combo (≤3). For 50 cards C(50,3)=19,600 combos,
//             each combo runs in constant time → total ~300K ops, well within budget.
// ─────────────────────────────────────────────────────────────

export function computeCombo(
  spend: SpendInput[],
  combo: CreditCard[],
): ComboResult {
  const K = combo.length; // 1, 2, or 3

  // ── Step 1: For each category, determine which card offers the best effective rate ──
  // Build a priority list: for each category, sort cards by potential rate (descending)
  type CardRateEntry = { cardIdx: number; tierIdx: number; rate: number };
  const categoryPriority: Record<string, CardRateEntry[]> = {};

  for (const { category } of spend) {
    const entries: CardRateEntry[] = [];
    for (let i = 0; i < K; i++) {
      const card = combo[i];
      // Find the tier that covers this category with the highest rate
      let bestRate = card.baseCashbackRate;
      let bestTierIdx = -1;
      for (let t = 0; t < card.tiers.length; t++) {
        const tier = card.tiers[t];
        if (tier.categories.includes(category)) {
          const effectiveRate = tier.isWeekendOnly ? tier.rate * 0.5 : tier.rate;
          if (effectiveRate > bestRate) {
            bestRate = effectiveRate;
            bestTierIdx = t;
          }
        }
      }
      entries.push({ cardIdx: i, tierIdx: bestTierIdx, rate: bestRate });
    }
    // Sort descending by rate
    entries.sort((a, b) => b.rate - a.rate);
    categoryPriority[category] = entries;
  }

  // ── Step 2 & 3: Greedy allocation with cap tracking ──
  // State per card: total allocated spend, cashback earned per tier
  const allocatedSpend = new Array(K).fill(0);
  const tierCashback: number[][] = combo.map(c => new Array(c.tiers.length).fill(0));
  const catCashback: Record<string, number[]> = {}; // [category][cardIdx]
  for (const { category } of spend) {
    catCashback[category] = new Array(K).fill(0);
  }
  const breakdowns: CategoryBreakdown[][] = combo.map(() => []);

  for (const { category, amount } of spend) {
    let remainingSpend = amount;
    const priority = categoryPriority[category];

    for (const { cardIdx, tierIdx, rate } of priority) {
      if (remainingSpend <= 0) break;
      const card = combo[cardIdx];

      if (tierIdx === -1) {
        // Base rate — no tier covers this category, allocate all remaining to base
        const cashback = remainingSpend * rate;
        allocatedSpend[cardIdx] += remainingSpend;
        breakdowns[cardIdx].push({
          category,
          spend: remainingSpend,
          rate,
          cashback,
          cappedBy: 'none',
        });
        remainingSpend = 0;
        break;
      }

      const tier = card.tiers[tierIdx];
      const effectiveRate = tier.isWeekendOnly ? tier.rate * 0.5 : tier.rate;

      // How much can this tier still earn? (pool cap check)
      const tierEarnedSoFar = tierCashback[cardIdx][tierIdx];
      const tierRemaining =
        tier.poolCap > 0 ? Math.max(0, tier.poolCap - tierEarnedSoFar) : Infinity;

      // How much can this category still earn? (category cap check)
      const catEarnedSoFar = catCashback[category][cardIdx];
      const catRemaining =
        tier.categoryCap > 0 ? Math.max(0, tier.categoryCap - catEarnedSoFar) : Infinity;

      // Effective cap on cashback for this allocation
      const maxCashback = Math.min(tierRemaining, catRemaining);
      if (maxCashback <= 0) continue; // Both caps exhausted, skip

      // Spend needed to hit the cashback cap
      const spendToHitCap = maxCashback / effectiveRate;
      const spendHere = Math.min(remainingSpend, spendToHitCap);
      const cashbackHere = Math.min(spendHere * effectiveRate, maxCashback);

      let cappedBy: 'none' | 'categoryCap' | 'poolCap' = 'none';
      if (cashbackHere < remainingSpend * effectiveRate) {
        if (catRemaining <= tierRemaining) {
          cappedBy = 'categoryCap';
        } else {
          cappedBy = 'poolCap';
        }
      }

      allocatedSpend[cardIdx] += spendHere;
      tierCashback[cardIdx][tierIdx] += cashbackHere;
      catCashback[category][cardIdx] += cashbackHere;
      remainingSpend -= spendHere;

      breakdowns[cardIdx].push({
        category,
        spend: spendHere,
        rate: effectiveRate,
        cashback: cashbackHere,
        cappedBy,
      });
    }

    // If any spend still unallocated (all caps exhausted), assign to highest-base card
    if (remainingSpend > 0) {
      const bestBase = priority[0];
      const baseRate = combo[bestBase.cardIdx].baseCashbackRate;
      const cashback = remainingSpend * baseRate;
      allocatedSpend[bestBase.cardIdx] += remainingSpend;
      breakdowns[bestBase.cardIdx].push({
        category,
        spend: remainingSpend,
        rate: baseRate,
        cashback,
        cappedBy: 'none',
      });
    }
  }

  // ── Step 4: Check minMonthlySpend — if not met, recalculate at base rate ──
  const cardDetails: CardAllocationDetail[] = combo.map((card, i) => {
    const metMinSpend = allocatedSpend[i] >= card.tiers.reduce(
      (max, t) => Math.max(max, t.minMonthlySpend), 0,
    );

    let earnedCashback: number;
    let finalBreakdowns: CategoryBreakdown[];

    if (metMinSpend) {
      earnedCashback = tierCashback[i].reduce((s, v) => s + v, 0);
      // Also add base-rate spends
      const baseSpend = breakdowns[i]
        .filter(b => !combo[i].tiers.some(t => t.categories.includes(b.category)))
        .reduce((s, b) => s + b.cashback, 0);
      earnedCashback += baseSpend;
      finalBreakdowns = breakdowns[i];
    } else {
      // Recalculate everything at base rate
      earnedCashback = allocatedSpend[i] * card.baseCashbackRate;
      finalBreakdowns = breakdowns[i].map(b => ({
        ...b,
        rate: card.baseCashbackRate,
        cashback: b.spend * card.baseCashbackRate,
        cappedBy: 'none' as const,
      }));
    }

    return {
      cardId: card.id,
      cardName: card.cardName,
      bank: card.bank,
      hexColor: card.hexColor,
      allocatedSpend: allocatedSpend[i],
      earnedCashback: Math.round(earnedCashback * 100) / 100,
      breakdown: finalBreakdowns,
      metMinSpend,
    };
  });

  const totalCashback = cardDetails.reduce((s, c) => s + c.earnedCashback, 0);
  const monthlyFeeAmortized = combo.reduce((s, c) => s + c.annualFee / 12, 0);

  return {
    cards: cardDetails,
    totalCashback: Math.round(totalCashback * 100) / 100,
    monthlyFeeAmortized: Math.round(monthlyFeeAmortized * 100) / 100,
    netCashback: Math.round((totalCashback - monthlyFeeAmortized) * 100) / 100,
  };
}

// ─────────────────────────────────────────────────────────────
// OPTIMIZER: findBestCombos
//
// Evaluates all C(N,k) combinations for k = 1, 2, 3 using the
// computeCombo engine and returns the top-K results sorted by
// netCashback descending.
//
// C(50,1) = 50
// C(50,2) = 1,225
// C(50,3) = 19,600
// Total = 20,875 combinations — fast enough for the main thread.
// Above 50,000 combos (if card DB grows), use the Web Worker variant.
// ─────────────────────────────────────────────────────────────

export interface OptimizeResult {
  combo: CreditCard[];
  result: ComboResult;
}

export function findBestCombos(
  spend: SpendInput[],
  cards: CreditCard[],
  topK = 5,
): OptimizeResult[] {
  const results: OptimizeResult[] = [];

  // Filter cards to only those at least partially matching spend categories
  const spendCategories = new Set(spend.filter(s => s.amount > 0).map(s => s.category));
  const relevantCards = cards.filter(card =>
    card.tiers.some(t => t.categories.some(c => spendCategories.has(c as Category))) ||
    card.baseCashbackRate > 0,
  );

  const N = relevantCards.length;

  for (let i = 0; i < N; i++) {
    // k=1
    const r1 = computeCombo(spend, [relevantCards[i]]);
    results.push({ combo: [relevantCards[i]], result: r1 });

    for (let j = i + 1; j < N; j++) {
      // k=2
      const r2 = computeCombo(spend, [relevantCards[i], relevantCards[j]]);
      results.push({ combo: [relevantCards[i], relevantCards[j]], result: r2 });

      for (let k = j + 1; k < N; k++) {
        // k=3
        const r3 = computeCombo(spend, [
          relevantCards[i],
          relevantCards[j],
          relevantCards[k],
        ]);
        results.push({
          combo: [relevantCards[i], relevantCards[j], relevantCards[k]],
          result: r3,
        });
      }
    }
  }

  results.sort((a, b) => b.result.netCashback - a.result.netCashback);
  return results.slice(0, topK);
}
