"""Build all 6 new Astro calculator pages following the exact Kwsp/Asb format."""
import os

BASE = "C:/Users/irfan/rakyathub/src/pages/kalkulator"
HEAD = '---\nimport Layout from \'~/layouts/PageLayout.astro\';\nimport CallToAction from \'~/components/widgets/CallToAction.astro\';\n'
CTA_OUTRO = '\n  </CallToAction>\n  <script is:inline>\n'

TAILWIDGET = 'rounded-2xl bg-white dark:bg-slate-900/60 backdrop-blur-sm border border-gray-100 dark:border-slate-700/30 shadow-sm'
TWINPUT = 'w-full rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-base focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition'
CARD_HOVER = 'bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl p-6 card-hover'
RESULT_CELL = 'rounded-xl p-4 text-center'
CTABTN = 'inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-secondary text-white font-semibold text-sm transition-all duration-300 hover:shadow-lg hover:shadow-primary/30 hover:scale-[1.02]'

def write_page(filename, metadata_title, heading, description, calc_html, info_cards, related_articles, cta_title, cta_subtitle, cta_links, script_js):
    """Write a complete .astro page."""
    meta = 'const metadata = {\n  title: \'' + metadata_title + '\',\n};\n'
    lines = [HEAD, meta, '---\n\n', '<Layout metadata={metadata}>\n']
    lines.append('  <section class="max-w-4xl mx-auto px-4 sm:px-6 py-12 md:py-20">\n')
    lines.append('    <div class="mb-8">\n      <a href="/kalkulator" class="text-sm text-muted hover:text-primary transition-colors">\u2190 Semua Kalkulator</a>\n    </div>\n')
    lines.append('    <h1 class="text-3xl md:text-5xl font-bold tracking-tight mb-4">\n      ' + heading + '\n    </h1>\n')
    lines.append('    <p class="text-lg md:text-xl text-muted mb-8">\n      ' + description + '\n    </p>\n')
    # Calculator card
    lines.append(calc_html)
    # Info cards
    lines.append('    <div class="grid md:grid-cols-3 gap-6 mb-8">\n')
    for card in info_cards:
        lines.append('      <div class="' + CARD_HOVER + '">\n')
        lines.append('        <h3 class="font-semibold text-lg mb-2">' + card[0] + '</h3>\n')
        lines.append('        <p class="text-muted text-sm">' + card[1] + '</p>\n')
        lines.append('      </div>\n')
    lines.append('    </div>\n')
    # Related articles
    lines.append('    <div class="rounded-2xl bg-gradient-to-br from-blue-50 to-emerald-50 dark:from-slate-800 dark:to-slate-800 border border-blue-100 dark:border-slate-700 p-6 md:p-8">\n')
    lines.append('      <h3 class="text-xl font-bold mb-4">\uD83D\uDCDA Artikel Berkaitan</h3>\n')
    lines.append('      <ul class="space-y-2">\n')
    for url, text in related_articles:
        lines.append('        <li>\n')
        lines.append('          <a href="' + url + '" class="text-primary font-medium hover:underline text-sm">\u2192 ' + text + '</a>\n')
        lines.append('        </li>\n')
    lines.append('      </ul>\n')
    lines.append('    </div>\n')
    lines.append('  </section>\n')
    # CTA
    lines.append('  <CallToAction\n    actions={[\n')
    for link in cta_links:
        lines.append('      { variant: \'' + link[0] + '\', text: \'' + link[1] + '\', href: \'' + link[2] + '\' },\n')
    lines.append('    ]}\n  >\n')
    lines.append('    <Fragment slot="title">' + cta_title + '</Fragment>\n')
    lines.append('    <Fragment slot="subtitle">' + cta_subtitle + '</Fragment>\n')
    lines.append(CTA_OUTRO)
    lines.append(script_js)
    lines.append('</script>\n')
    lines.append('</Layout>\n')

    path = os.path.join(BASE, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return os.path.getsize(path)


# ============================================================
# 1. STR/SARA CHECKER
# ============================================================
str_calc = """    <div class=\"""" + TAILWIDGET + ' p-5 md:p-8 mb-8">\n'
str_calc += """      <div class="grid md:grid-cols-2 gap-4 md:gap-6">
        <div>
          <label for="st" class="block text-sm font-semibold text-default mb-1.5">Status</label>
          <select id="st" class=\"""" + TWINPUT + """">
            <option value="berkahwin">Berkahwin</option>
            <option value="bujang">Bujang</option>
            <option value="berkahwin_tidak_bekerja">Berkahwin (Isteri tdk bekerja)</option>
            <option value="warga_emas">Warga Emas 60+</option>
            <option value="bapa_tunggal">Ibu/Bapa Tunggal</option>
          </select>
        </div>
        <div>
          <label for="pd" class="block text-sm font-semibold text-default mb-1.5">Pendapatan Isi Rumah (RM/bulan)</label>
          <input type="number" id="pd" value="2500" min="0" step="100" class=\"""" + TWINPUT + """">
        </div>
        <div>
          <label for="ak" class="block text-sm font-semibold text-default mb-1.5">Bilangan Anak (bawah 18 tahun)</label>
          <input type="number" id="ak" value="2" min="0" class=\"""" + TWINPUT + """">
        </div>
        <div>
          <label for="ok" class="block text-sm font-semibold text-default mb-1.5">OKU?</label>
          <select id="ok" class=\"""" + TWINPUT + """">
            <option value="0">Tidak</option>
            <option value="1">Ya</option>
          </select>
        </div>
      </div>
      <div class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class=\"""" + RESULT_CELL + ' bg-blue-50 dark:bg-blue-900/20">\n          <p class="text-xs text-muted uppercase tracking-wide">STR</p>\n          <p class="text-lg font-bold text-default" id="hasilStr">RM 0.00</p>\n        </div>\n'
str_calc += '        <div class="' + RESULT_CELL + ' bg-emerald-50 dark:bg-emerald-900/20">\n          <p class="text-xs text-muted uppercase tracking-wide">SARA</p>\n          <p class="text-lg font-bold text-emerald-700" id="hasilSara">RM 0.00</p>\n        </div>\n'
str_calc += '        <div class="' + RESULT_CELL + ' bg-amber-50 dark:bg-amber-900/20">\n          <p class="text-xs text-muted uppercase tracking-wide">Tambahan</p>\n          <p class="text-lg font-bold text-amber-600 dark:text-amber-400" id="hasilTambahan">RM 0.00</p>\n        </div>\n'
str_calc += '        <div class="' + RESULT_CELL + ' bg-primary/10">\n          <p class="text-xs text-muted uppercase tracking-wide">Jumlah</p>\n          <p class="text-lg font-bold text-primary" id="hasilJumlah">RM 0.00</p>\n        </div>\n'
str_calc += """      </div>
      <div class="mt-6 p-5 rounded-2xl bg-gradient-to-br from-primary/10 to-secondary/5 border border-primary/20 text-center">
        <p class="text-sm text-muted" id="labelKategori">Kategori: B40 - Keluarga</p>
        <p class="text-3xl md:text-4xl font-bold text-primary" id="hasilProjected">RM 0</p>
        <p class="text-xs text-muted mt-1">*Anggaran berdasarkan Belanjawan 2025.</p>
      </div>
    </div>
    <div class=\"""" + TAILWIDGET + ' p-5 md:p-8 mb-8">\n      <h2 class="text-xl font-bold mb-4">\uD83D\uDCCA Pecahan Bantuan</h2>\n      <div class="overflow-x-auto -mx-5 md:-mx-0">\n        <div class="min-w-[400px] px-5 md:px-0">\n          <table class="w-full text-sm">\n            <thead>\n              <tr class="border-b border-gray-100 dark:border-slate-700">\n                <th class="text-left py-3 px-2 font-semibold text-muted">Komponen</th>\n                <th class="text-right py-3 px-2 font-semibold text-muted">Jumlah (RM)</th>\n              </tr>\n            </thead>\n            <tbody id="breakdownBody"></tbody>\n          </table>\n        </div>\n      </div>\n    </div>\n'
str_calc += docukilat_cta('Perlukan Surat Rayuan Bantuan?', 'Guna DocuKilat untuk bina surat rasmi rayuan, permohonan STR dan dokumen berkaitan.')

str_cards = [
    ('\U0001f4b0 STR', 'Sumbangan Tunai Rahmah — bantuan tunai langsung kepada isi rumah B40 dan M40.'),
    ('\U0001f7e6 SARA', 'Sumbangan Asas Rahmah — bantuan tambahan untuk keperluan asas dan barangan keperluan.'),
    ('\U0001f4ca Kelayakan', 'Kelayakan berdasarkan pendapatan isi rumah, bilangan anak, OKU dan status perkahwinan.'),
]
str_articles = [
    ('/info-tuntutan-bantuan-rm100-mykad-subsidi-ron95-kemas-kini/', 'Info Bantuan RM100 MyKad & Subsidi RON95'),
    ('/cadangan-bajet-50-30-20-di-malaysia/', 'Bajet 50/30/20 — Cara Urus Wang Dengan Bijak'),
    ('/cara-simpan-duit-gaji-rm2500/', 'Cara Simpan Duit Gaji RM2,500 Sebulan'),
]
str_cta_links = [
    ('primary', 'Kalkulator Gaji Bersih', '/kalkulator/gaji-bersih'),
    ('secondary', 'Kalkulator SST', '/kalkulator/sst'),
]

str_js = '''function fmt(v) { return 'RM ' + (typeof v === 'number' && !isNaN(v) && isFinite(v) ? v.toLocaleString('ms-MY', {minimumFractionDigits:2,maximumFractionDigits:2}) : '0.00'); }
function sn(v, d) { var n = parseFloat(v); return (!isNaN(n) && isFinite(n) && n >= 0) ? n : (d || 0); }
function calc() {
  var st = document.getElementById('st').value;
  var pd = sn(document.getElementById('pd').value, 2500);
  var ak = parseInt(document.getElementById('ak').value) || 0;
  var ok = parseInt(document.getElementById('ok').value) || 0;
  var sA=0, rA=0, cat='';
  if(pd<1000) {
    if(st==='bujang'){sA=1200;cat='B40 - Bujang'}
    else if(st==='warga_emas'||st==='bapa_tunggal'){sA=3000;cat='B40 - Warga Emas/Tunggal'}
    else{sA=3700;cat='B40 - Keluarga';} rA=1200;
  } else if(pd<2000) {
    if(st==='bujang'){sA=900;cat='B40 - Bujang'}
    else if(st==='warga_emas'||st==='bapa_tunggal'){sA=2000;cat='B40 - Warga Emas/Tunggal'}
    else{sA=2500;cat='B40 - Keluarga';} rA=900;
  } else if(pd<3000) {
    if(st==='bujang'){sA=600;cat='B40 - Bujang'}
    else if(st==='warga_emas'||st==='bapa_tunggal'){sA=1500;cat='B40 - Warga Emas/Tunggal'}
    else{sA=2000;cat='B40 - Keluarga';} rA=600;
  } else if(pd<5000) {
    if(st==='bujang'){sA=300;cat='M40 - Bujang'}else{sA=1000;cat='M40 - Keluarga';} rA=300;
  } else {
    if(st==='bujang'){sA=150;cat='M40 - Bujang'}else{sA=500;cat='M40 - Keluarga';} rA=0;
  }
  var ea = (ak>0 && pd<3000) ? Math.min(ak*100,500) : 0;
  var eo = ok ? 300 : 0;
  var total = sA + rA + ea + eo;
  document.getElementById('hasilStr').textContent = fmt(sA);
  document.getElementById('hasilSara').textContent = fmt(rA);
  document.getElementById('hasilTambahan').textContent = fmt(ea+eo);
  document.getElementById('hasilJumlah').textContent = fmt(total);
  document.getElementById('hasilProjected').textContent = fmt(total);
  document.getElementById('labelKategori').textContent = 'Kategori: ' + cat + ' | Anggaran: RM ' + Math.round(total/12).toLocaleString() + '/bulan';
  var tb = document.getElementById('breakdownBody'); var fr = document.createDocumentFragment();
  var items = [
    {l:'STR (Sumbangan Tunai Rahmah)', v:sA}, {l:'SARA (Sumbangan Asas Rahmah)', v:rA},
    {l:'Tambahan Anak ('+ak+' orang)', v:ea}, {l:'Tambahan OKU', v:eo}
  ];
  items.forEach(function(i){ var tr=document.createElement('tr'); tr.className='border-b border-gray-50 dark:border-slate-800';
    var td1=document.createElement('td'); td1.className='py-2.5 px-2'; td1.textContent=i.l;
    var td2=document.createElement('td'); td2.className='text-right py-2.5 px-2 text-primary font-medium'; td2.textContent=fmt(i.v);
    tr.appendChild(td1); tr.appendChild(td2); fr.appendChild(tr);
  });
  var tr=document.createElement('tr'); tr.className='font-bold bg-primary/5';
  var td1=document.createElement('td'); td1.className='py-2.5 px-2'; td1.textContent='JUMLAH';
  var td2=document.createElement('td'); td2.className='text-right py-2.5 px-2 text-primary'; td2.textContent=fmt(total);
  tr.appendChild(td1); tr.appendChild(td2); fr.appendChild(tr);
  tb.textContent=''; tb.appendChild(fr);
}
['st','pd','ak','ok'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calc);el.addEventListener('change',calc);}});
calc();'''

print("1. str-sara.astro:", write_page('str-sara.astro', 'STR & SARA Checker — Semak Bantuan Kerajaan',
    'STR &amp; SARA Checker', 'Semak anggaran bantuan STR dan SARA berdasarkan pendapatan isi rumah.',
    str_calc, str_cards, str_articles, 'Nak Kira Gaji Bersih', 'Semua kalkulator percuma', str_cta_links, str_js), "bytes")
