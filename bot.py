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
    print(text, flush=True)
    sys.stdout.flush()

def run_bot():
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

    print_log(">>> Menyiapkan Browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        # 1. PROSES MENGAMBIL SEMUA LINK DENGAN KLIK 'LOAD MORE'
        profile_url = "https://www.febspot.com/heru01221996"
        print_log(f">>> Membuka profil: {profile_url}")
        driver.get(profile_url)
        time.sleep(5)

        while True:
            try:
                # Cari tombol 'Load more'
                # Berdasarkan gambar, biasanya berupa button atau element dengan teks 'Load more'
                load_more_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load more')] | //div[contains(text(), 'Load more')]"))
                )
                
                # Scroll ke tombol agar bisa diklik
                driver.execute_script("arguments[0].scrollIntoView();", load_more_btn)
                time.sleep(1)
                
                load_more_btn.click()
                print_log("Klik 'Load more'...")
                time.sleep(3) # Tunggu video baru dimuat
            except:
                # Jika tombol tidak ditemukan lagi atau sudah habis
                print_log("Semua video telah dimuat.")
                break

        # Mengambil semua link video yang muncul
        elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
        video_links = list(set([el.get_attribute("href") for el in elements]))
        
        print_log(f">>> Total ditemukan {len(video_links)} video.")
        print_log("-" * 40)

        # 2. PROSES MENONTON (Logika Tetap Sama)
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print_log(f"\n[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            time.sleep(5) 
            
            try:
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                actions = ActionChains(driver)
                actions.move_to_element(video_element).click().perform()
                print_log("Berhasil klik Play.")

                duration = driver.execute_script("return arguments[0].duration;", video_element)

                if duration and duration > 0:
                    print_log(f"Video dikesan. Durasi: {int(duration)} detik.")
                    start_watch = time.time()
                    
                    while True:
                        current = driver.execute_script("return arguments[0].currentTime;", video_element)
                        ended = driver.execute_script("return arguments[0].ended;", video_element)
                        
                        if ended or current >= (duration - 1):
                            print_log("Konfirmasi: Video selesai ditonton.")
                            break
                            
                        if (time.time() - start_watch) > (duration + 20):
                            print_log("Timeout: Melanjutkan ke video berikutnya.")
                            break
                            
                        if int(current) % 15 == 0 and int(current) > 0:
                            print_log(f"Status: Menonton detik ke-{int(current)}")
                            
                        time.sleep(5)
                else:
                    print_log("Gagal ambil durasi, tunggu 25 detik manual...")
                    time.sleep(25)

            except Exception:
                print_log("Peringatan: Gagal memuat video.")
            
            jeda = random.randint(4, 7)
            print_log(f"Istirahat {jeda} detik...")
            time.sleep(jeda)

    except Exception as e:
        print_log(f"KESALAHAN SISTEM: {e}")
    finally:
        print_log("\nProses selesai. Menutup browser.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
