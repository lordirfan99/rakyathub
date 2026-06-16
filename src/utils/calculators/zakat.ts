/**
 * Zakat Calculators — Simpanan, Emas, Fitrah
 *
 * Sources: JAKIM, Pusat Pungutan Zakat (PPZ), Lembaga Zakat Selangor
 * Last updated: 2026-06-16
 */

// ── Zakat Simpanan ──
// Source: PPZ — https://www.zakat.com.my
// Conditions:
// 1. Nisab: value of 85g gold (use live price or current estimate)
// 2. Haul: 1 year (354/365 days)
// 3. Rate: 2.5%
// 4. Only on savings ≥ nisab that have been held for 1 year
export function calculateZakatSimpanan(
  savingsBalance: number,
  nisabValue: number,
  daysHeld: number
): { eligible: number; zakatDue: number; isEligible: boolean; reason: string } {
  if (daysHeld < 354) {
    return {
      eligible: 0,
      zakatDue: 0,
      isEligible: false,
      reason: 'Belum cukup haul (perlu 354 hari / 1 tahun qamariah)',
    };
  }
  if (savingsBalance < nisabValue) {
    return {
      eligible: 0,
      zakatDue: 0,
      isEligible: false,
      reason: 'Baki simpanan kurang dari nisab (RM ' + nisabValue.toLocaleString() + ')',
    };
  }
  return {
    eligible: savingsBalance,
    zakatDue: Math.round(savingsBalance * 0.025 * 100) / 100,
    isEligible: true,
    reason: 'Layak — cukup haul dan melebihi nisab',
  };
}

// ── Zakat Emas ──
// Source: PPZ / JAKIM
// Rules:
// - Emas dipakai: uruf 800g (Selangor/PPZ standard) — zakat on excess only
// - Emas simpanan: 2.5% on total if ≥ nisab (85g)
// - Rate: 2.5%
export function calculateZakatEmas(
  totalGoldGrams: number,
  goldPricePerGram: number,
  goldType: 'pakai' | 'simpanan',
  urufGrams: number = 800
): {
  chargeableGrams: number;
  chargeableValue: number;
  zakatDue: number;
  note: string;
} {
  let chargeableGrams = totalGoldGrams;

  if (goldType === 'pakai') {
    chargeableGrams = Math.max(0, totalGoldGrams - urufGrams);
  }

  const chargeableValue = chargeableGrams * goldPricePerGram;
  const zakatDue = chargeableValue * 0.025;

  let note = '';
  if (chargeableGrams <= 0) {
    note = 'Tidak perlu bayar zakat — emas dipakai dalam lingkungan uruf (' + urufGrams + 'g)';
  } else {
    note = 'Zakat 2.5% atas ' + chargeableGrams + 'g emas (nilai RM ' + Math.round(chargeableValue).toLocaleString() + ')';
  }

  return {
    chargeableGrams: Math.round(chargeableGrams * 100) / 100,
    chargeableValue: Math.round(chargeableValue * 100) / 100,
    zakatDue: Math.round(zakatDue * 100) / 100,
    note,
  };
}

// ── Zakat Fitrah ──
// Source: JAKIM 2026 rates
// Varies by state and type of staple food
export const ZAKAT_FITRAH_RATES: Record<string, number> = {
  'Selangor': 15,
  'Kuala Lumpur': 15,
  'Putrajaya': 15,
  'Johor': 10,
  'Kedah': 10,
  'Kelantan': 10,
  'Melaka': 12,
  'Negeri Sembilan': 12,
  'Pahang': 12,
  'Perak': 12,
  'Perlis': 10,
  'Pulau Pinang': 14,
  'Sabah': 10,
  'Sarawak': 12,
  'Terengganu': 10,
};

export interface ZakatFitrahResult {
  perPerson: number;
  total: number;
  people: number;
  state: string;
}

export function calculateZakatFitrah(
  people: number,
  state: string,
  rateOverride?: number
): ZakatFitrahResult {
  const perPerson = rateOverride || ZAKAT_FITRAH_RATES[state] || 15;
  return {
    perPerson,
    total: perPerson * people,
    people,
    state,
  };
}
