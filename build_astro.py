import os

D = 'C:/Users/irfan/rakyathub/src/pages/kalkulator'

def w(fname, content):
    with open(os.path.join(D, fname), 'w', encoding='utf-8') as f:
        f.write(content)
    sz = os.path.getsize(os.path.join(D, fname))
    print(f'  {fname}: {sz} bytes')
    return sz

# ============================================================
# UTILITY HELPERS
# ============================================================
IMPORTS = '---\nimport Layout from \'~/layouts/PageLayout.astro\';\nimport CallToAction from \'~/components/widgets/CallToAction.astro\';\n'

TW = 'w-full rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-base focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition'
TW_SEL = TW

DOCU_CTA = '''    <div class="rounded-2xl bg-gradient-to-br from-primary/10 via-primary/[0.03] to-secondary/10 border border-primary/20 p-6 md:p-8 text-center mb-8">
      <h3 class="text-xl md:text-2xl font-bold mb-2">{title}</h3>
      <p class="text-muted mb-4">{subtitle}</p>
      <a href="https://docukilat.netlify.app" target="_blank" rel="noopener noreferrer"
        class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-secondary text-white font-semibold text-sm transition-all duration-300 hover:shadow-lg hover:shadow-primary/30 hover:scale-[1.02]">
        Bina Dokumen di DocuKilat
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
        </svg>
      </a>
    </div>'''

CTA_TEMPLATE = '''  <CallToAction
    actions={[
{actions}
    ]}
  >
    <Fragment slot="title">{title}</Fragment>
    <Fragment slot="subtitle">{subtitle}</Fragment>
  </CallToAction>'''

JS_FMT = """function fmt(v) { return 'RM ' + (typeof v === 'number' && !isNaN(v) && isFinite(v) ? v.toLocaleString('ms-MY', {minimumFractionDigits:2,maximumFractionDigits:2}) : '0.00'); }
function sn(v, d) { var n = parseFloat(v); return (!isNaN(n) && isFinite(n) && n >= 0) ? n : (d || 0); }
"""

INFOCARD = '''      <div class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl p-6 card-hover">
        <h3 class="font-semibold text-lg mb-2">{title}</h3>
        <p class="text-muted text-sm">{desc}</p>
      </div>'''

ARTIKEL = '''        <li>
          <a href="{url}" class="text-primary font-medium hover:underline text-sm">{text}</a>
        </li>'''

def page(fname, meta_title, heading, desc, calculator_html, info_cards, cta_title, cta_subtitle, cta_actions, script_js, related=None):
    parts = [IMPORTS]
    parts.append(f'\nconst metadata = {{\n  title: \'{meta_title}\',\n}};\n')
    parts.append('---\n\n<Layout metadata={metadata}>\n')
    parts.append('  <section class="max-w-4xl mx-auto px-4 sm:px-6 py-12 md:py-20">\n')
    parts.append('    <div class="mb-8"><a href="/kalkulator" class="text-sm text-muted hover:text-primary transition-colors">\u2190 Semua Kalkulator</a></div>\n')
    parts.append(f'    <h1 class="text-3xl md:text-5xl font-bold tracking-tight mb-4">{heading}</h1>\n')
    parts.append(f'    <p class="text-lg md:text-xl text-muted mb-8">{desc}</p>\n')
    parts.append(calculator_html)
    # Info cards
    parts.append('    <div class="grid md:grid-cols-3 gap-6 mb-8">\n')
    for ic in info_cards:
        parts.append(INFOCARD.replace('{title}', ic[0]).replace('{desc}', ic[1]))
    parts.append('    </div>\n')
    # Related articles
    if related:
        parts.append('    <div class="rounded-2xl bg-gradient-to-br from-blue-50 to-emerald-50 dark:from-slate-800 dark:to-slate-800 border border-blue-100 dark:border-slate-700 p-6 md:p-8">\n')
        parts.append('      <h3 class="text-xl font-bold mb-4">Artikel Berkaitan</h3>\n')
        parts.append('      <ul class="space-y-2">\n')
        for url, text in related:
            parts.append(ARTIKEL.replace('{url}', url).replace('{text}', text))
        parts.append('      </ul>\n    </div>\n')
    parts.append('  </section>\n')
    # CTA
    acts = ''
    for variant, text, href in cta_actions:
        acts += f"      {{ variant: '{variant}', text: '{text}', href: '{href}' }},\n"
    parts.append(CTA_TEMPLATE.replace('{actions}', acts).replace('{title}', cta_title).replace('{subtitle}', cta_subtitle))
    parts.append('  <script is:inline>\n')
    parts.append(script_js)
    parts.append('\n</script>\n</Layout>\n')
    return w(fname, ''.join(parts))


print('=== Building 6 calculator pages ===')

