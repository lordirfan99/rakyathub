import re

# ── 1. HOMEPAGE: Calculator grid icons ──
path = r'C:\Users\irfan\rakyathub\src\pages\index.astro'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

calc_old = r"""        { icon: '\U0001f3e6', name: 'KWSP', href: '/kalkulator/kwsp/', desc: 'Caruman & dividen' },
        { icon: '\U0001f4c8', name: 'ASB', href: '/kalkulator/asb/', desc: 'Dividen & bonus' },
        { icon: '\U0001f7e1', name: 'Emas', href: '/kalkulator/emas/', desc: 'Harga emas semasa' },
        { icon: '\U0001f697', name: 'Kereta', href: '/kalkulator/kereta/', desc: 'Ansuran bulanan' },
        { icon: '\U0001f3e0', name: 'Loan Rumah', href: '/kalkulator/loan-rumah/', desc: 'Kelayakan & ansuran' },
        { icon: '\U0001f4b0', name: 'Gaji Bersih', href: '/kalkulator/gaji-bersih/', desc: 'EPF + SOCSO + PCB' },
        { icon: '\U0001f9fe', name: 'Diskaun', href: '/kalkulator/diskaun/', desc: 'Harga selepas diskaun' },
        { icon: '\U0001f9ee', name: 'Lagi Alat', href: '/kalkulator/', desc: '20+ kalkulator \u2192' },
      ].map(calc => (
        <a href={calc.href} class="rounded-xl bg-white dark:bg-slate-800/80 border border-gray-100 dark:border-slate-700/50 p-4 sm:p-5 hover:border-blue-200 dark:hover:border-blue-800/50 hover:shadow-md transition-all hover:-translate-y-0.5 group">
          <span class="text-2xl sm:text-3xl block mb-2">{calc.icon}</span>"""

# Since the actual emoji bytes might not match, let me do a different approach.
# Find and replace blocks by known structure instead

def replace_block(content, marker, new_block):
    """Replace from marker to next ].map(calc => using new content"""
    idx = content.find(marker)
    if idx < 0:
        return content, False
    
    # Find the ].map(calc => ( part  
    end_marker = "].map(calc => ("
    end_idx = content.find(end_marker, idx)
    if end_idx < 0:
        return content, False
    
    # Find the starting <a tag
    a_idx = content.find('<a href={calc.href}', end_idx)
    if a_idx < 0:
        return content, False
    
    # Find next line after
    nl = content.find('\n', a_idx)
    
    before = content[:idx]
    after = content[nl:]
    
    return before + new_block + after, True

# Actually, let me do it the simple way - just find unique identifying strings
# and do the replacements directly

# Replace calc grid (the one with 🏦 as first item)
# Need unique context
marker1 = "{ icon: '\U0001f3e6', name: 'KWSP'"
if marker1 in c:
    print("Found 🏦 marker")
    
    # Find the whole block from { icon: to ].map(calc => (
    start = c.find(marker1)
    # Go back to start of line
    line_start = c.rfind('\n', 0, start) + 1
    # Find the ].map(calc =>
    map_end = c.find("].map(calc => (", start)
    if map_end >= 0:
        map_end = c.find('\n', map_end) + 1
        
        new_grid = """        { icon: 'K', name: 'KWSP', href: '/kalkulator/kwsp/', desc: 'Caruman & dividen', bg: 'from-blue-500 to-blue-600' },
        { icon: 'A', name: 'ASB', href: '/kalkulator/asb/', desc: 'Dividen & bonus', bg: 'from-indigo-500 to-indigo-600' },
        { icon: 'E', name: 'Emas', href: '/kalkulator/emas/', desc: 'Harga emas semasa', bg: 'from-amber-500 to-amber-600' },
        { icon: 'K', name: 'Kereta', href: '/kalkulator/kereta/', desc: 'Ansuran bulanan', bg: 'from-cyan-500 to-cyan-600' },
        { icon: 'R', name: 'Loan Rumah', href: '/kalkulator/loan-rumah/', desc: 'Kelayakan & ansuran', bg: 'from-teal-500 to-teal-600' },
        { icon: 'G', name: 'Gaji Bersih', href: '/kalkulator/gaji-bersih/', desc: 'EPF + SOCSO + PCB', bg: 'from-emerald-500 to-emerald-600' },
        { icon: 'D', name: 'Diskaun', href: '/kalkulator/diskaun/', desc: 'Harga selepas diskaun', bg: 'from-violet-500 to-violet-600' },
        { icon: '+', name: 'Lagi Alat', href: '/kalkulator/', desc: '20+ kalkulator \u2192', bg: 'from-slate-500 to-slate-600' },
      ].map(calc => (
        <a href={calc.href} class="rounded-xl bg-white dark:bg-slate-800/80 border border-gray-100 dark:border-slate-700/50 p-4 sm:p-5 hover:border-blue-200 dark:hover:border-blue-800/50 hover:shadow-md transition-all hover:-translate-y-0.5 group">
          <span class={`w-8 h-8 rounded-lg bg-gradient-to-br ${calc.bg} flex items-center justify-center text-white text-xs font-bold shadow-sm mb-2.5`}>{calc.icon}</span>
"""
        
        c = c[:line_start] + new_grid + c[map_end:]
        print("Calculator grid updated!")
else:
    print("Marker not found in exact form, checking bytes...")
    # Check what the actual bytes are
    for i in range(len(c)):
        if c[i:i+6] == '{ icon':
            snippet = c[i:i+60]
            # Check if it has emoji
            for ch in snippet:
                if ord(ch) > 0x1F300:
                    print(f"Found emoji at offset {i}: U+{ord(ch):04X}")
                    print(repr(snippet))
                    break

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
