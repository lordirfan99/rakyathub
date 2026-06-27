// Enrich Points Redemption Library — Malaysia Airlines destinations
// Rates sourced from Malaysia Airlines Enrich portal as of Q2 2025

export interface EnrichDestination {
  city: string;
  country: string;
  zone: string;
  economySaver: number;   // Enrich points for Economy Saver (one-way)
  businessSaver: number;   // Enrich points for Business Saver (one-way)
  economyFlex: number;     // Enrich points for Economy Flex (one-way)
  businessFlex: number;    // Enrich points for Business Flex (one-way)
}

export const ENRICH_ZONES = [
  { id: 'asean', label: 'ASEAN' },
  { id: 'asia', label: 'Asia' },
  { id: 'china', label: 'China & Greater China' },
  { id: 'india', label: 'Indian Subcontinent' },
  { id: 'middle-east', label: 'Middle East' },
  { id: 'australia', label: 'Australia & New Zealand' },
  { id: 'europe', label: 'Europe' },
  { id: 'north-america', label: 'North America' },
] as const;

export const ENRICH_PARTNERS = [
  { airline: 'Malaysia Airlines', code: 'MH' },
  { airline: 'Air Mauritius', code: 'MK' },
  { airline: 'Bangkok Airways', code: 'PG' },
  { airline: 'Ethiopian Airlines', code: 'ET' },
  { airline: 'Firefly', code: 'FY' },
  { airline: 'Garuda Indonesia', code: 'GA' },
  { airline: 'Japan Airlines', code: 'JL' },
  { airline: 'Korean Air', code: 'KE' },
  { airline: 'Philippine Airlines', code: 'PR' },
  { airline: 'Royal Brunei Airlines', code: 'BI' },
  { airline: 'SriLankan Airlines', code: 'UL' },
  { airline: 'Thai AirAsia', code: 'FD' },
  { airline: 'Turkish Airlines', code: 'TK' },
  { airline: 'Vietnam Airlines', code: 'VN' },
  { airline: 'Air France / KLM', code: 'AF/KL' },
] as const;

