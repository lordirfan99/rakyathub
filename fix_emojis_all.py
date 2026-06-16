# Fix all emojis across site - comprehensive script
import re

# ── 1. HOMEPAGE ──
path = r'C:\Users\irfan\rakyathub\src\pages\index.astro'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace emoji function
c = c.replace(
    "function getEmoji(n) {\n  const u = (n||'').toUpperCase();\n  const EMOJI_MAP = { AYAM:'🍗', DAGING:'🥩', IKAN:'🐟', TELUR:'🥚', BERAS:'🍚', MINYAK:'🫙', GULA:'🧂', TEPUNG:'🌾', CILI:'🌶️', BAWANG:'🧅', HALIA:'🫚', KACANG:'🥜', KUBIS:'🥬', LOBAK:'🥕', TIMUN:'🥒', SANTAN:'🥥' };\n  for (const [k,v] of Object.entries(EMOJI_MAP)) if (u.includes(k)) return v;\n  return '🛒';\n}",
    "function getInitial(n) {\n  const u = (n||'').toUpperCase();\n  return u.charAt(0) || '?';\n}"
)

# Replace getEmoji calls
c = c.replace("getEmoji(item.name||'')", "getInitial(item.name||'')")

# Replace span with gradient badge for food items
old_span = '<span class=\"text-lg sm:text-xl w-7 sm:w-8 text-center shrink-0\">{getInitial(item.name||\\'\\')}</span>'
c = c.replace(
    '<span class="text-lg sm:text-xl w-7 sm:w-8 text-center shrink-0">{getInitial(item.name||'')}</span>',
    '<span class="w-6 h-6 rounded-md bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-[10px] font-bold shrink-0">{getInitial(item.name||'')}</span>'
)

# Replace Hero section emojis
c = c.replace(
    '<a href="/harga-makanan-hari-ini/" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold transition-all hover:shadow-lg hover:-translate-y-0.5">\n          🛒 Harga Makanan',
    '<a href="/harga-makanan-hari-ini/" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold transition-all hover:shadow-lg hover:-translate-y-0.5">\n          Harga Makanan'
)
c = c.replace(
    '<a href="/kalkulator/" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300 text-sm font-semibold hover:bg-gray-50 dark:hover:bg-slate-800/60 transition-all">\n          📊 Kalkulator',
    '<a href="/kalkulator/" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300 text-sm font-semibold hover:bg-gray-50 dark:hover:bg-slate-800/60 transition-all">\n          Kalkulator'
)

# Replace food section stats emojis
c = c.replace('<span class="inline-flex items-center gap-1">📊 <span', '<span class="inline-flex items-center gap-1"><span')
c = c.replace('<span class="inline-flex items-center gap-1">📦 <span', '<span class="inline-flex items-center gap-1"><span')

# Replace Food section "LANGSUNG" badge  
c = c.replace(
    'LANGSUNG',
    'Terkini'
)
# Remove live dot before LANGSUNG
c = c.replace(
    '<span class="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>\n            LANGSUNG',
    'Terkini'
)

# Fix the badge for food - put label back
c = c.replace(
    '<span class="inline-flex items-center gap-1.5 text-[10px] sm:text-xs font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 px-2.5 py-1 rounded-full shrink-0">\n            Terkini\n          </span>',
    '<span class="inline-flex items-center gap-1.5 text-[10px] sm:text-xs font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 px-2.5 py-1 rounded-full shrink-0">\n            <span class="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>\n            Live\n          </span>'
)

