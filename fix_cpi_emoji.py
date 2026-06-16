"""Clean emojis from CPI page - precise line-by-line approach"""
path = r'C:\Users\irfan\rakyathub\src\pages\inflasi-malaysia.astro'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0
for i, line in enumerate(lines):
    if '📊 CPI' in line:
        lines[i] = line.replace('📊 CPI', 'CPI')
        changes += 1
    if '🔥 Inflasi' in line:
        lines[i] = line.replace('🔥 Inflasi', 'Inflasi')
        changes += 1
    if '📈 ' in line and 'tahun data' in line:
        lines[i] = line.replace('📈 ', '')
        changes += 1
    if '📈 Indeks Harga' in line:
        lines[i] = line.replace('📈 Indeks Harga', 'Indeks Harga')
        changes += 1
    if '🏷️ CPI Ikut' in line:
        lines[i] = line.replace('🏷️ CPI Ikut', 'CPI Ikut')
        changes += 1
    if '🧮 Kira Nilai' in line:
        lines[i] = line.replace('🧮 Kira Nilai', 'Kira Nilai')
        changes += 1

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"CPI page: {changes} emojis cleaned")
