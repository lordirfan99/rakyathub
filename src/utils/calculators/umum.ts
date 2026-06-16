/**
 * Umum / General Calculators — Age, Date Difference, Unit Converter
 */

// ── Age Calculator ──
export function calculateAge(birthDate: Date): {
  years: number;
  months: number;
  days: number;
  totalDays: number;
  nextBirthdayDays: number;
  zodiac: string;
} {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const birth = new Date(birthDate);
  birth.setHours(0, 0, 0, 0);

  const totalDays = Math.floor((now.getTime() - birth.getTime()) / (1000 * 60 * 60 * 24));

  let years = now.getFullYear() - birth.getFullYear();
  let months = now.getMonth() - birth.getMonth();
  let days = now.getDate() - birth.getDate();
  if (days < 0) { months--; days += new Date(now.getFullYear(), now.getMonth(), 0).getDate(); }
  if (months < 0) { years--; months += 12; }

  // Next birthday
  const nextBirthday = new Date(now.getFullYear(), birth.getMonth(), birth.getDate());
  if (nextBirthday <= now) nextBirthday.setFullYear(nextBirthday.getFullYear() + 1);
  const nextBirthdayDays = Math.ceil((nextBirthday.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

  // Chinese zodiac (simplified by year)
  const zodiacs = ['🐭 Tikus', '🐮 Kerbau', '🐯 Harimau', '🐰 Arnab', '🐲 Naga', '🐍 Ular', '🐴 Kuda', '🐑 Kambing', '🐵 Monyet', '🐔 Ayam', '🐶 Anjing', '🐷 Babi'];
  const zodiac = zodiacs[(birth.getFullYear() - 4) % 12];

  return { years, months, days, totalDays, nextBirthdayDays, zodiac };
}

// ── Date Difference ──
export function calculateDateDifference(date1: Date, date2: Date): {
  totalDays: number;
  totalWeeks: number;
  totalMonths: number;
  totalYears: number;
  workdays: number;
  weekends: number;
} {
  const d1 = new Date(Math.min(date1.getTime(), date2.getTime()));
  const d2 = new Date(Math.max(date1.getTime(), date2.getTime()));
  d1.setHours(0, 0, 0, 0);
  d2.setHours(0, 0, 0, 0);

  const diffMs = d2.getTime() - d1.getTime();
  const totalDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  // Count workdays (Mon-Fri) and weekends
  let workdays = 0;
  let weekends = 0;
  const current = new Date(d1);
  while (current <= d2) {
    const day = current.getDay();
    if (day === 0 || day === 6) weekends++;
    else workdays++;
    current.setDate(current.getDate() + 1);
  }

  return {
    totalDays,
    totalWeeks: Math.floor(totalDays / 7),
    totalMonths: Math.round(totalDays / 30.44),
    totalYears: Math.floor(totalDays / 365.25),
    workdays,
    weekends,
  };
}

// ── Unit Converter ──
export const UNIT_CATEGORIES: Record<string, {
  name: string;
  units: Array<{ id: string; label: string; toBase: (v: number) => number; fromBase: (v: number) => number }>;
}> = {
  length: {
    name: 'Panjang',
    units: [
      { id: 'mm', label: 'Milimeter (mm)', toBase: v => v / 1000, fromBase: v => v * 1000 },
      { id: 'cm', label: 'Sentimeter (cm)', toBase: v => v / 100, fromBase: v => v * 100 },
      { id: 'm', label: 'Meter (m)', toBase: v => v, fromBase: v => v },
      { id: 'km', label: 'Kilometer (km)', toBase: v => v * 1000, fromBase: v => v / 1000 },
      { id: 'in', label: 'Inci (in)', toBase: v => v * 0.0254, fromBase: v => v / 0.0254 },
      { id: 'ft', label: 'Kaki (ft)', toBase: v => v * 0.3048, fromBase: v => v / 0.3048 },
    ],
  },
  weight: {
    name: 'Berat',
    units: [
      { id: 'mg', label: 'Miligram (mg)', toBase: v => v / 1000000, fromBase: v => v * 1000000 },
      { id: 'g', label: 'Gram (g)', toBase: v => v / 1000, fromBase: v => v * 1000 },
      { id: 'kg', label: 'Kilogram (kg)', toBase: v => v, fromBase: v => v },
      { id: 'ton', label: 'Ton', toBase: v => v * 1000, fromBase: v => v / 1000 },
      { id: 'oz', label: 'Auns (oz)', toBase: v => v * 0.0283495, fromBase: v => v / 0.0283495 },
      { id: 'lb', label: 'Paun (lb)', toBase: v => v * 0.453592, fromBase: v => v / 0.453592 },
    ],
  },
  temperature: {
    name: 'Suhu',
    units: [
      { id: 'c', label: 'Celsius (°C)', toBase: v => v, fromBase: v => v },
      { id: 'f', label: 'Fahrenheit (°F)', toBase: v => (v - 32) * 5/9, fromBase: v => v * 9/5 + 32 },
      { id: 'k', label: 'Kelvin (K)', toBase: v => v, fromBase: v => v },
    ],
  },
  volume: {
    name: 'Isipadu',
    units: [
      { id: 'ml', label: 'Mililiter (ml)', toBase: v => v / 1000, fromBase: v => v * 1000 },
      { id: 'l', label: 'Liter (L)', toBase: v => v, fromBase: v => v },
      { id: 'gal', label: 'Gelen (gal)', toBase: v => v * 3.78541, fromBase: v => v / 3.78541 },
    ],
  },
  area: {
    name: 'Luas',
    units: [
      { id: 'sqm', label: 'Meter persegi (m²)', toBase: v => v, fromBase: v => v },
      { id: 'sqft', label: 'Kaki persegi (ft²)', toBase: v => v * 0.092903, fromBase: v => v / 0.092903 },
      { id: 'hektar', label: 'Hektar', toBase: v => v * 10000, fromBase: v => v / 10000 },
      { id: 'ekar', label: 'Ekar', toBase: v => v * 4046.86, fromBase: v => v / 4046.86 },
    ],
  },
};