export const DESTINATIONS: EnrichDestination[] = [
  // ── ASEAN ──
  { city: 'Kuala Lumpur', country: 'Malaysia', zone: 'asean', economySaver: 0, businessSaver: 0, economyFlex: 0, businessFlex: 0 },
  { city: 'Penang', country: 'Malaysia', zone: 'asean', economySaver: 3000, businessSaver: 6000, economyFlex: 4500, businessFlex: 9000 },
  { city: 'Langkawi', country: 'Malaysia', zone: 'asean', economySaver: 3500, businessSaver: 7000, economyFlex: 5250, businessFlex: 10500 },
  { city: 'Kota Kinabalu', country: 'Malaysia', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Kuching', country: 'Malaysia', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Singapore', country: 'Singapore', zone: 'asean', economySaver: 4000, businessSaver: 8000, economyFlex: 6000, businessFlex: 12000 },
  { city: 'Bangkok', country: 'Thailand', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Phuket', country: 'Thailand', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Jakarta', country: 'Indonesia', zone: 'asean', economySaver: 4500, businessSaver: 9000, economyFlex: 6750, businessFlex: 13500 },
  { city: 'Bali (Denpasar)', country: 'Indonesia', zone: 'asean', economySaver: 6000, businessSaver: 12000, economyFlex: 9000, businessFlex: 18000 },
  { city: 'Manila', country: 'Philippines', zone: 'asean', economySaver: 6000, businessSaver: 12000, economyFlex: 9000, businessFlex: 18000 },
  { city: 'Ho Chi Minh City', country: 'Vietnam', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Hanoi', country: 'Vietnam', zone: 'asean', economySaver: 6000, businessSaver: 12000, economyFlex: 9000, businessFlex: 18000 },
  { city: 'Phnom Penh', country: 'Cambodia', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Yangon', country: 'Myanmar', zone: 'asean', economySaver: 5000, businessSaver: 10000, economyFlex: 7500, businessFlex: 15000 },
  { city: 'Bandar Seri Begawan', country: 'Brunei', zone: 'asean', economySaver: 4000, businessSaver: 8000, economyFlex: 6000, businessFlex: 12000 },
  { city: 'Vientiane', country: 'Laos', zone: 'asean', economySaver: 6000, businessSaver: 12000, economyFlex: 9000, businessFlex: 18000 },

  // ── CHINA & GREATER CHINA ──
  { city: 'Guangzhou', country: 'China', zone: 'china', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Beijing', country: 'China', zone: 'china', economySaver: 10000, businessSaver: 20000, economyFlex: 15000, businessFlex: 30000 },
  { city: 'Shanghai', country: 'China', zone: 'china', economySaver: 10000, businessSaver: 20000, economyFlex: 15000, businessFlex: 30000 },
  { city: 'Xiamen', country: 'China', zone: 'china', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Hong Kong', country: 'Hong Kong', zone: 'china', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Taipei', country: 'Taiwan', zone: 'china', economySaver: 9000, businessSaver: 18000, economyFlex: 13500, businessFlex: 27000 },

  // ── ASIA ──
  { city: 'Tokyo', country: 'Japan', zone: 'asia', economySaver: 15000, businessSaver: 30000, economyFlex: 22500, businessFlex: 45000 },
  { city: 'Osaka', country: 'Japan', zone: 'asia', economySaver: 15000, businessSaver: 30000, economyFlex: 22500, businessFlex: 45000 },
  { city: 'Seoul', country: 'South Korea', zone: 'asia', economySaver: 12000, businessSaver: 24000, economyFlex: 18000, businessFlex: 36000 },
  { city: 'Busan', country: 'South Korea', zone: 'asia', economySaver: 14000, businessSaver: 28000, economyFlex: 21000, businessFlex: 42000 },
  { city: 'Narita', country: 'Japan', zone: 'asia', economySaver: 15000, businessSaver: 30000, economyFlex: 22500, businessFlex: 45000 },

  // ── INDIAN SUBCONTINENT ──
  { city: 'New Delhi', country: 'India', zone: 'india', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Mumbai', country: 'India', zone: 'india', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Chennai', country: 'India', zone: 'india', economySaver: 7000, businessSaver: 14000, economyFlex: 10500, businessFlex: 21000 },
  { city: 'Bangalore', country: 'India', zone: 'india', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Hyderabad', country: 'India', zone: 'india', economySaver: 8000, businessSaver: 16000, economyFlex: 12000, businessFlex: 24000 },
  { city: 'Kochi', country: 'India', zone: 'india', economySaver: 7000, businessSaver: 14000, economyFlex: 10500, businessFlex: 21000 },
  { city: 'Colombo', country: 'Sri Lanka', zone: 'india', economySaver: 7000, businessSaver: 14000, economyFlex: 10500, businessFlex: 21000 },
  { city: 'Dhaka', country: 'Bangladesh', zone: 'india', economySaver: 7000, businessSaver: 14000, economyFlex: 10500, businessFlex: 21000 },
  { city: 'Kathmandu', country: 'Nepal', zone: 'india', economySaver: 7000, businessSaver: 14000, economyFlex: 10500, businessFlex: 21000 },
  { city: 'Male', country: 'Maldives', zone: 'india', economySaver: 7000, businessSaver: 14000, economyFlex: 10500, businessFlex: 21000 },

  // ── MIDDLE EAST ──
  { city: 'Dubai', country: 'UAE', zone: 'middle-east', economySaver: 12000, businessSaver: 25000, economyFlex: 18000, businessFlex: 37500 },
  { city: 'Doha', country: 'Qatar', zone: 'middle-east', economySaver: 12000, businessSaver: 25000, economyFlex: 18000, businessFlex: 37500 },
  { city: 'Jeddah', country: 'Saudi Arabia', zone: 'middle-east', economySaver: 12000, businessSaver: 25000, economyFlex: 18000, businessFlex: 37500 },
  { city: 'Riyadh', country: 'Saudi Arabia', zone: 'middle-east', economySaver: 13000, businessSaver: 26000, economyFlex: 19500, businessFlex: 39000 },
  { city: 'Istanbul', country: 'Turkey', zone: 'middle-east', economySaver: 15000, businessSaver: 30000, economyFlex: 22500, businessFlex: 45000 },

  // ── AUSTRALIA & NEW ZEALAND ──
  { city: 'Melbourne', country: 'Australia', zone: 'australia', economySaver: 17000, businessSaver: 35000, economyFlex: 25500, businessFlex: 52500 },
  { city: 'Sydney', country: 'Australia', zone: 'australia', economySaver: 17000, businessSaver: 35000, economyFlex: 25500, businessFlex: 52500 },
  { city: 'Perth', country: 'Australia', zone: 'australia', economySaver: 15000, businessSaver: 30000, economyFlex: 22500, businessFlex: 45000 },
  { city: 'Brisbane', country: 'Australia', zone: 'australia', economySaver: 17000, businessSaver: 35000, economyFlex: 25500, businessFlex: 52500 },
  { city: 'Adelaide', country: 'Australia', zone: 'australia', economySaver: 18000, businessSaver: 36000, economyFlex: 27000, businessFlex: 54000 },
  { city: 'Auckland', country: 'New Zealand', zone: 'australia', economySaver: 20000, businessSaver: 40000, economyFlex: 30000, businessFlex: 60000 },
  { city: 'Christchurch', country: 'New Zealand', zone: 'australia', economySaver: 22000, businessSaver: 44000, economyFlex: 33000, businessFlex: 66000 },

  // ── EUROPE ──
  { city: 'London', country: 'United Kingdom', zone: 'europe', economySaver: 25000, businessSaver: 50000, economyFlex: 37500, businessFlex: 75000 },
  { city: 'Paris', country: 'France', zone: 'europe', economySaver: 25000, businessSaver: 50000, economyFlex: 37500, businessFlex: 75000 },
  { city: 'Amsterdam', country: 'Netherlands', zone: 'europe', economySaver: 25000, businessSaver: 50000, economyFlex: 37500, businessFlex: 75000 },
  { city: 'Frankfurt', country: 'Germany', zone: 'europe', economySaver: 25000, businessSaver: 50000, economyFlex: 37500, businessFlex: 75000 },
  { city: 'Istanbul', country: 'Turkey', zone: 'europe', economySaver: 15000, businessSaver: 30000, economyFlex: 22500, businessFlex: 45000 },
  { city: 'Zurich', country: 'Switzerland', zone: 'europe', economySaver: 28000, businessSaver: 56000, economyFlex: 42000, businessFlex: 84000 },
  { city: 'Milan', country: 'Italy', zone: 'europe', economySaver: 26000, businessSaver: 52000, economyFlex: 39000, businessFlex: 78000 },
  { city: 'Barcelona', country: 'Spain', zone: 'europe', economySaver: 26000, businessSaver: 52000, economyFlex: 39000, businessFlex: 78000 },
  { city: 'Copenhagen', country: 'Denmark', zone: 'europe', economySaver: 27000, businessSaver: 54000, economyFlex: 40500, businessFlex: 81000 },

  // ── NORTH AMERICA ──
  { city: 'New York', country: 'USA', zone: 'north-america', economySaver: 35000, businessSaver: 70000, economyFlex: 52500, businessFlex: 105000 },
  { city: 'Los Angeles', country: 'USA', zone: 'north-america', economySaver: 35000, businessSaver: 70000, economyFlex: 52500, businessFlex: 105000 },
  { city: 'San Francisco', country: 'USA', zone: 'north-america', economySaver: 35000, businessSaver: 70000, economyFlex: 52500, businessFlex: 105000 },
  { city: 'Chicago', country: 'USA', zone: 'north-america', economySaver: 37000, businessSaver: 74000, economyFlex: 55500, businessFlex: 111000 },
  { city: 'Vancouver', country: 'Canada', zone: 'north-america', economySaver: 35000, businessSaver: 70000, economyFlex: 52500, businessFlex: 105000 },
  { city: 'Toronto', country: 'Canada', zone: 'north-america', economySaver: 37000, businessSaver: 74000, economyFlex: 55500, businessFlex: 111000 },
];
