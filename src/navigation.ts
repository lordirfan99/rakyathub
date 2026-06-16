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
        { text: '---', href: '#' },
        {
          text: 'Duti Setem Hartanah',
          href: '/kalkulator/stamp-duty/',
        },
        {
          text: 'Yuran Guaman',
          href: '/kalkulator/legal-fees/',
        },
        {
          text: 'Refinancing',
          href: '/kalkulator/refinance/',
        },
        { text: '---', href: '#' },
        {
          text: 'Diskaun',
          href: '/kalkulator/diskaun/',
        },
        {
          text: 'Bahagi Bil & Tip',
          href: '/kalkulator/bahagi-bil/',
        },
        {
          text: 'Penukar Wang',
          href: '/kalkulator/currency-converter/',
        },
        { text: '---', href: '#' },
        {
          text: 'Cukai Jalan',
          href: '/kalkulator/cukai-jalan/',
        },
        {
          text: 'Kos Minyak',
          href: '/kalkulator/kos-minyak/',
        },
        { text: '---', href: '#' },
        {
          text: 'Umur',
          href: '/kalkulator/umur/',
        },
        {
          text: 'Beza Tarikh',
          href: '/kalkulator/beza-tarikh/',
        },
        {
          text: 'Penukar Unit',
          href: '/kalkulator/unit-converter/',
        },
        { text: '---', href: '#' },
        {
          text: 'Compound Interest',
          href: '/kalkulator/interest-compound/',
        },
        { text: '---', href: '#' },
        {
          text: 'Zakat Simpanan',
          href: '/kalkulator/zakat-simpanan/',
        },
        {
          text: 'Zakat Emas',
          href: '/kalkulator/zakat-emas/',
        },
        {
          text: 'Zakat Fitrah',
          href: '/kalkulator/zakat-fitrah/',
        },
        { text: '---', href: '#' },
        {
          text: 'BMI / Body Mass Index',
          href: '/kalkulator/bmi/',
        },
        {
          text: 'BMR & Kalori Harian',
          href: '/kalkulator/bmr/',
        },
        {
          text: 'Berat Badan Ideal',
          href: '/kalkulator/berat-ideal/',
        },
        {
          text: 'Tarikh Bersalin (Due Date)',
          href: '/kalkulator/tarikh-bersalin/',
        },
      ],
    },
    {
      text: 'Blog',
      href: getBlogPermalink(),
    },
    {
      text: 'Alat Dokumen',
      href: 'https://docukilat.rakyathub.my',
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
        { text: '---', href: '#' },
        { text: 'Duti Setem', href: '/kalkulator/stamp-duty/' },
        { text: 'Yuran Guaman', href: '/kalkulator/legal-fees/' },
        { text: 'Refinancing', href: '/kalkulator/refinance/' },
        { text: '---', href: '#' },
        { text: 'BMI', href: '/kalkulator/bmi/' },
        { text: 'BMR & Kalori', href: '/kalkulator/bmr/' },
        { text: 'Berat Ideal', href: '/kalkulator/berat-ideal/' },
        { text: 'Due Date', href: '/kalkulator/tarikh-bersalin/' },
      ],
    },
    {
      title: 'Blog',
      links: [
        { text: 'KWSP', href: getPermalink('kwsp', 'category') },
        { text: 'Kewangan', href: getPermalink('kewangan', 'category') },
        { text: 'Kerajaan', href: getPermalink('kerajaan', 'category') },
        { text: 'Insurans', href: getPermalink('insurans', 'category') },
        { text: 'Kesihatan', href: getPermalink('kesihatan', 'category') },
        { text: 'Pendidikan', href: getPermalink('pendidikan', 'category') },
        { text: 'Teknologi', href: getPermalink('teknologi', 'category') },
        { text: 'Bisnes', href: getPermalink('bisnes', 'category') },
      ],
    },
    {
      title: 'Alat',
      links: [
        { text: 'Penjana Surat AI', href: 'https://docukilat.rakyathub.my' },
        { text: 'PDF Tools', href: 'https://docukilat.rakyathub.my/tools/' },
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
