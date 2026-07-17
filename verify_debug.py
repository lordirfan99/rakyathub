import requests, re, json, quopri, html

# Get verify URL from mailbox
mt = requests.Session()
mt.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
r = mt.post("https://api.mail.tm/token", 
    json={"address": "lasttry994cmor7an@web-library.net", "password": "TestPass789!"}, timeout=15)
mt.headers["Authorization"] = "Bearer " + r.json()["token"]
data = mt.get("https://api.mail.tm/messages", timeout=10).json()
msgs = data if isinstance(data, list) else data.get("hydra:member", [])
mid = msgs[0]["id"] if msgs else None

if not mid:
    print("No messages")
    exit(1)

raw = mt.get("https://api.mail.tm/messages/" + mid + "/download", timeout=10).text
decoded = quopri.decodestring(raw.encode()).decode("utf-8", errors="replace")
vm = re.search(r'href="([^"]*verify-email[^"]*)"', decoded)
if not vm:
    print("No verify URL in email")
    exit(1)
vu = html.unescape(vm.group(1))

# Login
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
rl = s.get("https://dash.reply.la/login", timeout=15)
csrf = re.search(r'csrf-token" content="([^"]+)"', rl.text).group(1)
s.post("https://dash.reply.la/login",
    data={"_token": csrf, "email": "lasttry994cmor7an@web-library.net", "password": "TestPass789!", "remember": "1"},
    allow_redirects=True, timeout=15)

# Click verify - DON'T follow redirect
rv = s.get(vu, timeout=15, allow_redirects=False)
print("Verify: " + str(rv.status_code) + " -> " + rv.headers.get("Location", "-"))

if rv.status_code == 302:
    dest = rv.headers["Location"]
    
    # Follow redirect to dashboard
    r_dest = s.get(dest, timeout=15, allow_redirects=True)
    print("After redirect: " + r_dest.url)
    
    # Now check dashboard with fresh request
    r_dash = s.get("https://dash.reply.la/dashboard", headers={"X-Inertia": "true"}, timeout=10)
    print("Dashboard: " + str(r_dash.status_code))
    
    if r_dash.status_code == 200:
        m_dp = re.search(r'data-page=\\({(.+?)}\\)', r_dash.text, re.DOTALL)
        if m_dp:
            pg = json.loads(m_dp.group(1).replace('&quot;', '"'))
            user = pg.get("props",{}).get("auth",{}).get("user",{})
            print("*** VERIFIED! User: " + str(user.get("id")) + " at " + str(user.get("email_verified_at")))
            print("Component: " + pg.get("component", ""))
    else:
        print("Still blocked. Checking auth state in current page...")
        m_dp = re.search(r'data-page=\\({(.+?)}\\)', r_dest.text, re.DOTALL)
        if m_dp:
            pg = json.loads(m_dp.group(1).replace('&quot;', '"'))
            user = pg.get("props",{}).get("auth",{}).get("user",{})
            print("User ID: " + str(user.get("id")))
            print("Verified: " + str(user.get("email_verified_at")))
        else:
            print("No data-page in response")
            print("Response URL: " + r_dest.url)
            print("First 500 chars: " + r_dest.text[:500])
else:
    print("Unexpected status. Body: " + rv.text[:500])
