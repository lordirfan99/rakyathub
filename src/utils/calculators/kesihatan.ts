/**
 * Kesihatan Calculators — Pure calculation functions
 *
 * These are the source-of-truth formulas. Each calculator page embeds
 * its own copy of the relevant function in <script is:inline> with
 * a comment pointing back to this file.
 *
 * Sources cited in each function.
 */

// ── BMI ──
// Formula: weight (kg) / [height (m)]²
// Source: WHO — https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight
export function calculateBMI(weightKg: number, heightCm: number): number {
  const heightM = heightCm / 100;
  return weightKg / (heightM * heightM);
}

// ── BMR (Mifflin-St Jeor) ──
// Source: Mifflin MD, St Jeor ST, et al. 1990 — https://pubmed.ncbi.nlm.nih.gov/2305711/
export function calculateBMR(
  weightKg: number,
  heightCm: number,
  age: number,
  isMale: boolean
): number {
  if (isMale) {
    return 10 * weightKg + 6.25 * heightCm - 5 * age + 5;
  }
  return 10 * weightKg + 6.25 * heightCm - 5 * age - 161;
}

// ── TDEE (Total Daily Energy Expenditure) ──
// BMR × activity multiplier
// Source: National Health Service UK
export function calculateTDEE(bmr: number, activityMultiplier: number): number {
  return bmr * activityMultiplier;
}

// ── Ideal Weight (Devine formula, adapted for cm) ──
// Source: Devine BJ, 1974
export function calculateIdealWeight(heightCm: number, isMale: boolean): number {
  const base = isMale ? 50 : 45.5;
  const excessCm = Math.max(0, heightCm - 152.4);
  return base + excessCm * 0.9;
}

// ── Pregnancy Due Date (Naegele's Rule) ──
// LMP + 280 days (40 weeks)
// Source: Naegele's Rule — standard obstetric calculation
export function calculateDueDate(lmpDate: Date): Date {
  const due = new Date(lmpDate);
  due.setDate(due.getDate() + 280);
  return due;
}

// ── Current Gestational Age ──
export function calculateGestationalAge(lmpDate: Date): {
  weeks: number;
  days: number;
  trimester: number;
  progressPct: number;
} {
  const now = new Date();
  const diffMs = now.getTime() - lmpDate.getTime();
  const totalDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const weeks = Math.floor(totalDays / 7);
  const days = totalDays % 7;

  let trimester = 1;
  if (weeks >= 14) trimester = 2;
  if (weeks >= 27) trimester = 3;

  const progressPct = Math.min(100, Math.round((totalDays / 280) * 100));

  return { weeks, days, trimester, progressPct };
}
