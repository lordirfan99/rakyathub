import json, urllib.request, re

# Open DOSM data catalogue page to find salary dataset IDs
url = "https://api.data.gov.my/data-catalogue/"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "RakyatHub/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode()
    # Try JSON
    try:
        data = json.loads(body)
        if isinstance(data, list):
            print(f"Total datasets: {len(data)}")
            for d in data:
                if isinstance(d, dict) and any(kw in str(d).lower() for kw in ["salary","wage","gaji","upah"]):
                    print(json.dumps(d, indent=2)[:500])
            for d in data[:20]:
                if isinstance(d, dict):
                    print(f"  {d.get('id','?')}: {str(d)[:100]}")
        else:
            print(f"Not a list: {type(data)}")
            print(str(data)[:1000])
    except json.JSONDecodeError:
        print(f"Not JSON, content preview: {body[:500]}")
except Exception as e:
    print(f"Error: {e}")
