/**
 * Miles/Points Calculation Engine
 * Calculates how many KrisFlyer/Enrich miles/points a card earns
 * given a spending profile.
 */

import type { MileCard, MileCardTier } from '~/data/mile-cards';

export interface SpendInput {
  category: string;
  amount: number;
}

export interface CardMileResult {
  cardId: string;
  cardName: string;
  bank: string;
  totalMiles: number;
  breakdown: { category: string; spend: number; rate: number; miles: number }[];
  annualFee: number;
  monthlyFee: number;
  netMilesMonthly: number;
}

export function calculateMiles(
  spend: SpendInput[],
  card: MileCard,
): CardMileResult {
  let totalMiles = 0;
  const breakdown: { category: string; spend: number; rate: number; miles: number }[] = [];

  for (const { category, amount } of spend) {
    if (amount <= 0) continue;

    // Find best tier for this category
    let bestRate = card.earnRate;
    let bestTier: MileCardTier | null = null;

    for (const tier of card.tiers) {
      if (tier.categories.includes(category)) {
        const rate = tier.isWeekendOnly ? tier.earnRate * 0.5 : tier.earnRate;
        if (rate > bestRate) {
          bestRate = rate;
          bestTier = tier;
        }
      }
    }

    const miles = amount * bestRate;
    totalMiles += miles;
    breakdown.push({ category, spend: amount, rate: bestRate, miles });
  }

  const monthlyFee = card.annualFee / 12;

  return {
    cardId: card.id,
    cardName: card.cardName,
    bank: card.bank,
    totalMiles: Math.round(totalMiles * 100) / 100,
    breakdown,
    annualFee: card.annualFee,
    monthlyFee: Math.round(monthlyFee * 100) / 100,
    netMilesMonthly: Math.round((totalMiles - monthlyFee) * 100) / 100,
  };
}

export function calculateAllCards(
  spend: SpendInput[],
  cards: MileCard[],
  program: 'krisflyer' | 'enrich',
): CardMileResult[] {
  const results: CardMileResult[] = [];

  for (const card of cards) {
    if (card.program === program || card.program === 'both') {
      const result = calculateMiles(spend, card);
      results.push(result);
    }
  }

  results.sort((a, b) => b.netMilesMonthly - a.netMilesMonthly);
  return results;
}
