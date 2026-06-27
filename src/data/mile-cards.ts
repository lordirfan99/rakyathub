// Malaysian Miles/Points Card Database — KrisFlyer & Enrich
// Schema version 1.0
// Rates sourced from publicly available bank websites as of Q2 2025

export interface MileCardTier {
  categories: string[];        // Spending categories that earn at this rate
  earnRate: number;            // Miles/points per RM1 spent
  categoryCap: number;         // Max miles/points per category per month (0 = unlimited)
  poolCap: number;             // Max miles/points across all categories (0 = unlimited)
  minMonthlySpend: number;     // Spend required to unlock this tier
  isWeekendOnly: boolean;      // Only on weekends
}

export interface MileCard {
  id: string;
  bank: string;
  cardName: string;
  program: 'krisflyer' | 'enrich' | 'both';
  hexColor: string;
  imageUrl?: string;
  network: 'Visa' | 'Mastercard' | 'Amex' | 'UnionPay';
  minIncome: number;
  annualFee: number;
  feeWaiverCondition: string;
  earnRate: number;            // Base earn rate (miles/points per RM1)
  tiers: MileCardTier[];
  foreignRate: number;         // Overseas earn rate
}

export const CATEGORIES = [
  'Petrol', 'Groceries', 'Dining', 'Online Shopping',
  'Utilities', 'Entertainment', 'Pharmacy', 'Airlines',
  'Telco', 'Education', 'Insurance', 'Hospital',
  'Government', 'eWallet', 'Others',
] as const;

export type Category = (typeof CATEGORIES)[number];

// Spend categories as used by UI input IDs
export const CAT_ID: Record<string, string> = {
  'Petrol': 'petrol', 'Groceries': 'groceries', 'Dining': 'dining',
  'Online Shopping': 'online', 'Utilities': 'utilities', 'Entertainment': 'entertainment',
  'Pharmacy': 'pharmacy', 'Airlines': 'airlines', 'Telco': 'telco',
  'Education': 'education', 'Insurance': 'insurance', 'Hospital': 'hospital',
  'Government': 'government', 'eWallet': 'ewallet', 'Others': 'others',
};

