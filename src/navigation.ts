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
          text: 'Kalkulator KWSP',
          href: getPermalink('/kalkulator/kwsp'),
        },
        {
          text: 'Kalkulator ASB',
          href: getPermalink('/kalkulator/asb'),
        },
        {
          text: 'Kalkulator Emas',
          href: getPermalink('/kalkulator/emas'),
        },
        {
          text: 'Kalkulator Kereta',
          href: getPermalink('/kalkulator/kereta'),
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
    { text: 'Langgan Percuma', href: '#', variant: 'primary' },
  ],
};

export const footerData = {
  links: [
    {
      title: 'Kalkulator',
      links: [
        { text: 'Kalkulator KWSP', href: getPermalink('/kalkulator/kwsp') },
        { text: 'Kalkulator ASB', href: getPermalink('/kalkulator/asb') },
        { text: 'Kalkulator Emas', href: getPermalink('/kalkulator/emas') },
        { text: 'Kalkulator Kereta', href: getPermalink('/kalkulator/kereta') },
      ],
    },
    {
      title: 'Blog',
      links: [
        { text: 'KWSP', href: getPermalink('kwsp', 'category') },
        { text: 'ASB', href: getPermalink('asb', 'category') },
        { text: 'Emas & Pelaburan', href: getPermalink('emas', 'category') },
        { text: 'Bantuan Kerajaan', href: getPermalink('kerajaan', 'category') },
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
    { ariaLabel: 'X', icon: 'tabler:brand-x', href: '#' },
    { ariaLabel: 'Instagram', icon: 'tabler:brand-instagram', href: '#' },
    { ariaLabel: 'Facebook', icon: 'tabler:brand-facebook', href: '#' },
    { ariaLabel: 'TikTok', icon: 'tabler:brand-tiktok', href: '#' },
    { ariaLabel: 'RSS', icon: 'tabler:rss', href: getAsset('/rss.xml') },
  ],
  footNote: `
    <span class="w-5 h-5 md:w-6 md:h-6 md:-mt-0.5 bg-cover mr-1.5 rtl:mr-0 rtl:ml-1.5 float-left rtl:float-right rounded-sm bg-[url(https://rakyathub.com/favicon.ico)]"></span>
    Hak cipta terpelihara <a class="text-blue-600 underline dark:text-muted" href="https://rakyathub.com"> RakyatHub</a> · 2025.
  `,
};
