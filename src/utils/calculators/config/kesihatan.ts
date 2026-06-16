/**
 * Kesihatan Calculator Config — Rates, constants, and category definitions.
 *
 * Source: WHO, MOH Malaysia, CDC, NIDDK
 * Last updated: 2026-06-16
 */

// ── BMI Categories (WHO) ──
// Source: https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight
export const BMI_WHO = {
  underweight: { max: 18.4, label: 'Kurang Berat Badan' },
  normal: { min: 18.5, max: 24.9, label: 'Berat Normal' },
  overweight: { min: 25.0, max: 29.9, label: 'Berat Berlebihan' },
  obeseI: { min: 30.0, max: 34.9, label: 'Obesiti Kelas I' },
  obeseII: { min: 35.0, max: 39.9, label: 'Obesiti Kelas II' },
  obeseIII: { min: 40.0, max: Infinity, label: 'Obesiti Kelas III' },
} as const;

// BMI Categories (Asian — WHO-recommended lower thresholds for Asian populations)
// Source: WHO Expert Consultation 2004 — https://doi.org/10.1016/S0140-6736(04)16352-8
export const BMI_ASIAN = {
  underweight: { max: 18.4, label: 'Kurang Berat Badan' },
  normal: { min: 18.5, max: 22.9, label: 'Berat Normal' },
  overweight: { min: 23.0, max: 27.4, label: 'Berat Berlebihan' },
  obeseI: { min: 27.5, max: 32.4, label: 'Obesiti Kelas I' },
  obeseII: { min: 32.5, max: 37.4, label: 'Obesiti Kelas II' },
  obeseIII: { min: 37.5, max: Infinity, label: 'Obesiti Kelas III' },
} as const;

// ── BMR Formulas ──
// Source: Mifflin MD, St Jeor ST, et al. 1990 — https://pubmed.ncbi.nlm.nih.gov/2305711/
export const BMR_CONSTANTS = {
  mifflinStJeor: {
    male: { weight: 10, height: 6.25, age: 5, constant: 5 },
    female: { weight: 10, height: 6.25, age: 5, constant: -161 },
  },
} as const;

// ── Activity Level Multipliers (for TDEE) ──
// Source: National Health Service UK — https://www.nhs.uk/live-well/
export const ACTIVITY_LEVELS = [
  { value: 1.2, label: 'Tidak Aktif', desc: 'Kerja meja, langsung tiada senaman' },
  { value: 1.375, label: 'Ringan', desc: 'Senaman ringan 1-3 hari/minggu' },
  { value: 1.55, label: 'Sederhana', desc: 'Senaman sederhana 3-5 hari/minggu' },
  { value: 1.725, label: 'Aktif', desc: 'Senaman berat 6-7 hari/minggu' },
  { value: 1.9, label: 'Sangat Aktif', desc: 'Senaman berat + kerja fizikal' },
] as const;

// ── Ideal Weight (Devine formula) ──
// Source: Devine BJ, 1974 — Drug Intelligence & Clinical Pharmacy
// Note: Original formula uses inches. Adapted for cm here.
export const DEVINE_FORMULA = {
  // For first 152.4cm (5ft): base weight
  // For each additional 2.54cm (1in): add per cm
  baseMale: 50,       // kg for 152.4cm
  baseFemale: 45.5,   // kg for 152.4cm
  perCmOver: { male: 0.9, female: 0.9 },  // kg per cm above 152.4cm
} as const;

// ── Pregnancy Due Date ──
// Source: Naegele's Rule — standard obstetric calculation
// Gestational age: 280 days (40 weeks) from LMP
export const PREGNANCY = {
  gestationalDays: 280,
  gestationalWeeks: 40,
  trimesters: [
    { name: 'Trimester 1', weekStart: 1, weekEnd: 13 },
    { name: 'Trimester 2', weekStart: 14, weekEnd: 26 },
    { name: 'Trimester 3', weekStart: 27, weekEnd: 40 },
  ],
} as const;