export const MILE_CARDS: MileCard[] = [
  // ── KRISFLYER CARDS ─────────────────────────────────

  // Maybank 2 Cards (Amex) — can convert to KrisFlyer
  {
    id: 'maybank-2-amex-kf',
    bank: 'Maybank',
    cardName: 'Maybank 2 Amex (KrisFlyer)',
    program: 'krisflyer',
    hexColor: '#E6B800',
    network: 'Amex',
    minIncome: 36000,
    annualFee: 0,
    feeWaiverCondition: 'Gratis selamanya',
    earnRate: 0.5,
    foreignRate: 0.5,
    tiers: [
      {
        categories: ['Petrol', 'Groceries', 'Dining', 'Online Shopping', 'Utilities', 'Entertainment'],
        earnRate: 5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Others'],
        earnRate: 0.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // CIMB Visa Signature — KrisFlyer
  {
    id: 'cimb-visa-sig-kf',
    bank: 'CIMB',
    cardName: 'CIMB Visa Signature (KrisFlyer)',
    program: 'krisflyer',
    hexColor: '#E31837',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 690,
    feeWaiverCondition: 'Waived with annual spend RM30,000',
    earnRate: 1,
    foreignRate: 2,
    tiers: [
      {
        categories: ['Online Shopping', 'Entertainment', 'Airlines'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // SCB Visa Infinite — KrisFlyer
  {
    id: 'scb-vi-kf',
    bank: 'Standard Chartered',
    cardName: 'SCB Visa Infinite (KrisFlyer)',
    program: 'krisflyer',
    hexColor: '#003D7A',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1088,
    feeWaiverCondition: 'Waived with RM100,000 annual spend',
    earnRate: 1.5,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Petrol', 'Dining', 'Groceries', 'Online Shopping'],
        earnRate: 2.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // UOB PRVI Miles — KrisFlyer
  {
    id: 'uob-prvi',
    bank: 'UOB',
    cardName: 'UOB PRVI Miles',
    program: 'krisflyer',
    hexColor: '#0057B8',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 675,
    feeWaiverCondition: 'Waived with RM60,000 annual spend',
    earnRate: 1,
    foreignRate: 2.5,
    tiers: [
      {
        categories: ['Online Shopping', 'Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // HSBC Amanah Visa Infinite — KrisFlyer
  {
    id: 'hsbc-amanah-vi-kf',
    bank: 'HSBC Amanah',
    cardName: 'HSBC Amanah Visa Infinite',
    program: 'krisflyer',
    hexColor: '#DB0011',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1080,
    feeWaiverCondition: 'Waived with RM100,000 annual spend',
    earnRate: 1,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Dining', 'Online Shopping', 'Entertainment', 'Airlines'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // Alliance Visa Infinite — KrisFlyer
  {
    id: 'alliance-vi-kf',
    bank: 'Alliance Bank',
    cardName: 'Alliance Visa Infinite (KrisFlyer)',
    program: 'krisflyer',
    hexColor: '#004B87',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1088,
    feeWaiverCondition: 'Waived with RM100,000 annual spend',
    earnRate: 1,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Dining', 'Online Shopping', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Petrol', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // OCBC Voyage — KrisFlyer
  {
    id: 'ocbc-voyage',
    bank: 'OCBC',
    cardName: 'OCBC Voyage',
    program: 'krisflyer',
    hexColor: '#004B8D',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1088,
    feeWaiverCondition: 'Waived with RM120,000 annual spend',
    earnRate: 1,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Airlines', 'Online Shopping', 'Entertainment'],
        earnRate: 3.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // ── ENRICH CARDS ──────────────────────────────────

  // CIMB Enrich Visa Signature
  {
    id: 'cimb-enrich-visa-sig',
    bank: 'CIMB',
    cardName: 'CIMB Enrich Visa Signature',
    program: 'enrich',
    hexColor: '#E31837',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 590,
    feeWaiverCondition: 'Waived with RM30,000 annual spend',
    earnRate: 1,
    foreignRate: 2,
    tiers: [
      {
        categories: ['Online Shopping', 'Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // AmBank Enrich Visa Infinite
  {
    id: 'ambank-enrich-vi',
    bank: 'AmBank',
    cardName: 'AmBank Enrich Visa Infinite',
    program: 'enrich',
    hexColor: '#E3000F',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1088,
    feeWaiverCondition: 'Waived with RM120,000 annual spend',
    earnRate: 1,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Dining', 'Online Shopping', 'Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Petrol', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // RHB Enrich Visa Signature
  {
    id: 'rhb-enrich-visa-sig',
    bank: 'RHB',
    cardName: 'RHB Enrich Visa Signature',
    program: 'enrich',
    hexColor: '#005BAA',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 590,
    feeWaiverCondition: 'Waived with RM30,000 annual spend',
    earnRate: 1,
    foreignRate: 2,
    tiers: [
      {
        categories: ['Online Shopping', 'Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // SCB Enrich Visa Infinite
  {
    id: 'scb-enrich-vi',
    bank: 'Standard Chartered',
    cardName: 'SCB Enrich Visa Infinite',
    program: 'enrich',
    hexColor: '#003D7A',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1088,
    feeWaiverCondition: 'Waived with RM100,000 annual spend',
    earnRate: 1.5,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Petrol', 'Dining', 'Groceries', 'Online Shopping'],
        earnRate: 2.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // Public Bank Enrich Visa Signature
  {
    id: 'pb-enrich-visa-sig',
    bank: 'Public Bank',
    cardName: 'PB Enrich Visa Signature',
    program: 'enrich',
    hexColor: '#F47920',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 590,
    feeWaiverCondition: 'Waived with RM40,000 annual spend',
    earnRate: 1,
    foreignRate: 2,
    tiers: [
      {
        categories: ['Online Shopping', 'Entertainment', 'Airlines'],
        earnRate: 2.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 1.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // HSBC Amanah Enrich Visa Infinite
  {
    id: 'hsbc-enrich-vi',
    bank: 'HSBC Amanah',
    cardName: 'HSBC Amanah Enrich Visa Infinite',
    program: 'enrich',
    hexColor: '#DB0011',
    network: 'Visa',
    minIncome: 120000,
    annualFee: 1080,
    feeWaiverCondition: 'Waived with RM100,000 annual spend',
    earnRate: 1,
    foreignRate: 3,
    tiers: [
      {
        categories: ['Dining', 'Online Shopping', 'Entertainment', 'Airlines'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // UOB PRVI Miles — also Enrich
  {
    id: 'uob-prvi-enrich',
    bank: 'UOB',
    cardName: 'UOB PRVI Miles (Enrich)',
    program: 'enrich',
    hexColor: '#0057B8',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 675,
    feeWaiverCondition: 'Waived with RM60,000 annual spend',
    earnRate: 1,
    foreignRate: 2.5,
    tiers: [
      {
        categories: ['Online Shopping', 'Airlines', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries'],
        earnRate: 2,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },

  // ── GENERAL MILES CARDS ────────────────────────────
  // RHB Travel & Miles (convertible to both)
  {
    id: 'rhb-travel-miles',
    bank: 'RHB',
    cardName: 'RHB Travel & Miles',
    program: 'both',
    hexColor: '#005BAA',
    network: 'Visa',
    minIncome: 60000,
    annualFee: 675,
    feeWaiverCondition: 'Waived with RM40,000 annual spend',
    earnRate: 1,
    foreignRate: 2.5,
    tiers: [
      {
        categories: ['Airlines', 'Online Shopping', 'Entertainment'],
        earnRate: 3,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
      {
        categories: ['Dining', 'Groceries', 'Petrol'],
        earnRate: 1.5,
        categoryCap: 0,
        poolCap: 0,
        minMonthlySpend: 0,
        isWeekendOnly: false,
      },
    ],
  },
];
