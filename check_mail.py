import requests, re, json, quopri, html

# Check mail.tm inbox for all emails
mt = requests.Session()
mt.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
r = mt.post("https://api.mail.tm/token", 
    json={"address": "final2nxaqg4rgnq@web-library.net", "password": "TestPass789!"}, timeout=15)
mt.headers["Authorization"] = "Bearer " + r.json()["token"]

data = mt.get("https://api.mail.tm/messages", timeout=10).json()
msgs = data if isinstance(data, list) else data.get("hydra:member", [])
print("Total messages: " + str(len(msgs)))

for i, mo in enumerate(msgs):
    mid = mo["id"] if isinstance(mo, dict) else mo
    m = mt.get("https://api.mail.tm/messages/" + mid, timeout=10).json()
    subj = m.get("subject", "")
    frm = m.get("from", {}).get("address", "")
    print("[" + str(i) + "] " + subj + " from " + frm)
    
    raw = mt.get("https://api.mail.tm/messages/" + mid + "/download", timeout=10).text
    decoded = quopri.decodestring(raw.encode()).decode("utf-8", errors="replace")
    
    # Find ALL reply.la links
    links = re.findall(r'https?://dash\.reply\.la[^\s<>"\\\']+', decoded)
    for link in links:
        clean = html.unescape(link)
        if "verify" not in clean.lower() and "logo" not in clean.lower() and "storage" not in clean.lower():
            print("  LINK: " + clean[:120])
