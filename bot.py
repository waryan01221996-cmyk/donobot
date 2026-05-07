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
    # Memaksa teks langsung keluar ke log (Unbuffered)
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
        # 1. PROSES MENGUMPULKAN LINK DARI PROFIL
        profile_url = "https://www.febspot.com/heru01221996"
        print_log(f">>> Membuka profil: {profile_url}")
        driver.get(profile_url)
        time.sleep(5)

        print_log(">>> Memulai pemuatan video (Load more)...")
        
        last_count = 0
        same_count_retry = 0
        max_load_clicks = 20 # Batas maksimal klik load more

        for i in range(max_load_clicks):
            # Ambil jumlah video saat ini
            current_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
            current_count = len(set([el.get_attribute("href") for el in current_elements]))
            
            print_log(f"Terdeteksi: {current_count} video.")

            # Berhenti jika jumlah video tidak bertambah setelah klik sebelumnya
            if current_count == last_count:
                same_count_retry += 1
                if same_count_retry >= 2:
                    print_log("Tidak ada video baru lagi. Selesai memuat halaman.")
                    break
            else:
                same_count_retry = 0
            
            last_count = current_count

            try:
                # Scroll ke bawah agar tombol terdeteksi
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # Cari tombol Load More
                load_more_btn = WebDriverWait(driver, 7).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Load more')] | //div[contains(text(), 'Load more')] | //*[contains(@class, 'load-more')]"))
                )
                
                # Klik via JavaScript (lebih stabil)
                driver.execute_script("arguments[0].click();", load_more_btn)
                print_log(f"Klik ke-{i+1} berhasil. Menunggu konten...")
                time.sleep(5) 
            except:
                print_log("Tombol Load more sudah tidak ada.")
                break

        # Finalisasi daftar link
        elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
        video_links = list(set([el.get_attribute("href") for el in elements if "/video/" in el.get_attribute("href")]))
        
        print_log(f">>> TOTAL AKHIR: Berhasil mengumpulkan {len(video_links)} video.")
        print_log("-" * 40)

        if not video_links:
            print_log("Gagal mendapatkan link video. Skrip dihentikan.")
            return

        # 2. PROSES MENONTON (Logika Utama)
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print_log(f"\n[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            time.sleep(5) 
            
            try:
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Klik play menggunakan ActionChains
                actions = ActionChains(driver)
                actions.move_to_element(video_element).click().perform()
                print_log("Berhasil klik Play.")

                # Ambil durasi video
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
                            
                        # Safety timeout
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
                print_log("Peringatan: Gagal memuat video atau elemen hilang.")
            
            jeda = random.randint(4, 7)
            print_log(f"Istirahat {jeda} detik...")
            time.sleep(jeda)

    except Exception as e:
        print_log(f"KESALAHAN SISTEM: {e}")
    finally:
        print_log("\nProses selesai. Menutup browser.")
        driver.quit()

# Menggunakan double underscore sesuai standar Python
if __name__ == "__main__":
    run_bot()
