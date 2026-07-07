import json
import urllib.request
import os
from datetime import datetime, timezone, timedelta
from collections import Counter

TOKEN = "b1e7edf54fbb44107eb5ff5aac0d1fed0132bf755acada2c"
URL = "https://www.advancedgsc.com/api/mcp"

def call_mcp(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(URL, data=payload, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    })
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())

# Fetch query+page data
print("Fetching query+page data...")
qp_data = call_mcp("tools/call", {
    "name": "get_search_analytics",
    "arguments": {
        "site_url": "sc-domain:rakyathub.my",
        "days": 30,
        "dimensions": "query,page",
        "row_limit": 100
    }
})
qp_text = qp_data['result']['content'][0]['text']
qp_lines = qp_text.strip().split('\n')
qp_rows = qp_lines[4:]  # skip headers

print(f"Got {len(qp_rows)} query+page rows")

# Fetch query-only data
print("Fetching query-only data...")
q_data = call_mcp("tools/call", {
    "name": "get_search_analytics",
    "arguments": {
        "site_url": "sc-domain:rakyathub.my",
        "days": 30,
        "dimensions": "query",
        "row_limit": 100
    }
})
q_text = q_data['result']['content'][0]['text']
q_lines = q_text.strip().split('\n')
q_rows = q_lines[4:]  # skip headers

print(f"Got {len(q_rows)} query-only rows")

# Parse rows
def parse_qp_row(line):
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 6:
        return None
    return {
        "query": parts[0],
        "page": parts[1],
        "clicks": int(parts[2]),
        "impressions": int(parts[3]),
        "position": float(parts[5])
    }

def parse_q_row(line):
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 5:
        return None
    return {
        "query": parts[0],
        "clicks": int(parts[1]),
        "impressions": int(parts[2]),
        "position": float(parts[4])
    }

parsed_qp = [r for line in qp_rows if line.strip() for r in [parse_qp_row(line)] if r]
parsed_q = [r for line in q_rows if line.strip() for r in [parse_q_row(line)] if r]

print(f"\nParsed {len(parsed_qp)} query+page rows, {len(parsed_q)} query rows")

query_lookup = {r['query']: r for r in parsed_q}

# Intents and categories
BOF_KEYWORDS = ['cara', 'mohon', 'daftar', 'bayar', 'tuntut', 'semak', 
                'isi', 'renew', 'buka', 'beli', 'buat', 'baharui',
                'hidupkan', 'asingkan', 'ekstrak', 'apply']

def detect_intent(query):
    ql = query.lower()
    for kw in BOF_KEYWORDS:
        if kw in ql.split():
            return "bof"
        if ql.startswith(kw + " "):
            return "bof"
    if ql.startswith("cara "):
        return "bof"
    return "tof"

def categorize(query):
    ql = query.lower()
    if any(w in ql for w in ['harga', 'minyak', 'runcit', 'ayam', 'ikan', 'kembung', 'makanan']):
        return "harga"
    if any(w in ql for w in ['bantuan', 'kerajaan', 'selangor', 'jkm', 'oku', 'budi', 'diesel', 'roadtax', 'jpj', 'cukai jalan', 'road tax', 'renew']):
        return "kerajaan"
    if any(w in ql for w in ['gst', 'sst', 'cukai']):
        return "cukai"
    if any(w in ql for w in ['gaji', 'kerja', 'salary', 'swasta', 'pendapatan']):
        return "kerjaya"
    if any(w in ql for w in ['ptptn', 'asb', 'kwsp', 'dividen', 'zakat', 'akpk', 'bajet', 'diskaun', 'compound', 'compounding', 'refinance', 'calculator']):
        return "kewangan"
    if any(w in ql for w in ['berat', 'bmi', 'tinggi', 'badan', 'ideal', 'medical', 'kesihatan', 'pemeriksaan']):
        return "kesihatan"
    if any(w in ql for w in ['insurans', 'takaful']):
        return "insurans"
    if any(w in ql for w in ['emas']):
        return "emas"
    if any(w in ql for w in ['ai', 'suara ai', 'pdf', 'docukilat', 'split', 'asingkan', 'ekstrak']):
        return "teknologi"
    if any(w in ql for w in ['tribunal', 'aduan']):
        return "kerajaan"
    if any(w in ql for w in ['bisnes', 'business', 'startup']):
        return "bisnes"
    if any(w in ql for w in ['student', 'pelajar', 'universiti', 'matrikulasi']):
        return "student"
    return "lain-lain"

