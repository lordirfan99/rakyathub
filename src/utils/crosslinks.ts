// Cross-linking engine for RakyatHub blog
// Injects contextual internal links into rendered blog content
// Only processes text nodes outside HTML tags to avoid breaking existing links

export interface CrossLinkDef {
  word: string;
  url: string;
  title: string;
  keywords: string[];
}

export const crossLinks: CrossLinkDef[] = [
  {
    word: 'KWSP',
    url: '/blog/',
    title: 'baca panduan KWSP',
    keywords: ['kwsp', 'caruman kwsp', 'pengeluaran kwsp', 'akaun kwsp', 'persaraan'],
  },
  {
    word: 'ASB',
    url: '/blog/',
    title: 'baca panduan ASB',
    keywords: ['asb', 'dividen asb', 'asb loan', 'pelaburan asb', 'simpanan asb'],
  },
  {
    word: 'Bajet 50/30/20',
    url: '/cadangan-bajet-50-30-20-di-malaysia/',
    title: 'baca panduan bajet 50/30/20',
    keywords: ['bajet 50/30/20', '50 30 20', 'peraturan bajet', 'bajet bulanan'],
  },
  {
    word: 'Emas',
    url: '/blog/',
    title: 'baca panduan emas',
    keywords: ['emas', 'harga emas', 'public gold', 'pelaburan emas', 'dinar emas'],
  },
  {
    word: 'Pelaburan',
    url: '/blog/',
    title: 'baca panduan pelaburan',
    keywords: ['pelaburan', 'dca', 'lump sum', 'robo-advisor', 'investasi'],
  },
  {
    word: 'Loan Rumah',
    url: '/kalkulator/loan-rumah',
    title: 'kira loan rumah',
    keywords: ['loan rumah', 'pinjaman rumah', 'ansuran rumah', 'mortgage'],
  },
  {
    word: 'Bantuan Kerajaan',
    url: '/blog/',
    title: 'baca bantuan kerajaan',
    keywords: ['bantuan kerajaan', 'subsidi', 'bantuan tunai', 'sara hidup', 'str'],
  },
  {
    word: 'Kereta',
    url: '/kalkulator/kereta',
    title: 'kira ansuran kereta',
    keywords: ['kereta', 'ansuran kereta', 'loan kereta', 'beli kereta'],
  },
];

// Sanitize text before processing: remove content inside already-linked <a> tags
// and inject links into first 2 matching standalone text occurrences

export function injectCrosslinks(html: string, currentSlug?: string): string {
  let result = html;
  const maxLinks = 2; // max 2 cross-links per article
  let linkCount = 0;

  for (const link of crossLinks) {
    if (linkCount >= maxLinks) break;

    // Don't link to the current article
    if (currentSlug && link.url.includes(currentSlug)) continue;

    // Use word boundary matching to match standalone words
    const escaped = link.word.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&');
    const regex = new RegExp(`(?<!<a[^>]*>)\\b${escaped}\\b(?!.*?<\\/a>)`, 'gi');

    result = result.replace(regex, (match) => {
      if (linkCount >= maxLinks) return match;
      linkCount++;
      return `<a href="${link.url}" class="text-primary dark:text-blue-400 hover:underline font-medium" title="${link.title}">${match}</a>`;
    });
  }

  return result;
}
