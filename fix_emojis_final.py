#!/usr/bin/env python3
"""Remove emojis from rakyathub.my pages - replace with gradient letter badges"""

import re

def clean_homepage():
    path = r'C:\Users\irfan\rakyathub\src\pages\index.astro'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # 1. Replace emoji function with initial-letter function
    # The emoji map line
    c = c.replace(
        "const EMOJI_MAP = { AYAM:'\U0001f357', DAGING:'\U0001f969', IKAN:'\U0001f41f', TELUR:'\U0001f95a', BERAS:'\U0001f35a', MINYAK:'\U0001fad9', GULA:'\U0001f9ca', TEPUNG:'\U0001f33e', CILI:'\U0001f336\ufe0f', BAWANG:'\U0001f9c5', HALIA:'\U0001fada', KACANG:'\U0001f95c', KUBIS:'\U0001f96c', LOBAK:'\U0001f955', TIMUN:'\U0001f952', SANTAN:'\U0001f965' };",
        ""
    )
    c = c.replace(
        "for (const [k,v] of Object.entries(EMOJI_MAP)) if (u.includes(k)) return v;",
        ""
    )
    c = c.replace("return '\U0001f6d2';", "return u.charAt(0) || '?';")
    
    # Rename function
    c = c.replace("function getEmoji(n)", "function getInitial(n)")
    c = c.replace("getEmoji(item.name||'')", "getInitial(item.name||'')")
    
    # 2. Replace emoji food icon span with gradient badge
    old_food_icon = '<span class="text-lg sm:text-xl w-7 sm:w-8 text-center shrink-0">{getInitial(item.name||'')}</span>'
    new_food_icon = '<span class="w-6 h-6 rounded-md bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-[10px] font-bold shrink-0">{getInitial(item.name||'')}</span>'
    c = c.replace(old_food_icon, new_food_icon)
    
    # 3. Replace hero button emojis
    c = c.replace('\U0001f6d2 Harga Makanan', 'Harga Makanan')
    c = c.replace('\U0001f4ca Kalkulator', 'Kalkulator')
    
    # 4. Replace food section stat emojis
    c = c.replace('\U0001f4ca <span class="font-semibold', '<span class="font-semibold')
    c = c.replace('\U0001f4e6 <span class="font-semibold', '<span class="font-semibold')
    
    # 5. Fix the food header badge
    c = c.replace(
        '<span class="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>\n            LANGSUNG',
        'Live'
    )
    # Clean up double badge
    c = c.replace('''<span class="inline-flex items-center gap-1.5 text-[10px] sm:text-xs font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 px-2.5 py-1 rounded-full shrink-0">
            Live
          </span>''', 
      '<span class="inline-flex items-center gap-1.5 text-[10px] sm:text-xs font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 px-2.5 py-1 rounded-full shrink-0">Live</span>')
    
    # 6. Replace popular articles grid emojis with letter badges
    # Find the popular articles section
    pop_start = c.find("title: 'Bajet 50/30/20'")
    if pop_start > 0:
        # Find the start of the icons block
        block_start = c.rfind("]", 0, pop_start)
        block_start = c.rfind("{ icon:", 0, block_start)
        
        # Find the ].map(a => line
        map_line = c.find("].map(a => (", block_start)
        a_tag = c.find('<a href={a.href}', map_line)
        
        # Build replacement
        new_pop = """        { icon: 'B', title: 'Bajet 50/30/20', href: '/cadangan-bajet-50-30-20-di-malaysia/', desc: 'Cara bahagi gaji', bg: 'from-blue-500 to-indigo-600' },
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
        
        c = c[:block_start] + new_pop + c[a_tag:]
        print("Popular articles grid updated!")
    
    # 7. Replace Data Tools section emojis
    c = c.replace(
        '<span class="w-10 h-10 rounded-xl bg-gradient-to-br from-red-500 to-amber-600 flex items-center justify-center text-white text-lg shadow-sm">\U0001f4c8</span>',
        '<span class="w-10 h-10 rounded-xl bg-gradient-to-br from-red-500 to-amber-600 flex items-center justify-center text-white text-sm font-bold shadow-sm">%</span>'
    )
    c = c.replace(
        '<span class="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white text-lg shadow-sm">\U0001f1f2\U0001f1fe</span>',
        '<span class="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white text-sm font-bold shadow-sm">RM</span>'
    )
    
    # 8. Clean up remaining stat emojis in food footer
    c = c.replace('\U0001f4ca <span', '<span')
    c = c.replace('\U0001f4e6 <span', '<span')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Homepage cleaned!")


def clean_cpi_page():
    path = r'C:\Users\irfan\rakyathub\src\pages\inflasi-malaysia.astro'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Remove emojis from badge labels
    c = c.replace('\U0001f4ca CPI', 'CPI')
    c = c.replace('\U0001f525 Inflasi', 'Inflasi')
    c = c.replace('\U0001f4c8 47', '47')
    
    # Remove emojis from headings
    c = c.replace('\U0001f4c8 Indeks Harga Pengguna Malaysia (Tahunan)', 'Indeks Harga Pengguna Malaysia (Tahunan)')
    c = c.replace('\U0001f3f7\ufe0f CPI Ikut Kategori', 'CPI Ikut Kategori')
    c = c.replace('\U0001f9ee Kira Nilai Wang Mengikut Tahun', 'Kira Nilai Wang Mengikut Tahun')
    
    # Also try without variation selector
    c = c.replace('\U0001f3f7 CPI Ikut Kategori', 'CPI Ikut Kategori')
    c = c.replace('\U0001f9ee Kira Nilai Wang', 'Kira Nilai Wang')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("CPI page cleaned!")


def clean_bantuan_page():
    path = r'C:\Users\irfan\rakyathub\src\pages\bantuan-kerajaan.astro'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    c = c.replace('\U0001f1f2\U0001f1fe Bantuan Kerajaan Malaysia 2026', 'Bantuan Kerajaan Malaysia 2026')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Bantuan page cleaned!")


def clean_article_widgets():
    path = r'C:\Users\irfan\rakyathub\src\components\blog\SinglePost.astro'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    c = c.replace("Harga Barang Runcit Malaysia</h3>'", "Harga Barang Runcit</h3>'")
    c = c.replace("'\U0001f4ca Lihat Semua Harga Terkini \u2192</a>'", "'Lihat Semua Harga Terkini \u2192</a>'")
    c = c.replace("'\U0001f4c8 Semak Data Inflasi Penuh \u2192</a>'", "'Semak Data Inflasi Penuh \u2192</a>'")
    c = c.replace("'<span class=\"text-xs font-semibold text-red-500\">\U0001f525 Inflasi</span></div>'", "'<span class=\"text-xs font-semibold text-red-500\">Inflasi</span></div>'")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Article widgets cleaned!")


if __name__ == '__main__':
    clean_homepage()
    clean_cpi_page()
    clean_bantuan_page()
    clean_article_widgets()
    print("\nAll done!")
