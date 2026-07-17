import requests, re, json, quopri, html

# Login to mail.tm and get the verify URL
mt = requests.Session()
mt.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
r = mt.post("https://api.mail.tm/token", 
    json={"address": "lasttry994cmor7an@web-library.net", "password": "TestPass789!"}, timeout=15)
mt.headers["Authorization"] = "Bearer " + r.json()["token"]
data = mt.get("https://api.mail.tm/messages", timeout=10).json()
msgs = data if isinstance(data, list) else data.get("hydra:member", [])
mid = msgs[0]["id"] if msgs else None

if mid:
    raw = mt.get("https://api.mail.tm/messages/" + mid + "/download", timeout=10).text
    decoded = quopri.decodestring(raw.encode()).decode("utf-8", errors="replace")
    vm = re.search(r'href="([^"]*verify-email[^"]*)"', decoded)
    if vm:
        vu = html.unescape(vm.group(1))
        print("Verify URL: " + vu[:80] + "...")
        
        # Login
        s = requests.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0"})
        rl = s.get("https://dash.reply.la/login", timeout=15)
        csrf = re.search(r'csrf-token" content="([^"]+)"', rl.text).group(1)
        s.post("https://dash.reply.la/login",
            data={"_token": csrf, "email": "lasttry994cmor7an@web-library.net", "password": "TestPass789!", "remember": "1"},
            allow_redirects=True, timeout=15)
        
        # GET verify URL - capture full response (no redirect)
        rv = s.get(vu, timeout=15, allow_redirects=False)
        print("\nVerify response: " + str(rv.status_code))
        print("Location: " + rv.headers.get("Location", "-"))
        print("Content-Type: " + rv.headers.get("Content-Type", "-"))
        print("Set-Cookie: " + rv.headers.get("Set-Cookie", "-")[:100])
        
        # Check body
        if rv.status_code == 200 and rv.text:
            print("\nBody (first 3000 chars):")
            print(rv.text[:3000])
            
            # Search for key elements
            if "form" in rv.text.lower():
                forms = re.findall(r'<form[^>]*>', rv.text, re.I)
                print("\nForms: " + str(len(forms)))
                for f in forms[:5]:
                    print("  " + f[:200])
            
            # Search for verify-related text
            for kw in ["verify", "success", "error", "click", "confirm", "button"]:
                matches = re.findall(r'[^.]*' + kw + '[^.]*\.', rv.text, re.I)
                if matches:
                    print("\n'" + kw + "' mentions: " + str(len(matches)))
                    for m in matches[:3]:
                        print("  -> " + m.strip()[:150])
        
        # Also try with Inertia headers
        print("\n--- With Inertia headers ---")
        rv2 = s.get(vu, headers={"X-Inertia": "true", "Accept": "application/json"}, 
                     timeout=15, allow_redirects=False)
        print("Status: " + str(rv2.status_code))
        print("Body: " + rv2.text[:500])
        
        # Check if there are flash messages
        rv3 = s.get(vu, timeout=15, allow_redirects=True)
        flash_search = re.search(r'flash[^}]+(?:success|error)[^}]+}', rv3.text)
        if flash_search:
            print("\nFlash: " + flash_search.group()[:200])
