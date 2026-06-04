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
    url: '/cara-semak-baki-kwsp-online-tanpa-pergi-kaunter-2025-panduan-lengkap/',
    title: 'cara semak baki KWSP online 2025',
    keywords: ['kwsp', 'caruman kwsp', 'pengeluaran kwsp', 'akaun kwsp', 'persaraan'],
  },
  {
    word: 'ASB',
    url: '/7-kelebihan-simpanan-asb-pelaburan-bijak-pulangan-konsisten-yang-pasti-korang-tak-tahu/',
    title: '7 kelebihan simpanan ASB yang perlu tahu',
    keywords: ['asb', 'dividen asb', 'asb loan', 'pelaburan asb', 'simpanan asb'],
  },
  {
    word: 'Bajet 50/30/20',
    url: '/cadangan-bajet-50-30-20-di-malaysia/',
    title: 'panduan bajet 50/30/20 di Malaysia',
    keywords: ['bajet 50/30/20', '50 30 20', 'peraturan bajet', 'bajet bulanan'],
  },
  {
    word: 'Emas',
    url: '/cara-beli-emas-public-gold/',
    title: 'cara beli emas Public Gold',
    keywords: ['emas', 'harga emas', 'public gold', 'pelaburan emas', 'dinar emas'],
  },
  {
    word: 'Pelaburan',
    url: '/strategi-dca-vs-lump-sum-pilihan-pelaburan-bijak-untuk-orang-muda/',
    title: 'strategi DCA vs Lump Sum untuk pelabur muda',
    keywords: ['pelaburan', 'dca', 'lump sum', 'robo-advisor', 'investasi'],
  },
  {
    word: 'Loan Rumah',
    url: '/kalkulator/loan-rumah/',
    title: 'kalkulator loan rumah',
    keywords: ['loan rumah', 'pinjaman rumah', 'ansuran rumah', 'mortgage'],
  },
  {
    word: 'Bantuan Kerajaan',
    url: '/info-bantuan-rm100-mykad-subsidi-ron95-kemas-kini-rakyathub/',
    title: 'info bantuan RM100 MyKad & subsidi RON95',
    keywords: ['bantuan kerajaan', 'subsidi', 'bantuan tunai', 'sara hidup', 'str'],
  },
  {
    word: 'Kereta',
    url: '/kalkulator/kereta/',
    title: 'kalkulator ansuran kereta',
    keywords: ['kereta', 'ansuran kereta', 'loan kereta', 'beli kereta'],
  },
];

// NOTE: Cross-linking is performed client-side via the DOM walker in SinglePost.astro.
// This SSR version is retained as a reference but is NOT called anywhere in the build.
// If re-activated for SSR rendering, ensure all injected values are HTML-escaped.

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

export function injectCrosslinks(html: string, currentSlug?: string): string {
  let result = html;
  const maxLinks = 2;
  let linkCount = 0;

  for (const link of crossLinks) {
    if (linkCount >= maxLinks) break;
    if (currentSlug && link.url.includes(currentSlug)) continue;

    const escapedWord = link.word.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&');
    // Avoid catastrophic backtracking: use a bounded lookahead depth
    const regex = new RegExp(`(?<!<a[^>]{0,200}>)\\b${escapedWord}\\b(?![^<]{0,200}<\\/a>)`, 'gi');

    // Escape link metadata before injecting into HTML attribute context
    const safeUrl = escapeHtml(link.url);
    const safeTitle = escapeHtml(link.title);

    result = result.replace(regex, (match) => {
      if (linkCount >= maxLinks) return match;
      linkCount++;
      return `<a href="${safeUrl}" class="text-primary dark:text-blue-400 hover:underline font-medium" title="${safeTitle}">${escapeHtml(match)}</a>`;
    });
  }

  return result;
}
