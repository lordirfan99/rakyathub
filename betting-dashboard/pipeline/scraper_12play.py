"""
Extract 12Play odds using Selenium with proper login.
12Play uses Cloudflare - needs real browser rendering.
"""

import json, os, time, re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.12play21.com/en-MY/en"
USERNAME = "lordirfan"
PASSWORD = "lordirfan"

def create_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def login(driver):
    print("[12Play] Loading page...")
    driver.get(URL)
    time.sleep(5)
    
    # Click Login button
    try:
        login_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]")
        login_btn.click()
        time.sleep(2)
    except:
        print("[12Play] Login button not found")
    
    # Fill username
    try:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        if inputs:
            inputs[0].clear()
            inputs[0].send_keys(USERNAME)
            print(f"[12Play] Username entered: {USERNAME}")
        if len(inputs) > 1:
            inputs[1].clear()
            inputs[1].send_keys(PASSWORD)
            print("[12Play] Password entered")
    except Exception as e:
        print(f"[12Play] Input error: {e}")
    
    time.sleep(1)
    
    # Click submit
    try:
        submit = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        submit.click()
        print("[12Play] Login submitted")
        time.sleep(5)
    except Exception as e:
        print(f"[12Play] Submit error: {e}")
    
    print(f"[12Play] URL after login: {driver.current_url}")
    
    # Check if logged in
    if 'login' not in driver.current_url.lower():
        print("[12Play] LOGIN SUCCESSFUL!")
        return True
    
    # Try navigate to sports
    driver.get(URL)
    time.sleep(3)
    try:
        sports = driver.find_element(By.XPATH, "//a[contains(text(), 'Sports')]")
        sports.click()
        time.sleep(4)
        print(f"[12Play] Sports page URL: {driver.current_url}")
    except:
        print("[12Play] Sports link not found")
    
    return 'login' not in driver.current_url.lower()


def extract_odds(driver):
    """Extract match odds from 12Play sports page."""
    print("[12Play] Extracting odds...")
    
    # Save page source for debugging
    with open("debug_12play.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    # Look for match containers
    matches = driver.find_elements(By.XPATH, "//*[contains(@class, 'match') or contains(@class, 'event') or contains(@class, 'game')]")
    print(f"[12Play] Found {len(matches)} potential match elements")
    
    # Look for World Cup / WC text
    body = driver.find_element(By.TAG_NAME, "body")
    print(f"[12Play] Body text sample: {body.text[:1000]}")
    
    return []


def main():
    driver = None
    try:
        driver = create_driver()
        logged_in = login(driver)
        
        if logged_in:
            matches = extract_odds(driver)
        
        input("Press Enter to close...")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
