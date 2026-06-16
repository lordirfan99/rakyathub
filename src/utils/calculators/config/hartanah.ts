/**
 * Hartanah / Property Calculator Config — Rates, tiers, and constants.
 *
 * Sources: LHDN Stamp Duty Act 1949, Solicitors' Remuneration Order 2023, BNM
 * Last updated: 2026-06-16
 */

// ── MOT (Memorandum of Transfer) Stamp Duty ──
// Source: LHDN Stamp Duty Act 1949 — First Schedule
// https://www.hasil.gov.my/en/stamp-duty/
export const MOT_STAMP_DUTY_TIERS = [
  { max: 100000, rate: 0.01 },     // 1% — first RM100k
  { max: 500000, rate: 0.02 },     // 2% — RM100k–RM500k
  { max: 1000000, rate: 0.03 },    // 3% — RM500k–RM1M
  { max: Infinity, rate: 0.04 },   // 4% — above RM1M
] as const;

// ── Loan Agreement Stamp Duty ──
// Source: LHDN — 0.5% of total loan amount
export const LOAN_STAMP_DUTY_RATE = 0.005; // 0.5%

// ── S&P Legal Fees (Solicitors' Remuneration Order 2023) ──
// Source: Solicitors' Remuneration Order 2023 — PU(A) 33/2023
// Scale applies to property price OR loan amount
export const LEGAL_FEE_TIERS = [
  { max: 500000, rate: 0.01 },       // 1% — first RM500k
  { max: 1000000, rate: 0.008 },     // 0.8% — next RM500k
  { max: 3000000, rate: 0.007 },     // 0.7% — next RM2M
  { max: 5000000, rate: 0.006 },     // 0.6% — next RM2M
  { max: 7500000, rate: 0.005 },     // 0.5% — next RM2.5M
  { max: Infinity, rate: 0.005 },    // negotiated — capped at 0.5%
] as const;

// ── Estimated Disbursements ──
// Non-exhaustive; varies by lawyer and location
export const DISBURSEMENTS = {
  landSearch: 60,          // RM — land search fee
  registration: 100,       // RM — registration of transfer
  bankruptcySearch: 30,    // RM — bankruptcy search
  copyDoc: 60,             // RM — copy documents
  miscellaneous: 300,      // RM — miscellaneous (transport, postage, etc.)
} as const;

// ── Estimated Valuation Fee ──
// Source: Board of Valuers, Appraisers, Estate Agents & Property Managers Malaysia
// Simplified: ~0.25% for first RM100k, lower for higher values
export const VALUATION_FEE_TIERS = [
  { max: 100000, rate: 0.0025 },
  { max: 2000000, rate: 0.002 },
  { max: Infinity, rate: 0.0015 },
] as const;

// ── First-Time Buyer Exemption (Budget 2025/2026) ──
// MOT exemption on first RM300,000 for first-time buyers
// Property price must not exceed RM500,000
export const FTB_EXEMPTION = {
  motExemptionMax: 300000,  // First RM300k MOT exempt
  maxPropertyPrice: 500000,  // Property must be ≤ RM500k
} as const;
