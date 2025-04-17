import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = "chiragsawant_F9A7B4"
ACCESS_KEY = "dirweyPuBXZBbk2G8oQm"
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

capabilities = {
    "browser": "Chrome",
    "browser_version": "latest",
    "os": "Windows",
    "os_version": "10",
    "name": "Dhan Chat Automation"
}

messages = [
    "I want to close my Dhan account", "Please close my Dhan account", "How do I close my Dhan account?",
    "Can you help me close my Dhan account?", "I need to deactivate my Dhan account",
    # ... (add all your messages)
]

def run_single_test():
    selected_message = random.choice(messages)
    print(f"\n[+] Selected message: {selected_message}")

    driver = webdriver.Remote(command_executor=URL, options=webdriver.ChromeOptions())
    session_id = None

    try:
        print("[+] Opening Dhan account closure page...")
        driver.get("https://exit.dhan.co/index/accountClosure/connect")

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Start Chat')]"))
        ).click()

        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
        )

        chat_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app-conversation-editor > p"))
        )

        chat_input.click()
        chat_input.send_keys(selected_message)
        chat_input.send_keys(Keys.RETURN)

        print("[+] Message sent, waiting for 10 seconds...")
        time.sleep(10)

        session_id = driver.session_id
        print(f"[+] Session ID: {session_id}")

    except Exception as e:
        print(f"[!] Exception occurred: {e}")

    finally:
        print("[+] Closing browser...")
        driver.quit()

    return session_id

def get_browserstack_video_url(session_id):
    if not session_id:
        print("[!] No session ID to fetch video.")
        return
    print(f"[+] Fetching video for session ID: {session_id}")
    url = f"https://api.browserstack.com/automate/sessions/{session_id}.json"
    response = requests.get(url, auth=(USERNAME, ACCESS_KEY))

    if response.status_code == 200:
        video_url = response.json().get('automation_session', {}).get('video_url')
        if video_url:
            print(f"[+] Video URL: {video_url}")
        else:
            print("[!] Video URL not found.")
    else:
        print(f"[!] Failed to fetch video. HTTP {response.status_code}")

# Run every 10 minutes
if __name__ == "__main__":
    while True:
        print("\n========== Starting Automated Run ==========")
        sid = run_single_test()
        get_browserstack_video_url(sid)
        print("[+] Sleeping for 10 minutes...")
        time.sleep(600)  # Sleep for 600 seconds (10 mins)
