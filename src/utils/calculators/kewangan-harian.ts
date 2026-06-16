/**
 * Kewangan Harian Calculators — Pure functions
 *
 * Discount, Tip/Bill Split, Compound Interest, Currency
 */

// ── Discount Calculator ──
export function calculateDiscountedPrice(originalPrice: number, discountPct: number): {
  discountAmount: number;
  finalPrice: number;
  savingsPct: number;
} {
  const discountAmount = originalPrice * (discountPct / 100);
  return {
    discountAmount: Math.round(discountAmount * 100) / 100,
    finalPrice: Math.round((originalPrice - discountAmount) * 100) / 100,
    savingsPct: discountPct,
  };
}

// ── Tip Split ──
export function calculateBillSplit(
  billAmount: number,
  tipPct: number,
  people: number
): {
  tipAmount: number;
  totalWithTip: number;
  perPerson: number;
} {
  const tipAmount = billAmount * (tipPct / 100);
  const totalWithTip = billAmount + tipAmount;
  return {
    tipAmount: Math.round(tipAmount * 100) / 100,
    totalWithTip: Math.round(totalWithTip * 100) / 100,
    perPerson: Math.round((totalWithTip / people) * 100) / 100,
  };
}

// ── Compound Interest ──
export function calculateCompoundInterest(
  principal: number,
  monthlyTopUp: number,
  annualRatePct: number,
  years: number,
  compoundPerYear: number = 12
): {
  totalInvested: number;
  totalInterest: number;
  finalValue: number;
  yearlyBreakdown: Array<{ year: number; invested: number; interest: number; balance: number }>;
} {
  const ratePerPeriod = (annualRatePct / 100) / compoundPerYear;
  const totalPeriods = years * compoundPerYear;
  let balance = principal;
  const yearlyData = [];

  for (let y = 1; y <= years; y++) {
    const startYearBalance = balance;
    let yearInterest = 0;

    for (let m = 1; m <= compoundPerYear; m++) {
      const interestThisPeriod = balance * ratePerPeriod;
      yearInterest += interestThisPeriod;
      balance += interestThisPeriod;
      if (monthlyTopUp > 0 && (y - 1) * compoundPerYear + m < totalPeriods) {
        balance += monthlyTopUp;
      }
    }

    const totalInvestedSoFar = principal + monthlyTopUp * compoundPerYear * y;
    yearlyData.push({
      year: y,
      invested: Math.round(totalInvestedSoFar),
      interest: Math.round(yearInterest),
      balance: Math.round(balance),
    });
  }

  const totalMonthlyTopUp = monthlyTopUp * compoundPerYear * years;
  const totalInvested = principal + totalMonthlyTopUp;

  return {
    totalInvested: Math.round(totalInvested),
    totalInterest: Math.round(balance - totalInvested),
    finalValue: Math.round(balance),
    yearlyBreakdown: yearlyData,
  };
}

// ── Currency Reference Rates (for fallback) ──
// Source: Bank Negara Malaysia (BNM) — https://www.bnm.gov.my/exchangerates
// Last updated: 2026-06-16
export const REFERENCE_RATES: Record<string, number> = {
  'USD/MYR': 4.45,
  'SGD/MYR': 3.30,
  'THB/MYR': 0.122,
  'IDR/MYR': 0.000275,
  'CNY/MYR': 0.615,
  'JPY/MYR': 0.028,
  'GBP/MYR': 5.68,
  'EUR/MYR': 4.82,
  'AUD/MYR': 2.97,
  'KRW/MYR': 0.00325,
  'INR/MYR': 0.0535,
  'GBP/USD': 1.27,
  'EUR/USD': 1.08,
  'USD/JPY': 157.5,
  'GBP/EUR': 1.18,
};
