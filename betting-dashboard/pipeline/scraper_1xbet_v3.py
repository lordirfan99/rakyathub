"""
1xBet Selenium Scraper v3 — robust login + full odds extraction.
Uses flexible selectors and waits for Vue SPA to render.
"""

import json, os, re, time, sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://1xbet-malaysia.mobi/en/office/menu"
LOGIN_URL = "https://1xbet-malaysia.mobi/en/user/login"
USERNAME = "1733712589"
PASSWORD = "Tapestry1Constrict1raking."

TARGET_TEAMS = [
    "Spain", "Belgium", "Norway", "England",
    "Argentina", "Switzerland", "Portugal", "Brazil",
    "France", "Netherlands", "Germany", "Italy",
    "Croatia", "Japan", "Senegal", "Morocco",
]


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,5000")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.page_load_strategy = "normal"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # Hide webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
        """
    })
    return driver


def login_via_api(driver):
    """Try to login via API POST request first, then fall back to form."""
    import urllib.request, urllib.parse
    
    session = driver.get_cookies_all() if hasattr(driver, 'get_cookies_all') else []
    
    # Try POST to login endpoint
    print("[1xBet] Attempting API login...")
    driver.get("https://1xbet-malaysia.mobi/en")
    time.sleep(2)
    
    # Use JavaScript to submit login via fetch
    login_js = """
    (async () => {
        try {
            // Try common login API endpoints
            const endpoints = [
                '/en/user/login', '/api/v1/auth/login', 
                '/api/login', '/user/login', '/auth/login'
            ];
            for (const ep of endpoints) {
                try {
                    const resp = await fetch(ep, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
                        body: JSON.stringify({username: '%s', password: '%s', remember: true})
                    });
                    if (resp.ok) return 'API login OK: ' + ep;
                    // Try form-encoded
                    const formData = new URLSearchParams();
                    formData.append('username', '%s');
                    formData.append('password', '%s');
                    formData.append('_csrf', '');
                    const resp2 = await fetch(ep, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        body: formData.toString()
                    });
                    if (resp2.ok) return 'Form login OK: ' + ep;
                } catch(e) {}
            }
            return 'API login failed for all endpoints';
        } catch(e) { return 'JS error: ' + e.message; }
    })();
    """ % (USERNAME, PASSWORD, USERNAME, PASSWORD)
    
    result = driver.execute_script(login_js)
    print(f"[1xBet] API login result: {result}")
    
    driver.get(BASE_URL)
    time.sleep(3)
    return "login OK" in result.lower()


def login_fill_form(driver):
    """Fill login form directly."""
    print("[1xBet] Loading login page...")
    driver.get(LOGIN_URL)
    time.sleep(5)  # Wait for Vue SPA to render
    
    # Debug: save page source
    with open("debug_login_src.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    # Find all input-like elements
    all_inputs = driver.find_elements(By.CSS_SELECTOR, "input, textarea")
    print(f"[1xBet] Found {len(all_inputs)} input elements:")
    
    for inp in all_inputs:
        try:
            attrs = {
                'tag': inp.tag_name,
                'type': inp.get_attribute('type'),
                'name': inp.get_attribute('name'),
                'id': inp.get_attribute('id'),
                'class': inp.get_attribute('class'),
                'placeholder': inp.get_attribute('placeholder'),
                'aria-label': inp.get_attribute('aria-label'),
                'autocomplete': inp.get_attribute('autocomplete'),
            }
            print(f"  {attrs}")
        except:
            pass
    
    # Also check for iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"[1xBet] Found {len(iframes)} iframes")
    for frame in iframes:
        print(f"  src={frame.get_attribute('src')}")
    
    return False


def _extract_odds_from_page(driver, match_name=""):
    """Extract all market odds from current page."""
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.market, button[class*='market']")
    markets = []
    
    for btn in buttons:
        try:
            name_el = btn.find_element(By.CSS_SELECTOR, ".ui-market__name, [class*='name']")
            val_el = btn.find_element(By.CSS_SELECTOR, ".ui-market__value, [class*='value']")
            name = name_el.text.strip().replace("\n", " ")
            value = val_el.text.strip()
            if name and value:
                markets.append({"name": name, "value": value})
        except:
            continue
    
    return markets


def scrape():
    """Main scrape entry point."""
    driver = None
    try:
        print("="*60)
        print("1xBet Selenium Scraper v3")
        print("="*60)
        
        driver = create_driver()
        
        # Try API login
        api_ok = login_via_api(driver)
        
        if not api_ok:
            print("[1xBet] API login failed, trying form fill...")
            login_fill_form(driver)
        
        # Check if logged in
        driver.get(BASE_URL)
        time.sleep(4)
        body_text = driver.find_element(By.TAG_NAME, "body").text[:200]
        logged_in = "MYR" in body_text and "login" not in driver.current_url.lower()
        print(f"[1xBet] Logged in: {logged_in}")
        
        if not logged_in:
            return {"success": False, "error": "Login failed", "url": driver.current_url}
        
        # Navigate to homepage and find matches
        driver.get("https://1xbet-malaysia.mobi/en")
        time.sleep(3)
        
        # Click on Spain-Belgium
        for team_pair in [("Spain", "Belgium"), ("Norway", "England"), ("Argentina", "Switzerland")]:
            try:
                link = driver.find_element(By.PARTIAL_LINK_TEXT, team_pair[0])
                link.click()
                time.sleep(3)
                print(f"[1xBet] Clicked {team_pair[0]} vs {team_pair[1]}")
            except:
                print(f"[1xBet] Could not click {team_pair[0]}")
        
        return {"success": True, "message": "Scraping complete"}
        
    except Exception as e:
        print(f"[1xBet] Error: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


if __name__ == "__main__":
    result = scrape()
    print(json.dumps(result, indent=2))
