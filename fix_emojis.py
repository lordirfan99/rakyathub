import re

path = r'C:\Users\irfan\rakyathub\src\pages\index.astro'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace popular articles emojis with clean letter badges
old = "        { icon: '💰', title: 'Bajet 50/30/20', href: '/cadangan-bajet-50-30-20-di-malaysia/', desc: 'Cara bahagi gaji' },\n        { icon: '🏦', title: 'Panduan KWSP', href: '/panduan-kwsp-malaysia-2025/', desc: 'Caruman & dividen' },\n        { icon: '🟡', title: 'Beli Emas GAP', href: '/cara-beli-emas-public-gold/', desc: 'Panduan Public Gold' },\n        { icon: '💸', title: 'Urus Gaji <RM3K', href: '/urus-duit-gaji-bawah-rm3000/', desc: 'Tips praktikal' },\n        { icon: '🛡️', title: 'Medical Card', href: '/panduan-medical-card-malaysia-2026-first-time-buyer/', desc: 'Panduan first buyer' },\n        { icon: '🎓', title: 'Gaji Graduan', href: '/gaji-graduan-mengikut-industri-2026/', desc: 'Ikut industri' },\n        { icon: '🧾', title: 'E-Filing 2026', href: '/panduan-e-filing-cukai-pendapatan-2026/', desc: 'Cara isi cukai' },\n        { icon: '📱', title: 'eWallet Terbaik', href: '/gxbank-vs-bigpay-vs-tng-ewallet-dompet-digital-terbaik-2026/', desc: 'GXBank vs BigPay' },\n        { icon: '💰', title: 'Countdown Gaji', href: '/berapa-hari-lagi-nak-gaji/', desc: 'Hari ke gaji' },\n        { icon: '🩺', title: 'Quiz Kewangan', href: '/quiz-kesihatan-kewangan/', desc: 'Skor kesihatan' },\n      ].map(a => (\n        <a href={a.href} class=\"rounded-xl bg-white dark:bg-slate-800/80 border border-gray-100 dark:border-slate-700/50 p-4 hover:border-blue-200 dark:hover:border-blue-800/50 hover:shadow-md transition-all hover:-translate-y-0.5 group\">\n          <span class=\"text-xl block mb-1.5\">{a.icon}</span>"

new_items = """        { icon: 'B', title: 'Bajet 50/30/20', href: '/cadangan-bajet-50-30-20-di-malaysia/', desc: 'Cara bahagi gaji', bg: 'from-blue-500 to-indigo-600' },
        { icon: 'K', title: 'Panduan KWSP', href: '/panduan-kwsp-malaysia-2025/', desc: 'Caruman & dividen', bg: 'from-emerald-500 to-teal-600' },
        { icon: 'E', title: 'Beli Emas GAP', href: '/cara-beli-emas-public-gold/', desc: 'Panduan Public Gold', bg: 'from-amber-500 to-orange-600' },
        { icon: 'U', title: 'Urus Gaji <RM3K', href: '/urus-duit-gaji-bawah-rm3000/', desc: 'Tips praktikal', bg: 'from-rose-500 to-pink-600' },
        { icon: 'M', title: 'Medical Card', href: '/panduan-medical-card-malaysia-2026-first-time-buyer/', desc: 'Panduan first buyer', bg: 'from-violet-500 to-purple-600' },
        { icon: 'G', title: 'Gaji Graduan', href: '/gaji-graduan-mengikut-industri-2026/', desc: 'Ikut industri', bg: 'from-cyan-500 to-blue-600' },
        { icon: 'C', title: 'E-Filing 2026', href: '/panduan-e-filing-cukai-pendapatan-2026/', desc: 'Cara isi cukai', bg: 'from-sky-500 to-blue-600' },
        { icon: 'D', title: 'eWallet Terbaik', href: '/gxbank-vs-bigpay-vs-tng-ewallet-dompet-digital-terbaik-2026/', desc: 'GXBank vs BigPay', bg: 'from-indigo-500 to-purple-600' },
        { icon: '#', title: 'Countdown Gaji', href: '/berapa-hari-lagi-nak-gaji/', desc: 'Hari ke gaji', bg: 'from-orange-500 to-red-600' },
        { icon: '?', title: 'Quiz Kewangan', href: '/quiz-kesihatan-kewangan/', desc: 'Skor kesihatan', bg: 'from-green-500 to-emerald-600' },
      ].map(a => (
        <a href={a.href} class="rounded-xl bg-white dark:bg-slate-800/80 border border-gray-100 dark:border-slate-700/50 p-4 hover:border-blue-200 dark:hover:border-blue-800/50 hover:shadow-md transition-all hover:-translate-y-0.5 group">
          <span class={`w-7 h-7 rounded-lg bg-gradient-to-br ${a.bg} flex items-center justify-center text-white text-xs font-bold shadow-sm mb-1.5`}>{a.icon}</span>"""

if old in content:
    content = content.replace(old, new_items)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Popular articles updated!")
else:
    print("Old block not found - checking encoding...")
    # Find the emojis to check
    for emoji in ['💰', '🏦', '🟡']:
        idx = content.find(emoji)
        if idx >= 0:
            print(f"Found {emoji} at position {idx}")
            print(repr(content[idx-5:idx+30]))

# Now fix CPI page badges
cpi_path = r'C:\Users\irfan\rakyathub\src\pages\inflasi-malaysia.astro'
with open(cpi_path, 'r', encoding='utf-8') as f:
    cpi_content = f.read()

# Replace emoji badges in CPI page
cpi_content = cpi_content.replace('📊 CPI', 'CPI')
cpi_content = cpi_content.replace('🔥 Inflasi', 'Inflasi')
cpi_content = cpi_content.replace('📈 47', '47')

# Replace heading emojis
cpi_content = cpi_content.replace('📈 Indeks Harga Pengguna Malaysia (Tahunan)', 'Indeks Harga Pengguna Malaysia (Tahunan)')
cpi_content = cpi_content.replace('🏷️ CPI Ikut Kategori', 'CPI Ikut Kategori')
cpi_content = cpi_content.replace('🧮 Kira Nilai Wang Mengikut Tahun', 'Kira Nilai Wang Mengikut Tahun')

with open(cpi_path, 'w', encoding='utf-8') as f:
    f.write(cpi_content)

print("CPI page emojis cleaned!")
print("Done!")
