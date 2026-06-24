/**
 * Unit tests for the Cashback Combo Allocation Engine
 * Run with: npx vitest run src/utils/calculators/cashback-engine.test.ts
 */

import { describe, it, expect } from 'vitest';
import { computeCombo } from './cashback-engine';
import type { CreditCard, SpendInput } from './cashback-engine';

// ─────────────────────────────────────────────────────────────
// TEST FIXTURE HELPERS
// ─────────────────────────────────────────────────────────────

function makeCard(overrides: Partial<CreditCard> = {}): CreditCard {
  return {
    id: 'test-card',
    bank: 'Test Bank',
    cardName: 'Test Card',
    hexColor: '#123456',
    network: 'Visa',
    minIncome: 0,
    annualFee: 0,
    feeWaiverCondition: '',
    baseCashbackRate: 0,
    tiers: [],
    ...overrides,
  };
}

// ─────────────────────────────────────────────────────────────
// SPEC A — Missed Minimum Monthly Spend → falls back to base rate
// ─────────────────────────────────────────────────────────────
describe('Rule: minMonthlySpend', () => {
  it('A1: returns base rate cashback when spend is below minMonthlySpend', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 500,   // ← requires RM500
          categories: ['Petrol'],
          rate: 0.05,             // 5%
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Petrol', amount: 400 }]; // RM400 < RM500
    const result = computeCombo(spend, [card]);

    expect(result.cards[0].metMinSpend).toBe(false);
    // 0% base rate → RM0 cashback
    expect(result.totalCashback).toBe(0);
    expect(result.netCashback).toBe(0);
  });

  it('A2: returns 5% cashback when spend exactly meets minMonthlySpend', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 500,
          categories: ['Petrol'],
          rate: 0.05,
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Petrol', amount: 500 }];
    const result = computeCombo(spend, [card]);

    expect(result.cards[0].metMinSpend).toBe(true);
    expect(result.totalCashback).toBe(25); // 500 × 5% = RM25
  });

  it('A3: uses baseCashbackRate (0.1%) fallback instead of 0 if specified', () => {
    const card = makeCard({
      baseCashbackRate: 0.001,   // 0.1%
      tiers: [
        {
          minMonthlySpend: 500,
          categories: ['Petrol'],
          rate: 0.05,
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Petrol', amount: 400 }];
    const result = computeCombo(spend, [card]);

    expect(result.cards[0].metMinSpend).toBe(false);
    expect(result.totalCashback).toBeCloseTo(0.4, 4); // 400 × 0.1% = RM0.40
  });
});

// ─────────────────────────────────────────────────────────────
// SPEC B — Category Cap
// ─────────────────────────────────────────────────────────────
describe('Rule: categoryCap', () => {
  it('B1: caps cashback at categoryCap regardless of actual spend', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol'],
          rate: 0.05,           // 5%
          categoryCap: 15,      // ← max RM15
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Petrol', amount: 1000 }];
    // Without cap: 1000 × 5% = RM50. With cap → RM15.
    const result = computeCombo(spend, [card]);

    expect(result.totalCashback).toBe(15);
    expect(result.cards[0].breakdown[0].cappedBy).toBe('categoryCap');
  });

  it('B2: earns below cap when spend does not hit the cap threshold', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol'],
          rate: 0.05,
          categoryCap: 15,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Petrol', amount: 200 }];
    // 200 × 5% = RM10, below the RM15 cap
    const result = computeCombo(spend, [card]);

    expect(result.totalCashback).toBe(10);
    expect(result.cards[0].breakdown[0].cappedBy).toBe('none');
  });
});

// ─────────────────────────────────────────────────────────────
// SPEC C — Pool Cap
// ─────────────────────────────────────────────────────────────
describe('Rule: poolCap', () => {
  it('C1: total across categories is capped by poolCap', () => {
    // Card gives 5% on Petrol AND Groceries, pool cap RM50
    // Petrol RM800 → would earn RM40
    // Groceries RM500 → would earn RM25
    // Combined RM65 > RM50 pool cap → must stop at RM50
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol', 'Groceries'],
          rate: 0.05,
          categoryCap: 0,       // no individual cap
          poolCap: 50,          // ← total cap RM50
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [
      { category: 'Petrol', amount: 800 },
      { category: 'Groceries', amount: 500 },
    ];
    const result = computeCombo(spend, [card]);

    expect(result.totalCashback).toBe(50); // not 65
    // At least one entry should be capped by poolCap
    const hasCap = result.cards[0].breakdown.some(b => b.cappedBy === 'poolCap');
    expect(hasCap).toBe(true);
  });

  it('C2: pool cap does not trigger if combined cashback is below cap', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol', 'Groceries'],
          rate: 0.05,
          categoryCap: 0,
          poolCap: 50,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [
      { category: 'Petrol', amount: 200 },   // RM10
      { category: 'Groceries', amount: 300 }, // RM15
    ];
    const result = computeCombo(spend, [card]);

    expect(result.totalCashback).toBe(25); // RM25 < RM50 cap, no cap applied
    expect(result.cards[0].breakdown.every(b => b.cappedBy === 'none')).toBe(true);
  });
});