# Fix popular articles section - replace emoji icons with letter badges
old_pop = """      {[
        { icon: '\U0001f4b0', title: 'Bajet 50/30/20', href: '/cadangan-bajet-50-30-20-di-malaysia/', desc: 'Cara bahagi gaji' },
        { icon: '\U0001f3e6', title: 'Panduan KWSP', href: '/panduan-kwsp-malaysia-2025/', desc: 'Caruman & dividen' },
        { icon: '\U0001f7e1', title: 'Beli Emas GAP', href: '/cara-beli-emas-public-gold/', desc: 'Panduan Public Gold' },
        { icon: '\U0001f4b8', title: 'Urus Gaji <RM3K', href: '/urus-duit-gaji-bawah-rm3000/', desc: 'Tips praktikal' },
        { icon: '\U0001f6e1\ufe0f', title: 'Medical Card', href: '/panduan-medical-card-malaysia-2026-first-time-buyer/', desc: 'Panduan first buyer' },
        { icon: '\U0001f393', title: 'Gaji Graduan', href: '/gaji-graduan-mengikut-industri-2026/', desc: 'Ikut industri' },
        { icon: '\U0001f9fe', title: 'E-Filing 2026', href: '/panduan-e-filing-cukai-pendapatan-2026/', desc: 'Cara isi cukai' },
        { icon: '\U0001f4f1', title: 'eWallet Terbaik', href: '/gxbank-vs-bigpay-vs-tng-ewallet-dompet-digital-terbaik-2026/', desc: 'GXBank vs BigPay' },
        { icon: '\U0001f4b0', title: 'Countdown Gaji', href: '/berapa-hari-lagi-nak-gaji/', desc: 'Hari ke gaji' },
        { icon: '\U0001fa7a', title: 'Quiz Kewangan', href: '/quiz-kesihatan-kewangan/', desc: 'Skor kesihatan' },
      ].map(a => (
        <a href={a.href} class="rounded-xl bg-white dark:bg-slate-800/80 border border-gray-100 dark:border-slate-700/50 p-4 hover:border-blue-200 dark:hover:border-blue-800/50 hover:shadow-md transition-all hover:-translate-y-0.5 group">
          <span class="text-xl block mb-1.5">{a.icon}</span>"""

new_pop = """      {[
        { icon: 'B', title: 'Bajet 50/30/20', href: '/cadangan-bajet-50-30-20-di-malaysia/', desc: 'Cara bahagi gaji', bg: 'from-blue-500 to-indigo-600' },
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

if old_pop in c:
    c = c.replace(old_pop, new_pop)
    print("Popular articles updated!")
else:
    print("Popular articles NOT FOUND - checking raw bytes...")
    # Search for 'Bajet 50/30/20' to find the section
    idx = c.find("Bajet 50/30/20")
    if idx >= 0:
        print(f"Found 'Bajet 50/30/20' at pos {idx}")
        print(repr(c[idx-30:idx+120]))
    else:
        print("Not found at all")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("--- Homepage done ---")

# ── 2. CPI PAGE ──
path2 = r'C:\Users\irfan\rakyathub\src\pages\inflasi-malaysia.astro'
with open(path2, 'r', encoding='utf-8') as f:
    c2 = f.read()

c2 = c2.replace('📊 CPI', 'CPI')
c2 = c2.replace('🔥 Inflasi', 'Inflasi')
c2 = c2.replace('📈 47', '47')
c2 = c2.replace('📈 Indeks Harga Pengguna Malaysia (Tahunan)', 'Indeks Harga Pengguna Malaysia (Tahunan)')
c2 = c2.replace('🏷️ CPI Ikut Kategori', 'CPI Ikut Kategori')
c2 = c2.replace('🧮 Kira Nilai Wang Mengikut Tahun', 'Kira Nilai Wang Mengikut Tahun')
c2 = c2.replace('i', 'i')  # keep the info icon as is

with open(path2, 'w', encoding='utf-8') as f:
    f.write(c2)
print("--- CPI page done ---")

# ── 3. BANTUAN PAGE ──
path3 = r'C:\Users\irfan\rakyathub\src\pages\bantuan-kerajaan.astro'
with open(path3, 'r', encoding='utf-8') as f:
    c3 = f.read()

c3 = c3.replace('🇲🇾 Bantuan Kerajaan Malaysia 2026', 'Bantuan Kerajaan Malaysia 2026')

with open(path3, 'w', encoding='utf-8') as f:
    f.write(c3)
print("--- Bantuan page done ---")

# ── 4. ARTICLE WIDGETS (SinglePost) ──
path4 = r'C:\Users\irfan\rakyathub\src\components\blog\SinglePost.astro'
with open(path4, 'r', encoding='utf-8') as f:
    c4 = f.read()

c4 = c4.replace("Harga Barang Runcit Malaysia</h3>'", "Harga Barang Runcit</h3>'")
c4 = c4.replace("'📊 Lihat Semua Harga Terkini →</a>'", "'Lihat Semua Harga Terkini \u2192</a>'")
c4 = c4.replace("'📈 Semak Data Inflasi Penuh →</a>'", "'Semak Data Inflasi Penuh \u2192</a>'")
c4 = c4.replace("'<span class=\"text-xs font-semibold text-red-500\">🔥 Inflasi</span></div>'", "'<span class=\"text-xs font-semibold text-red-500\">Inflasi</span></div>'")

with open(path4, 'w', encoding='utf-8') as f:
    f.write(c4)
print("--- Article widgets done ---")

print("\n✅ All emoji cleanups complete!")
