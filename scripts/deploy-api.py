#!/usr/bin/env python3
"""
Copy fetched government data to public/api/ for public access.
This makes data files available at https://rakyathub.my/api/{name}.json
"""
import json, os, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "src", "data")
PUBLIC_API = os.path.join(BASE, "public", "api")

# Create public/api/ directory
os.makedirs(PUBLIC_API, exist_ok=True)

# Copy all *.json from src/data/ to public/api/
copied = 0
for f in os.listdir(DATA_DIR):
    if f.endswith(".json") and not f.startswith("."):
        src = os.path.join(DATA_DIR, f)
        dst = os.path.join(PUBLIC_API, f)
        shutil.copy2(src, dst)
        size = os.path.getsize(dst)
        copied += 1

# Create an index.json listing all available datasets
index = []
for f in sorted(os.listdir(PUBLIC_API)):
    if f == "index.json" or not f.endswith(".json"):
        continue
    path = os.path.join(PUBLIC_API, f)
    size = os.path.getsize(path)
    try:
        with open(path) as fp:
            data = json.load(fp)
        count = len(data) if isinstance(data, list) else "obj"
    except:
        count = "?"
    index.append({
        "name": f.replace(".json", ""),
        "url": f"/api/{f}",
        "size_bytes": size,
        "items": count,
    })

with open(os.path.join(PUBLIC_API, "index.json"), "w") as f:
    json.dump({
        "name": "RakyatHub Open Data API",
        "description": "Malaysian government open data fetched from data.gov.my, updated daily on build.",
        "source": "https://api.data.gov.my",
        "endpoints": len(index),
        "last_updated": __import__("datetime").datetime.now().isoformat(),
        "datasets": index
    }, f, indent=2)

print(f"✅ Copied {copied} datasets to public/api/")
print(f"   Available at https://rakyathub.my/api/index.json")