// ─────────────────────────────────────────────────────────────
// SPEC D — Annual Fee deduction
// ─────────────────────────────────────────────────────────────
describe('Rule: annualFee amortization', () => {
  it('D1: netCashback subtracts annualFee/12', () => {
    const card = makeCard({
      annualFee: 120,          // RM120/year = RM10/month
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Dining'],
          rate: 0.05,
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Dining', amount: 500 }];
    const result = computeCombo(spend, [card]);

    expect(result.totalCashback).toBe(25);        // 500 × 5%
    expect(result.monthlyFeeAmortized).toBe(10);  // 120/12
    expect(result.netCashback).toBe(15);          // 25 - 10
  });
});

// ─────────────────────────────────────────────────────────────
// SPEC E — Multi-card combo: greedy allocation
// ─────────────────────────────────────────────────────────────
describe('Rule: multi-card greedy allocation', () => {
  it('E1: allocates spend to card with highest rate first, then spills to 2nd', () => {
    // Card A: 10% on Petrol, cap RM30 (hits cap at RM300 spend)
    const cardA = makeCard({
      id: 'card-a',
      baseCashbackRate: 0.001,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol'],
          rate: 0.1,
          categoryCap: 30,  // RM30 cap → hits at RM300 spend
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    // Card B: 5% on Petrol, cap RM30
    const cardB = makeCard({
      id: 'card-b',
      baseCashbackRate: 0.001,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol'],
          rate: 0.05,
          categoryCap: 30,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    // User spends RM600 on Petrol
    const spend: SpendInput[] = [{ category: 'Petrol', amount: 600 }];
    const result = computeCombo(spend, [cardA, cardB]);

    // Card A: RM300 → RM30 cashback (hit categoryCap)
    // Card B: remaining RM300 → RM15 cashback
    // Total: RM45
    expect(result.totalCashback).toBe(45);
    const cA = result.cards.find(c => c.cardId === 'card-a');
    const cB = result.cards.find(c => c.cardId === 'card-b');
    expect(cA!.earnedCashback).toBe(30);
    expect(cB!.earnedCashback).toBe(15);
  });

  it('E2: isWeekendOnly card effective rate is halved', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Dining'],
          rate: 0.08,           // 8% but weekend only
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: true,  // ← 50% estimate applied
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Dining', amount: 500 }];
    const result = computeCombo(spend, [card]);

    // Effective rate = 8% × 0.5 = 4% → 500 × 4% = RM20
    expect(result.totalCashback).toBe(20);
    expect(result.cards[0].breakdown[0].rate).toBeCloseTo(0.04, 6);
  });
});

// ─────────────────────────────────────────────────────────────
// SPEC F — Edge cases
// ─────────────────────────────────────────────────────────────
describe('Edge cases', () => {
  it('F1: zero spend → zero cashback', () => {
    const card = makeCard({
      baseCashbackRate: 0.001,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol'],
          rate: 0.05,
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [];
    const result = computeCombo(spend, [card]);
    expect(result.totalCashback).toBe(0);
  });

  it('F2: spend in category not covered by any tier uses baseCashbackRate', () => {
    const card = makeCard({
      baseCashbackRate: 0.002,  // 0.2% base
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Petrol'],
          rate: 0.05,
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    // Spend on Airlines — not in any tier
    const spend: SpendInput[] = [{ category: 'Airlines', amount: 1000 }];
    const result = computeCombo(spend, [card]);

    // 1000 × 0.2% = RM2
    expect(result.totalCashback).toBeCloseTo(2, 4);
  });

  it('F3: rounding — cashback is rounded to 2 decimal places', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Dining'],
          rate: 0.03,     // 3%
          categoryCap: 0,
          poolCap: 0,
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Dining', amount: 333 }];
    const result = computeCombo(spend, [card]);
    // 333 × 3% = 9.99 → should be 9.99
    expect(result.totalCashback).toBe(9.99);
  });

  it('F4: categoryCap and poolCap both active — the lower limit wins', () => {
    const card = makeCard({
      baseCashbackRate: 0,
      tiers: [
        {
          minMonthlySpend: 0,
          categories: ['Groceries'],
          rate: 0.05,
          categoryCap: 10,  // RM10 per category
          poolCap: 5,       // RM5 pool — LOWER, wins
          isWeekendOnly: false,
        },
      ],
    });

    const spend: SpendInput[] = [{ category: 'Groceries', amount: 500 }];
    // Without caps: 500 × 5% = RM25. With poolCap RM5 < categoryCap RM10 → RM5
    const result = computeCombo(spend, [card]);
    expect(result.totalCashback).toBe(5);
    expect(result.cards[0].breakdown[0].cappedBy).toBe('poolCap');
  });
});
