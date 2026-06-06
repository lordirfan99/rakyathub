import { getPermalink, getBlogPermalink, getAsset } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Laman Utama',
      href: getPermalink('/'),
    },
    {
      text: 'Kalkulator',
      links: [
        {
          text: 'Semua Kalkulator',
          href: getPermalink('/kalkulator'),
        },
        {
          text: 'STR & SARA',
          href: '/kalkulator/str-sara/',
        },
        {
          text: 'Gaji Bersih',
          href: '/kalkulator/gaji-bersih/',
        },
        {
          text: 'SST',
          href: '/kalkulator/sst/',
        },
        {
          text: 'Zakat Pendapatan',
          href: '/kalkulator/zakat-pendapatan/',
        },
        {
          text: 'Beli vs Sewa',
          href: '/kalkulator/beli-sewa-rumah/',
        },
        {
          text: 'Emas vs ASB vs FD',
          href: '/kalkulator/pelaburan/',
        },
        { text: '---', href: '#' },
        {
          text: 'KWSP',
          href: getPermalink('/kalkulator/kwsp'),
        },
        {
          text: 'ASB',
          href: getPermalink('/kalkulator/asb'),
        },
        {
          text: 'Emas',
          href: getPermalink('/kalkulator/emas'),
        },
        {
          text: 'Kereta',
          href: getPermalink('/kalkulator/kereta'),
        },
        {
          text: 'Loan Rumah',
          href: getPermalink('/kalkulator/loan-rumah'),
        },
        {
          text: 'Zakat',
          href: getPermalink('/kalkulator/zakat'),
        },
      ],
    },
    {
      text: 'Blog',
      href: getBlogPermalink(),
    },
    {
      text: 'Alat Dokumen',
      href: 'https://docukilat.netlify.app',
    },
    {
      text: 'Tentang',
      href: getPermalink('/tentang'),
    },
    {
      text: 'Hubungi',
      href: getPermalink('/hubungi'),
    },
  ],
  actions: [
    { text: 'Semua Kalkulator', href: getPermalink('/kalkulator'), variant: 'primary' as const },
  ],
};

export const footerData = {
  links: [
    {
      title: 'Kalkulator',
      links: [
        { text: 'Semua Kalkulator', href: getPermalink('/kalkulator') },
        { text: 'STR & SARA', href: '/kalkulator/str-sara/' },
        { text: 'Gaji Bersih', href: '/kalkulator/gaji-bersih/' },
        { text: 'SST', href: '/kalkulator/sst/' },
        { text: 'Zakat Pendapatan', href: '/kalkulator/zakat-pendapatan/' },
        { text: 'Beli vs Sewa', href: '/kalkulator/beli-sewa-rumah/' },
        { text: 'Emas vs ASB vs FD', href: '/kalkulator/pelaburan/' },
        { text: '---', href: '#' },
        { text: 'KWSP', href: getPermalink('/kalkulator/kwsp') },
        { text: 'ASB', href: getPermalink('/kalkulator/asb') },
        { text: 'Emas', href: getPermalink('/kalkulator/emas') },
        { text: 'Kereta', href: getPermalink('/kalkulator/kereta') },
        { text: 'Loan Rumah', href: getPermalink('/kalkulator/loan-rumah') },
        { text: 'Zakat', href: getPermalink('/kalkulator/zakat') },
      ],
    },
    {
      title: 'Blog',
      links: [
        { text: 'KWSP', href: getPermalink('kwsp', 'category') },
        { text: 'Kewangan', href: getPermalink('kewangan', 'category') },
        { text: 'Kerajaan', href: getPermalink('kerajaan', 'category') },
        { text: 'Insurans', href: getPermalink('insurans', 'category') },
      ],
    },
    {
      title: 'Alat',
      links: [
        { text: 'Penjana Surat AI', href: 'https://docukilat.netlify.app' },
        { text: 'PDF Tools', href: 'https://docukilat.netlify.app/tools/' },
        { text: 'Kalkulator Kewangan', href: getPermalink('/kalkulator/kwsp') },
      ],
    },
    {
      title: 'Syarikat',
      links: [
        { text: 'Tentang Kami', href: getPermalink('/tentang') },
        { text: 'Hubungi', href: getPermalink('/hubungi') },
        { text: 'Dasar Privasi', href: getPermalink('/privasi') },
        { text: 'Terma & Syarat', href: getPermalink('/terma') },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Terma', href: getPermalink('/terma') },
    { text: 'Dasar Privasi', href: getPermalink('/privasi') },
  ],
  socialLinks: [
    { ariaLabel: 'RSS', icon: 'tabler:rss', href: getAsset('/rss.xml') },
  ],
  footNote: `
    <span class="w-5 h-5 md:w-6 md:h-6 md:-mt-0.5 bg-cover mr-1.5 rtl:mr-0 rtl:ml-1.5 float-left rtl:float-right rounded-sm bg-[url(/favicon.ico)]"></span>
    Hak cipta terpelihara <a class="text-primary hover:text-secondary transition-colors font-medium" href="/"> RakyatHub</a> · ${new Date().getFullYear()}.
  `,
};
