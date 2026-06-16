/**
 * Kenderaan Calculators — Road Tax (JPJ), Fuel Cost
 *
 * Sources: JPJ (Jabatan Pengangkutan Jalan), Kementerian Pengangkutan Malaysia
 * Last updated: 2026-06-16
 */

// ── Road Tax (Annual) — Private Cars ──
// Source: JPJ Malaysia — https://www.jpj.gov.my/
// Peninsular Malaysia rates
export const ROAD_TAX_PRIVATE_CAR: Array<{ maxCC: number; rate: number }> = [
  { maxCC: 1000, rate: 20 },
  { maxCC: 1200, rate: 55 },
  { maxCC: 1400, rate: 70 },
  { maxCC: 1600, rate: 90 },
  { maxCC: 1800, rate: 150 },
  { maxCC: 2000, rate: 200 },
  { maxCC: 2500, rate: 300 },
  { maxCC: 3000, rate: 450 },
  { maxCC: Infinity, rate: -1 }, // -1 means use progressive formula
];

// For engine > 3000cc: base RM450 + RM5 per cc above 3000cc (Peninsular)
export const ROAD_TAX_ABOVE_3000_BASE = 450;
export const ROAD_TAX_ABOVE_3000_RATE = 5; // per cc

// Sabah & Sarawak rates (lower)
export const ROAD_TAX_SABAH_ABOVE_3000_BASE = 225;
export const ROAD_TAX_SABAH_ABOVE_3000_RATE = 2.5; // per cc

// Sabah/Sarawak private car rates
export const ROAD_TAX_SABAH_CAR: Array<{ maxCC: number; rate: number }> = [
  { maxCC: 1000, rate: 10 },
  { maxCC: 1200, rate: 27.50 },
  { maxCC: 1400, rate: 35 },
  { maxCC: 1600, rate: 45 },
  { maxCC: 1800, rate: 75 },
  { maxCC: 2000, rate: 100 },
  { maxCC: 2500, rate: 150 },
  { maxCC: 3000, rate: 225 },
  { maxCC: Infinity, rate: -1 },
];

// ── Fuel Cost ──
// Source: Kementerian Kewangan Malaysia (subsidised RON95 price)
// Last updated: 2026-06-16
export const FUEL_PRICES = {
  RON95: 2.05,    // RM/litre — subsidised
  RON97: 3.35,    // RM/litre — float
  Diesel: 2.15,   // RM/litre — subsidised
} as const;

// Average fuel consumption by vehicle type (km/litre)
export const AVG_CONSUMPTION = {
  'Myvi/Kecil': { city: 18, highway: 22 },
  'Sedan Sederhana': { city: 14, highway: 18 },
  'SUV/MPV': { city: 10, highway: 13 },
  'Pickup/Truck': { city: 9, highway: 12 },
  'Motosikal <150cc': { city: 40, highway: 45 },
  'Motosikal >150cc': { city: 25, highway: 30 },
} as const;

export function calculateRoadTax(cc: number, region: 'peninsular' | 'sabah_sarawak'): number {
  const table = region === 'peninsular' ? ROAD_TAX_PRIVATE_CAR : ROAD_TAX_SABAH_CAR;

  for (const tier of table) {
    if (cc <= tier.maxCC) {
      if (tier.rate >= 0) return tier.rate;
      // Above 3000cc formula
      if (region === 'peninsular') {
        return ROAD_TAX_ABOVE_3000_BASE + (cc - 3000) * ROAD_TAX_ABOVE_3000_RATE;
      }
      return ROAD_TAX_SABAH_ABOVE_3000_BASE + (cc - 3000) * ROAD_TAX_SABAH_ABOVE_3000_RATE;
    }
  }
  return 0;
}

export function calculateFuelCost(
  distanceKm: number,
  consumptionKmPerLitre: number,
  fuelPricePerLitre: number,
  tripsPerMonth: number
): {
  litresNeeded: number;
  costPerTrip: number;
  costPerMonth: number;
} {
  const litresPerTrip = distanceKm / consumptionKmPerLitre;
  const costPerTrip = litresPerTrip * fuelPricePerLitre;
  return {
    litresNeeded: Math.round(litresPerTrip * 100) / 100,
    costPerTrip: Math.round(costPerTrip * 100) / 100,
    costPerMonth: Math.round(costPerTrip * tripsPerMonth * 100) / 100,
  };
}
