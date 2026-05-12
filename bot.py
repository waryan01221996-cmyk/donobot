import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def print_log(text):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}", flush=True)

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def run_bot():
    # Daftar link manual kamu
    manual_links = [
        "https://www.febspot.com/video/3218504", "https://www.febspot.com/video/3218505",
        "https://www.febspot.com/video/3218527", "https://www.febspot.com/video/3218528",
        "https://www.febspot.com/video/3216677", "https://www.febspot.com/video/3217419",
        "https://www.febspot.com/video/3217420", "https://www.febspot.com/video/3217423",
        "https://www.febspot.com/video/3217424", "https://www.febspot.com/video/3189338",
        "https://www.febspot.com/video/3137164", "https://www.febspot.com/video/3141573", 
        "https://www.febspot.com/video/3141576", "https://www.febspot.com/video/3141587", 
        "https://www.febspot.com/video/3141592"
        # ... (tambahkan link lainnya jika perlu)
    ]

    driver = setup_browser()

    try:
        # 1. CEK IP GITHUB
        driver.get("https://api.ipify.org")
        print_log(f"🌐 GITHUB ACTION IP: {driver.find_element(By.TAG_NAME, 'body').text}")
        print_log("-" * 45)

        # 2. SCRAPE PROFIL (Otomatis ambil link baru)
        profile_url = "https://www.febspot.com/heru01221996"
        print_log(f"🔍 Mencari video baru di profil: {profile_url}")
        driver.get(profile_url)
        time.sleep(10)

        # Scroll untuk ambil link
        for _ in range(5): 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        scraped_links = [el.get_attribute("href") for el in driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")]
        all_links = list(set(manual_links + scraped_links))
        
        # PILIH 100 VIDEO SECARA ACAK
        target_count = 100
        video_links = random.sample(all_links, min(len(all_links), target_count))
        
        print_log(f"📚 Memulai pemutaran {len(video_links)} video secara acak.")
        print_log("-" * 45)

        # 3. PROSES NONTON
        for index, link in enumerate(video_links):
            print_log(f"[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            time.sleep(7)
            
            try:
                wait = WebDriverWait(driver, 20)
                video = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Klik tombol play
                ActionChains(driver).move_to_element(video).click().perform()
                
                duration = driver.execute_script("return arguments[0].duration;", video)
                if duration:
                    print_log(f"▶️ Menonton {int(duration)} detik...")
                    time.sleep(duration + 2) # Tunggu sampai video habis
                    print_log("✅ Selesai.")
                else:
                    time.sleep(30) # Durasi gagal baca, tunggu standar
            except:
                print_log("⚠️ Gagal memutar video ini.")
            
            # Jeda antar video agar natural
            time.sleep(random.randint(3, 6))

    except Exception as e:
        print_log(f"❌ ERROR: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print_log("🚀 BOT DIMULAI")
    run_bot()
    print_log("🏁 BOT SELESAI")
