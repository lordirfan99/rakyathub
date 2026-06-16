"""Clean remaining emojis across site"""
import os

# Bantuan page
path = r'C:\Users\irfan\rakyathub\src\pages\bantuan-kerajaan.astro'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('🇲🇾 Bantuan Kerajaan Malaysia 2026', 'Bantuan Kerajaan Malaysia 2026')
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Bantuan page: cleaned flag emoji")

# SinglePost article widgets
path = r'C:\Users\irfan\rakyathub\src\components\blog\SinglePost.astro'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Harga Barang Runcit Malaysia' in line and "h3" in line:
        lines[i] = line.replace("Harga Barang Runcit Malaysia", "Harga Barang Runcit")
    if '📊 Lihat Semua Harga Terkini' in line:
        lines[i] = line.replace("📊 Lihat Semua Harga Terkini", "Lihat Semua Harga Terkini")
    if '📈 Semak Data Inflasi Penuh' in line:
        lines[i] = line.replace("📈 Semak Data Inflasi Penuh", "Semak Data Inflasi Penuh")
    if '🔥 Inflasi' in line and 'red-500' in line:
        lines[i] = line.replace("🔥 Inflasi", "Inflasi")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Article widgets: cleaned emojis")

# Homepage - fix food stats line (remaining emojis)
path = r'C:\Users\irfan\rakyathub\src\pages\index.astro'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '📊 <span class="font-semibold' in line:
        lines[i] = line.replace('📊 ', '')
    if '📦 <span class="font-semibold' in line:
        lines[i] = line.replace('📦 ', '')
    if '🛒 Harga Makanan' in line:
        lines[i] = line.replace('🛒 Harga Makanan', 'Harga Makanan')
    if '📊 Kalkulator' in line:
        lines[i] = line.replace('📊 Kalkulator', 'Kalkulator')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Homepage: remaining stat emojis cleaned")
print("All done!")
