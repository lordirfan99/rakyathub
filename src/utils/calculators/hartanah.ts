/**
 * Hartanah / Property Calculators — Pure calculation functions
 *
 * Sources cited in each function. See src/utils/calculators/config/hartanah.ts
 * for rate tables and constants.
 */

import {
  MOT_STAMP_DUTY_TIERS,
  LOAN_STAMP_DUTY_RATE,
  LEGAL_FEE_TIERS,
  DISBURSEMENTS,
} from './config/hartanah';

// ── Stamp Duty: MOT (Property Transfer) ──
// Source: LHDN Stamp Duty Act 1949 — First Schedule
export function calculateMOTStampDuty(propertyPrice: number): number {
  let remaining = propertyPrice;
  let total = 0;
  let prevMax = 0;

  for (const tier of MOT_STAMP_DUTY_TIERS) {
    const bracket = Math.min(remaining, tier.max - prevMax);
    if (bracket <= 0) break;
    total += bracket * tier.rate;
    remaining -= bracket;
    prevMax = tier.max;
    if (remaining <= 0) break;
  }

  return Math.round(total);
}

// ── Loan Agreement Stamp Duty ──
// Source: LHDN — 0.5% of loan amount
export function calculateLoanStampDuty(loanAmount: number): number {
  return Math.round(loanAmount * LOAN_STAMP_DUTY_RATE);
}

// ── Legal Fees (Scale Rate) ──
// Source: Solicitors' Remuneration Order 2023
export function calculateLegalFees(amount: number): number {
  let remaining = amount;
  let total = 0;
  let prevMax = 0;

  for (const tier of LEGAL_FEE_TIERS) {
    const bracket = Math.min(remaining, tier.max - prevMax);
    if (bracket <= 0) break;
    total += bracket * tier.rate;
    remaining -= bracket;
    prevMax = tier.max;
    if (remaining <= 0) break;
  }

  return Math.round(total);
}

// ── Total Disbursements ──
export function calculateDisbursements(): number {
  return Object.values(DISBURSEMENTS).reduce((sum, v) => sum + v, 0);
}

// ── Monthly Loan Payment (Reducing Balance) ──
// Standard amortization formula
export function calculateMonthlyPayment(
  loanAmount: number,
  annualRatePct: number,
  years: number
): number {
  const monthlyRate = (annualRatePct / 100) / 12;
  const months = years * 12;
  if (monthlyRate === 0) return Math.round(loanAmount / months);
  const factor = Math.pow(1 + monthlyRate, months);
  return Math.round(loanAmount * (monthlyRate * factor) / (factor - 1));
}

// ── Remaining Loan Balance after N months ──
export function calculateRemainingBalance(
  loanAmount: number,
  annualRatePct: number,
  monthlyPayment: number,
  monthsPaid: number
): number {
  const monthlyRate = (annualRatePct / 100) / 12;
  let balance = loanAmount;
  for (let m = 0; m < monthsPaid; m++) {
    if (balance <= 0) break;
    const interest = balance * monthlyRate;
    const principal = monthlyPayment - interest;
    balance -= principal;
    if (balance < 0) balance = 0;
  }
  return Math.round(balance);
}
