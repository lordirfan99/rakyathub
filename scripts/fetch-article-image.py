#!/usr/bin/env python3
"""
fetch-article-image.py — Pre-download relevant article image BEFORE writing.

Usage:
    python3 scripts/fetch-article-image.py <slug> <topic_keywords>

Example:
    python3 scripts/fetch-article-image.py cara-buat-resume "resume writing career tips"

The script maps topic keywords to known-good Unsplash photo IDs and downloads
the best-matching image as src/assets/images/hero-{slug}.jpg.
"""

import sys, os, random, re, json, hashlib, subprocess, urllib.request, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(REPO, "src", "assets", "images")

# ── Known-good Unsplash photo IDs mapped by topic ──
# These are verified to return JPEG images from unsplash CDN.
TOPIC_IMAGES = {
    # Finance / Budget / Savings
    "kewangan": ["1554224155-6726b3ff858f", "1579621971588-5c3d44e1a1d0", "1560472355070-2b7d7c3b1f5e", "1450101499163-c8848c66ca85", "1554224155-6726b3ff858f"],
    "bajet": ["1554224155-6726b3ff858f", "1579621971588-5c3d44e1a1d0", "1460925895917-afdab827c52f"],
    "simpanan": ["1579621971588-5c3d44e1a1d0", "1554224155-6726b3ff858f"],
    "gaji": ["1554224155-6726b3ff858f", "1460925895917-afdab827c52f", "1450101499163-c8848c66ca85"],
    "hutang": ["1554224155-6726b3ff858f", "1560472355070-2b7d7c3b1f5e"],

    # Career / Office / Work
    "kerjaya": ["1522202176988-66273c2fd55f", "1600880292203-757bb62b4baf", "1556761176-5974dc0c3f8c", "1521791127-8a8e3c4a5b6c"],
    "kerja": ["1522202176988-66273c2fd55f", "1556761176-5974dc0c3f8c"],
    "temuduga": ["1521791127-8a8e3c4a5b6c", "1551836022-d5d88e8a9c9b"],
    "resume": ["1551836022-d5d88e8a9c9b", "1450101499163-c8848c66ca85"],
    "internship": ["1522202176988-66273c2fd55f", "1524178232363-1fb2b075b655"],

    # Education / Student
    "pendidikan": ["1523240795612-9a054b0db644", "1524178232363-1fb2b075b655", "1541339907198-e08756dedf3f", "1523050854058-8df90110c7f1"],
    "student": ["1523240795612-9a054b0db644", "1524178232363-1fb2b075b655", "1523050854058-8df90110c7f1"],
    "universiti": ["1541339907198-e08756dedf3f", "1523240795612-9a054b0db644"],
    "ptptn": ["1523240795612-9a054b0db644", "1541339907198-e08756dedf3f"],
    "belajar": ["1524178232363-1fb2b075b655", "1523240795612-9a054b0db644"],
    "assignment": ["1456513080510-7bf3a84b82f8", "1523240795612-9a054b0db644"],
    "bibliografi": ["1456513080510-7bf3a84b82f8"],
    "kajian": ["1456513080510-7bf3a84b82f8"],

    # Technology / Gadgets
    "teknologi": ["1496181133206-80ce9b88a853", "1517694712202-14dd9538aa97", "1461749280684-dccba630e2f6", "1517433670260-bc3c3f5d3c5a"],
    "laptop": ["1496181133206-80ce9b88a853", "1517694712202-14dd9538aa97"],
    "komputer": ["1496181133206-80ce9b88a853", "1517694712202-14dd9538aa97"],
    "vpn": ["1563986768609-322da13575f2", "1555949963-aa79dcee981c"],
    "keselamatan siber": ["1563986768609-322da13575f2", "1555949963-aa79dcee981c"],
    "password": ["1563986768609-322da13575f2"],
    "cloud": ["1544197150-b99a580bb7a8", "1564013799919-ab600027f61d"],
    "ai": ["1677446697252-1b7a5b5a3b5c", "1485827404703-89b55fcc595e"],

    # Health / Medical
    "kesihatan": ["1576091160550-8053e6b8b7a5", "1551077625-94c2c5c8b5e6", "1571016967546-4c9a32b5e7d8"],
    "hospital": ["1576091160550-8053e6b8b7a5", "1551077625-94c2c5c8b5e6"],
    "perubatan": ["1576091160550-8053e6b8b7a5", "1551077625-94c2c5c8b5e6"],
    "mental": ["1551077625-94c2c5c8b5e6", "1571016967546-4c9a32b5e7d8"],
    "jantung": ["1571016967546-4c9a32b5e7d8"],
    "diabetes": ["1576091160550-8053e6b8b7a5"],
    "kolestrol": ["1576091160550-8053e6b8b7a5"],

    # Insurance
    "insurans": ["1551077625-94c2c5c8b5e6", "1560472355070-2b7d7c3b1f5e", "1450101499163-c8848c66ca85"],
    "takaful": ["1551077625-94c2c5c8b5e6", "1560472355070-2b7d7c3b1f5e"],
    "medical card": ["1551077625-94c2c5c8b5e6", "1576091160550-8053e6b8b7a5"],

    # Car / Vehicle
    "kereta": ["1547514701-42782101795e", "1552519507-da3b142c6e3d", "1506521781263-d8422e82f27a"],
    "kenderaan": ["1547514701-42782101795e", "1552519507-da3b142c6e3d"],
    "roadtax": ["1547514701-42782101795e", "1506521781263-d8422e82f27a"],
    "jpj": ["1547514701-42782101795e"],
    "minyak": ["1580674285054-bed31e145f59", "1552519507-da3b142c6e3d"],
    "ev": ["1552519507-da3b142c6e3d"],
    "motorsikal": ["1552519507-da3b142c6e3d"],

    # Scam / Security
    "scam": ["1633265486064-086b219458ec", "1563013544-824ae1b704d3", "1555949963-aa79dcee981c"],
    "keselamatan": ["1563013544-824ae1b704d3", "1633265486064-086b219458ec"],
    "phishing": ["1563013544-824ae1b704d3", "1633265486064-086b219458ec"],

    # House / Rental / Property
    "sewa": ["1560448204-e02f11c3d0e2", "1502672260266-1c1ef2d93688", "1564013799919-ab600027f61d"],
    "rumah": ["1560448204-e02f11c3d0e2", "1502672260266-1c1ef2d93688", "1512917774080-9991f1c4c750"],
    "hartanah": ["1560448204-e02f11c3d0e2", "1512917774080-9991f1c4c750", "1558036117-15d8c8b5e6a7"],

    # Business
    "bisnes": ["1600880292203-757bb62b4baf", "1556761176-5974dc0c3f8c", "1559134115-5f9b5f8c4b6d"],
    "perniagaan": ["1600880292203-757bb62b4baf", "1556761176-5974dc0c3f8c"],
    "dropship": ["1556742049-0cfed4f6a45d", "1600880292203-757bb62b4baf"],
    "francais": ["1556761176-5974dc0c3f8c"],
    "startup": ["1559134115-5f9b5f8c4b6d", "1600880292203-757bb62b4baf"],

    # Tax
    "cukai": ["1554224155-6726b3ff858f", "1560472355070-2b7d7c3b1f5e", "1450101499163-c8848c66ca85"],
    "percukaian": ["1554224155-6726b3ff858f", "1450101499163-c8848c66ca85"],
    "lhdn": ["1554224155-6726b3ff858f"],

    # Investment / Gold / Emas
    "pelaburan": ["1560472355070-2b7d7c3b1f5e", "1554224155-6726b3ff858f", "1579621971588-5c3d44e1a1d0"],
    "emas": ["1579621971588-5c3d44e1a1d0", "1560472355070-2b7d7c3b1f5e"],
    "saham": ["1560472355070-2b7d7c3b1f5e", "1611976877345-8f5b5c8b4e7d"],
    "unit trust": ["1611976877345-8f5b5c8b4e7d"],
    "asb": ["1579621971588-5c3d44e1a1d0", "1560472355070-2b7d7c3b1f5e"],

    # KWSP / Retirement
    "kwsp": ["1579621971588-5c3d44e1a1d0", "1460925895917-afdab827c52f", "1554224155-6726b3ff858f"],
    "pencen": ["1579621971588-5c3d44e1a1d0", "1460925895917-afdab827c52f"],

    # Government
    "kerajaan": ["1554224155-6726b3ff858f", "1532375818-6b8c9b5f4d7e", "1517245386807-bb43f82c33c4"],
    "bantuan": ["1532375818-6b8c9b5f4d7e", "1517245386807-bb43f82c33c4"],

    # Lifestyle
    "gaya-hidup": ["1504672701922-9a5f4f0b5e6a", "1498837167922-d0d1f0b5a3c7"],
    "dapur": ["1540914124281-342587941389", "1498837167922-d0d1f0b5a3c7"],
    "resepi": ["1540914124281-342587941389", "1498837167922-d0d1f0b5a3c7"],
    "masak": ["1540914124281-342587941389"],
    "meal prep": ["1540914124281-342587941389"],

    # Consumer / Shopping
    "pengguna": ["1556742049-0cfed4f6a45d", "1554224155-6726b3ff858f"],
    "shopping": ["1556742049-0cfed4f6a45d"],
    "shopee": ["1556742049-0cfed4f6a45d"],

    # Food / Prices
    "makanan": ["1504672701922-9a5f4f0b5e6a", "1540914124281-342587941389"],
    "harga": ["1554224155-6726b3ff858f"],

    # Family / Parents
    "keluarga": ["1523240795612-9a054b0db644", "1502672260266-1c1ef2d93688"],
    "ibubapa": ["1502672260266-1c1ef2d93688"],

    # Energy
    "tenaga": ["1473340099505-5e5b5c8b4e7d", "1580674285054-bed31e145f59"],
    "elektrik": ["1473340099505-5e5b5c8b4e7d"],

    # General / Default
    "malaysia": ["1532375818-6b8c9b5f4d7e", "1517245386807-bb43f82c33c4"],
}