# Low hanging fruit: pos 5-15, 0 clicks
low_hanging = []
for r in parsed_qp:
    if 5 <= r['position'] <= 15 and r['clicks'] == 0:
        intent = detect_intent(r['query'])
        cat = categorize(r['query'])
        note_parts = []
        if intent == 'bof':
            note_parts.append("BOF — orang nak cari cara/tindakan")
        else:
            note_parts.append("TOF — informational query")
        note_parts.append(f"pos {r['position']}, {r['impressions']} impressions, 0 clicks")
        if r['impressions'] >= 5:
            note_parts.append("banyak impression, rugi 0 clicks!")
        if r['impressions'] >= 10:
            note_parts.append("PERLU OPTIMIZE SEGERA")
        entry = {
            "query": r['query'],
            "page": r['page'],
            "clicks": r['clicks'],
            "impressions": r['impressions'],
            "position": r['position'],
            "intent": intent,
            "category": cat,
            "note": ". ".join(note_parts)
        }
        low_hanging.append(entry)

# BOF opportunities - unique queries
bof_queries_set = set()
bof_detailed = []

for r in parsed_qp:
    intent = detect_intent(r['query'])
    if intent == 'bof' and r['query'] not in bof_queries_set:
        bof_queries_set.add(r['query'])
        cat = categorize(r['query'])
        bof_detailed.append({
            "query": r['query'],
            "page": r['page'],
            "clicks": r['clicks'],
            "impressions": r['impressions'],
            "position": r['position'],
            "intent": intent,
            "category": cat,
            "note": f"BOF — orang nak cari cara/tindakan. pos {r['position']}, {r['impressions']} impressions, {r['clicks']} clicks"
        })

# Also check query-only rows for BOF
for r in parsed_q:
    intent = detect_intent(r['query'])
    if intent == 'bof' and r['query'] not in bof_queries_set:
        bof_queries_set.add(r['query'])
        cat = categorize(r['query'])
        bof_detailed.append({
            "query": r['query'],
            "page": "",
            "clicks": r['clicks'],
            "impressions": r['impressions'],
            "position": r['position'],
            "intent": intent,
            "category": cat,
            "note": f"BOF — orang nak cari cara/tindakan. pos {r['position']}, {r['impressions']} impressions, {r['clicks']} clicks"
        })

bof_detailed.sort(key=lambda x: x['impressions'], reverse=True)

# Build output JSON
now = datetime.now(timezone(timedelta(hours=8)))
output = {
    "fetched_at": now.isoformat(),
    "source": "advanced_gsc MCP - sc-domain:rakyathub.my (30 days)",
    "data_period": "2026-06-07 to 2026-07-07",
    "low_hanging_fruit": low_hanging,
    "bof_opportunities": sorted(bof_queries_set)
}

# Compare with existing
existing_path = 'C:\\Users\\irfan\\rakyathub\\gsc_queries.json'
if os.path.exists(existing_path):
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing = json.load(f)
    existing_lh_queries = set(lh['query'] for lh in existing.get('low_hanging_fruit', []))
    existing_bof = set(existing.get('bof_opportunities', []))
    
    new_lh = [lh for lh in low_hanging if lh['query'] not in existing_lh_queries]
    new_bof = [b for b in bof_queries_set if b not in existing_bof]
    
    print(f"\n=== COMPARISON WITH EXISTING ===")
    print(f"Existing low hanging: {len(existing_lh_queries)}")
    print(f"Existing BOF: {len(existing_bof)}")
    print(f"New low hanging: {len(new_lh)}")
    print(f"New BOF: {len(new_bof)}")
    if new_lh:
        print(f"\nNew low hanging queries:")
        for lh in new_lh:
            print(f"  \"{lh['query']}\" | {lh['category']} | pos={lh['position']} | imp={lh['impressions']}")
    if new_bof:
        print(f"\nNew BOF queries:")
        for b in new_bof:
            print(f"  \"{b}\"")
else:
    print("No existing file to compare")
    new_lh_count = len(low_hanging)
    new_bof_count = len(bof_queries_set)

# Save to file
with open(existing_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n=== SAVED TO gsc_queries.json ===")
print(f"Low hanging fruit: {len(low_hanging)} entries")
print(f"BOF opportunities: {len(bof_queries_set)} unique queries")

# Category analysis
cat_counter = Counter()
for lh in low_hanging:
    cat_counter[lh['category']] += 1
print(f"\nLow hanging fruit by category:")
for cat, count in cat_counter.most_common():
    print(f"  {cat}: {count}")

bof_cat_counter = Counter()
for b in bof_detailed:
    bof_cat_counter[b['category']] += 1
print(f"\nBOF opportunities by category:")
for cat, count in bof_cat_counter.most_common():
    print(f"  {cat}: {count}")

# Top 3 BOF
print(f"\nTop 3 BOF opportunities (most impressions):")
for b in bof_detailed[:5]:
    print(f"  \"{b['query']}\"")
    print(f"    Page: {b['page']}")
    print(f"    Position: {b['position']}, Impressions: {b['impressions']}, Clicks: {b['clicks']}")
    print(f"    Category: {b['category']}")
    print()