# ============================================================
# 1. STR/SARA CHECKER
# ============================================================
str_calc = f'''    <div class="rounded-2xl bg-white dark:bg-slate-900/60 backdrop-blur-sm border border-gray-100 dark:border-slate-700/30 shadow-sm p-5 md:p-8 mb-8">
      <div class="grid md:grid-cols-2 gap-4 md:gap-6">
        <div>
          <label for="st" class="block text-sm font-semibold text-default mb-1.5">Status</label>
          <select id="st" class="{TW_SEL}">
            <option value="berkahwin">Berkahwin</option>
            <option value="bujang">Bujang</option>
            <option value="berkahwin_tidak_bekerja">Berkahwin (Isteri tdk bekerja)</option>
            <option value="warga_emas">Warga Emas 60+</option>
            <option value="bapa_tunggal">Ibu/Bapa Tunggal</option>
          </select>
        </div>
        <div>
          <label for="pd" class="block text-sm font-semibold text-default mb-1.5">Pendapatan Isi Rumah (RM/bulan)</label>
          <input type="number" id="pd" value="2500" min="0" step="100" class="{TW}">
        </div>
        <div>
          <label for="ak" class="block text-sm font-semibold text-default mb-1.5">Bilangan Anak (bawah 18 tahun)</label>
          <input type="number" id="ak" value="2" min="0" class="{TW}">
        </div>
        <div>
          <label for="ok" class="block text-sm font-semibold text-default mb-1.5">OKU?</label>
          <select id="ok" class="{TW_SEL}">
            <option value="0">Tidak</option>
            <option value="1">Ya</option>
          </select>
        </div>
      </div>
      <div class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="rounded-xl bg-blue-50 dark:bg-blue-900/20 p-4 text-center">
          <p class="text-xs text-muted uppercase tracking-wide">STR</p>
          <p class="text-lg font-bold text-default" id="hasilStr">RM 0.00</p>
        </div>
        <div class="rounded-xl bg-emerald-50 dark:bg-emerald-900/20 p-4 text-center">
          <p class="text-xs text-muted uppercase tracking-wide">SARA</p>
          <p class="text-lg font-bold text-emerald-700" id="hasilSara">RM 0.00</p>
        </div>
        <div class="rounded-xl bg-amber-50 dark:bg-amber-900/20 p-4 text-center">
          <p class="text-xs text-muted uppercase tracking-wide">Tambahan</p>
          <p class="text-lg font-bold text-amber-600" id="hasilTambahan">RM 0.00</p>
        </div>
        <div class="rounded-xl bg-primary/10 p-4 text-center">
          <p class="text-xs text-muted uppercase tracking-wide">Jumlah</p>
          <p class="text-lg font-bold text-primary" id="hasilJumlah">RM 0.00</p>
        </div>
      </div>
      <div class="mt-6 p-5 rounded-2xl bg-gradient-to-br from-primary/10 to-secondary/5 border border-primary/20 text-center">
        <p class="text-sm text-muted" id="labelKategori">Kategori: B40 - Keluarga</p>
        <p class="text-3xl md:text-4xl font-bold text-primary" id="hasilProjected">RM 0</p>
        <p class="text-xs text-muted mt-1">*Anggaran berdasarkan Belanjawan 2025.</p>
      </div>
    </div>
    <div class="rounded-2xl bg-white dark:bg-slate-900/60 border border-gray-100 dark:border-slate-700/30 shadow-sm p-5 md:p-8 mb-8">
      <h2 class="text-xl font-bold mb-4">Pecahan Bantuan</h2>
      <div class="overflow-x-auto -mx-5 md:-mx-0">
        <div class="min-w-[400px] px-5 md:px-0">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100 dark:border-slate-700">
                <th class="text-left py-3 px-2 font-semibold text-muted">Komponen</th>
                <th class="text-right py-3 px-2 font-semibold text-muted">Jumlah (RM)</th>
              </tr>
            </thead>
            <tbody id="breakdownBody"></tbody>
          </table>
        </div>
      </div>
    </div>
''' + DOCU_CTA.replace('{title}', 'Perlukan Surat Rayuan Bantuan?').replace('{subtitle}', 'Guna DocuKilat untuk bina surat rasmi rayuan bantuan kerajaan, permohonan STR dan dokumen berkaitan.')

str_info = [
    ('STR', 'Sumbangan Tunai Rahmah — bantuan tunai langsung kepada isi rumah B40 dan M40.'),
    ('SARA', 'Sumbangan Asas Rahmah — bantuan tambahan untuk keperluan asas.'),
    ('Kelayakan', 'Berdasarkan pendapatan isi rumah, bilangan anak, OKU dan status perkahwinan.'),
]

str_related = [
    ('/info-tuntutan-bantuan-rm100-mykad-subsidi-ron95-kemas-kini/', 'Info Bantuan RM100 MyKad & Subsidi RON95'),
    ('/cadangan-bajet-50-30-20-di-malaysia/', 'Bajet 50/30/20 — Cara Urus Wang Dengan Bijak'),
    ('/cara-simpan-duit-gaji-rm2500/', 'Cara Simpan Duit Gaji RM2,500 Sebulan'),
]

str_js = JS_FMT + """function calc() {
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
  var tb = document.getElementById('breakdownBody');
  var fr = document.createDocumentFragment();
  var items = [{l:'STR (Sumbangan Tunai Rahmah)',v:sA},{l:'SARA (Sumbangan Asas Rahmah)',v:rA},{l:'Tambahan Anak ('+ak+' orang)',v:ea},{l:'Tambahan OKU',v:eo}];
  items.forEach(function(i){
    var tr=document.createElement('tr'); tr.className='border-b border-gray-50 dark:border-slate-800';
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
calc();"""

page('str-sara.astro', 'STR & SARA Checker — Semak Bantuan Kerajaan',
     'STR &amp; SARA Checker', 'Semak anggaran bantuan STR dan SARA berdasarkan pendapatan isi rumah.',
     str_calc, str_info, 'Nak Kira Gaji Bersih atau SST?', 'Semua kalkulator percuma — guna sekarang.',
     [('primary', 'Kalkulator Gaji Bersih', '/kalkulator/gaji-bersih'), ('secondary', 'Kalkulator SST', '/kalkulator/sst')],
     str_js, related=str_related)

print('=== STR/SARA done ===')