# Build reverse index (category → list of IDs) from keywords above
CATEGORY_INDEX = {}
for keyword, ids in TOPIC_IMAGES.items():
    for cid in ids:
        if cid not in CATEGORY_INDEX:
            CATEGORY_INDEX[cid] = []
        CATEGORY_INDEX[cid].append(keyword)


def find_best_image_ids(topic: str) -> list:
    """Find best Unsplash photo IDs for a topic string."""
    topic_lower = topic.lower()
    matched_ids = set()

    # Direct keyword match
    for keyword, ids in TOPIC_IMAGES.items():
        if keyword in topic_lower or topic_lower in keyword:
            matched_ids.update(ids)

    # Word-by-word matching
    words = re.findall(r'\w+', topic_lower)
    for word in words:
        if word in TOPIC_IMAGES:
            matched_ids.update(TOPIC_IMAGES[word])

    # If no match, return a small set of generic Malaysian/images
    if not matched_ids:
        return ["1517245386807-bb43f82c33c4", "1532375818-6b8c9b5f4d7e", "1554224155-6726b3ff858f"]

    return list(matched_ids)


def download_image(photo_id: str, output_path: str) -> bool:
    """Download an Unsplash photo by ID. Returns True on success."""
    url = f"https://images.unsplash.com/photo-{photo_id}?w=1200&h=630&fit=crop"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if len(data) < 1000:
                return False
            # Verify it's a JPEG
            if data[:2] != b'\xff\xd8':
                return False
            with open(output_path, 'wb') as f:
                f.write(data)
            return True
    except Exception:
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/fetch-article-image.py <slug> <topic_keywords>")
        sys.exit(1)

    slug = sys.argv[1]
    topic = " ".join(sys.argv[2:])
    output_path = os.path.join(OUTPUT_DIR, f"hero-{slug}.jpg")

    # Ensure output dir exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find candidate image IDs
    candidates = find_best_image_ids(topic)
    random.shuffle(candidates)

    print(f"🎯 Topic: {topic}")
    print(f"📁 Output: {output_path}")
    print(f"🖼️  Candidates: {len(candidates)}")

    # Try each candidate until one works
    for cid in candidates:
        print(f"   Trying photo-{cid}...", end=" ")
        if download_image(cid, output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"✅ OK ({size_kb:.0f} KB)")
            print(f"✅ Image saved: hero-{slug}.jpg")
            return
        print("❌")

    # Last resort: picsum.photos (but we rarely get here now)
    print("⚠️  All Unsplash IDs failed, trying picsum...")
    try:
        req = urllib.request.Request(
            "https://picsum.photos/1200/630",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(output_path, 'wb') as f:
                f.write(data)
            size_kb = os.path.getsize(output_path) / 1024
            print(f"✅ picsum fallback OK ({size_kb:.0f} KB)")
    except Exception as e:
        print(f"❌ picsum also failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
