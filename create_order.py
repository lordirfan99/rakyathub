#!/usr/bin/env python3
"""Create completed order directly on TaskKita."""
import urllib.request, json, re, http.client

# Get key + login
resp = urllib.request.urlopen(urllib.request.Request(
    "https://taskkita.com/assets/index-CdJ2nOzM.js",
    headers={"User-Agent": "Mozilla/5.0"}), timeout=15)
k = re.findall(rb'["\x27](eyJ[a-zA-Z0-9_-]+[.]{1}[a-zA-Z0-9_-]+[.]{1}[a-zA-Z0-9_-]+)["\x27]',
    resp.read())[0].decode()

conn = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn.request("POST", "/auth/v1/token?grant_type=password",
    json.dumps({"email": "taskkita.test.7788@web-library.net", "password": "TestPass789!"}).encode(),
    {"Content-Type": "application/json", "apikey": k, "Authorization": f"Bearer {k}"})
r = conn.getresponse()
d = json.loads(r.read().decode())
conn.close()
t = d["access_token"]
uid = d["user"]["id"]

h = {"Content-Type": "application/json", "apikey": k, "Authorization": f"Bearer {t}",
     "Accept": "application/json", "Prefer": "return=representation"}

# Get smallest package
conn2 = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn2.request("GET", "/rest/v1/packages?select=id,name,price&order=price.asc&limit=1",
    headers={"apikey": k, "Authorization": f"Bearer {t}", "Accept": "application/json"})
pkg = json.loads(conn2.getresponse().read().decode())[0]
conn2.close()
print(f"Package: {pkg['name']} @ RM{pkg['price']}")

# Try direct order with status=completed
conn3 = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
body = json.dumps({"advertiser_id": uid, "package_id": pkg["id"],
    "amount_paid": pkg["price"], "target_url": "https://instagram.com/test",
    "status": "completed"}).encode()
conn3.request("POST", "/rest/v1/orders", body=body, headers=h)
r3 = conn3.getresponse()
print(f"Order (completed): {r3.status} {r3.read().decode()[:200]}")
conn3.close()

# Try with status=paid
conn4 = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
body2 = json.dumps({"advertiser_id": uid, "package_id": pkg["id"],
    "amount_paid": pkg["price"], "target_url": "https://instagram.com/test",
    "status": "paid"}).encode()
conn4.request("POST", "/rest/v1/orders", body=body2, headers=h)
r4 = conn4.getresponse()
print(f"Order (paid): {r4.status} {r4.read().decode()[:200]}")
conn4.close()

# Check balance
conn5 = http.client.HTTPSConnection("xvdibouzxfynsxgrmffb.supabase.co")
conn5.request("GET", f"/rest/v1/profiles?id=eq.{uid}&select=balance", headers=h)
r5 = conn5.getresponse()
prof = json.loads(r5.read().decode())
conn5.close()
print(f"Balance: RM{prof[0]['balance']}")
