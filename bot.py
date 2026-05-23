import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

def print_log(text):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}", flush=True)
    sys.stdout.flush()

def run_bot():
    # Daftar 119 link video manual bawaan kamu
    video_links = [
        "https://www.febspot.com/video/3218504", "https://www.febspot.com/video/3218505",
        "https://www.febspot.com/video/3218527", "https://www.febspot.com/video/3218528",
        "https://www.febspot.com/video/3216677", "https://www.febspot.com/video/3217419",
        "https://www.febspot.com/video/3217420", "https://www.febspot.com/video/3217423",
        "https://www.febspot.com/video/3217424", "https://www.febspot.com/video/3189338", 
        "https://www.febspot.com/video/3189741", "https://www.febspot.com/video/3189743",
        "https://www.febspot.com/video/3189744", "https://www.febspot.com/video/3189747", 
        "https://www.febspot.com/video/3189748", "https://www.febspot.com/video/3189750", 
        "https://www.febspot.com/video/3189751", "https://www.febspot.com/video/3189753",
        "https://www.febspot.com/video/3189754", "https://www.febspot.com/video/3189846", 
        "https://www.febspot.com/video/3189848", "https://www.febspot.com/video/3189849", 
        "https://www.febspot.com/video/3189851", "https://www.febspot.com/video/3189857",
        "https://www.febspot.com/video/3189858", "https://www.febspot.com/video/3189860", 
        "https://www.febspot.com/video/3189861", "https://www.febspot.com/video/3189863", 
        "https://www.febspot.com/video/3189864", "https://www.febspot.com/video/3183766",
        "https://www.febspot.com/video/3185499", "https://www.febspot.com/video/3185507", 
        "https://www.febspot.com/video/3185508", "https://www.febspot.com/video/3185510", 
        "https://www.febspot.com/video/3185511", "https://www.febspot.com/video/3185512",
        "https://www.febspot.com/video/3189317", "https://www.febspot.com/video/3189318", 
        "https://www.febspot.com/video/3189319", "https://www.febspot.com/video/3189320", 
        "https://www.febspot.com/video/3189321", "https://www.febspot.com/video/3189328",
        "https://www.febspot.com/video/3189329", "https://www.febspot.com/video/3189330", 
        "https://www.febspot.com/video/3189331", "https://www.febspot.com/video/3189333", 
        "https://www.febspot.com/video/3189334", "https://www.febspot.com/video/3189335",
        "https://www.febspot.com/video/3189336", "https://www.febspot.com/video/3181867", 
        "https://www.febspot.com/video/3181868", "https://www.febspot.com/video/3182071", 
        "https://www.febspot.com/video/3182072", "https://www.febspot.com/video/3182073",
        "https://www.febspot.com/video/3182075", "https://www.febspot.com/video/3182076", 
        "https://www.febspot.com/video/3182077", "https://www.febspot.com/video/3182079", 
        "https://www.febspot.com/video/3182080", "https://www.febspot.com/video/3182081",
        "https://www.febspot.com/video/3182082", "https://www.febspot.com/video/3182083", 
        "https://www.febspot.com/video/3182086", "https://www.febspot.com/video/3182087", 
        "https://www.febspot.com/video/3182089", "https://www.febspot.com/video/3182091",
        "https://www.febspot.com/video/3182092", "https://www.febspot.com/video/3182093", 
        "https://www.febspot.com/video/3183764", "https://www.febspot.com/video/3171758", 
        "https://www.febspot.com/video/3171759", "https://www.febspot.com/video/3171760",
        "https://www.febspot.com/video/3171761", "https://www.febspot.com/video/3171762", 
        "https://www.febspot.com/video/3181098", "https://www.febspot.com/video/3181099", 
        "https://www.febspot.com/video/3181100", "https://www.febspot.com/video/3181101",
        "https://www.febspot.com/video/3181102", "https://www.febspot.com/video/3181103", 
        "https://www.febspot.com/video/3181104", "https://www.febspot.com/video/3181106", 
        "https://www.febspot.com/video/3181108", "https://www.febspot.com/video/3181109",
        "https://www.febspot.com/video/3181860", "https://www.febspot.com/video/3181861", 
        "https://www.febspot.com/video/3181863", "https://www.febspot.com/video/3181865", 
        "https://www.febspot.com/video/3181866", "https://www.febspot.com/video/3141597",
        "https://www.febspot.com/video/3141598", "https://www.febspot.com/video/3141600", 
        "https://www.febspot.com/video/3141605", "https://www.febspot.com/video/3141763", 
        "https://www.febspot.com/video/3141777", "https://www.febspot.com/video/3141780",
        "https://www.febspot.com/video/3144339", "https://www.febspot.com/video/3144340", 
        "https://www.febspot.com/video/3144342", "https://www.febspot.com/video/3144343", 
        "https://www.febspot.com/video/3144347", "https://www.febspot.com/video/3144349",
        "https://www.febspot.com/video/3171613", "https://www.febspot.com/video/3171614", 
        "https://www.febspot.com/video/3171617", "https://www.febspot.com/video/3171618", 
        "https://www.febspot.com/video/3171620", "https://www.febspot.com/video/3171623",
        "https://www.febspot.com/video/3171624", "https://www.febspot.com/video/3137143", 
        "https://www.febspot.com/video/3137150", "https://www.febspot.com/video/3137152", 
        "https://www.febspot.com/video/3137158", "https://www.febspot.com/video/3137159",
        "https://www.febspot.com/video/3137164", "https://www.febspot.com/video/3141573", 
        "https://www.febspot.com/video/3141576", "https://www.febspot.com/video/3141587", 
        "https://www.febspot.com/video/3141592"
    ]

    print_log(">>> Menyiapkan Selenium WebDriver (Koneksi Reguler Tanpa Tor)...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    
    # 1. CEK KONEKSI IP UTAMA
    try:
        driver.get("https://api.ipify.org")
        ip_addr = driver.find_element(By.TAG_NAME, "body").text
        print_log(f"🟢 IP BROWSER AKTIF: {ip_addr.strip()}")
        print_log("-" * 45)
    except Exception:
        print_log("⚠️ Gagal cek IP, lanjut mengeksekusi target...")

    # 2. LOAD MORE DARI PROFIL (Diadopsi dari Skrip Pintarmu)
    profile_url = "https://www.febspot.com/heru01221996"
    print_log(f"🔍 Mencari seluruh video di halaman profil: {profile_url}")
    driver.get(profile_url)
    time.sleep(8)

    last_count = 0
    
    # Maksimal 25 kali percobaan scroll untuk pengamanan ekstra
    for i in range(25): 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        
        # Hitung jumlah link video unik yang saat ini ter-load di layar
        elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
        current_count = len(set([el.get_attribute("href") for el in elements if el.get_attribute("href")]))
        
        print_log(f"🔄 Scan ke-{i+1}: Ditemukan {current_count} link sementara di halaman...")
        
        # JIKA JUMLAH VIDEO SUDAH TIDAK BERTAMBAH, BREAK (Solusi anti-macet)
        if current_count == last_count: 
            print_log("✨ Jumlah video tidak bertambah lagi. Semua video profil berhasil dimuat penuh!")
            break
            
        last_count = current_count

        # Mencoba klik tombol 'Load more' jika muncul di layar
        try:
            load_more_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Load more')]")
            driver.execute_script("arguments[0].click();", load_more_btn)
            time.sleep(4)
        except:
            pass

    # Mengambil semua link video hasil scraping profil
    scraped_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
    scraped_links = [el.get_attribute("href") for el in scraped_elements if el.get_attribute("href")]
    
    # Gabungkan secara unik (menghapus duplikat)
    video_links = list(set(video_links + scraped_links))
    print_log(f"📚 TOTAL KESELURUHAN SELESAI DIKUMPULKAN: {len(video_links)} video.")
    print_log("-" * 45)

    # 3. PERULANGAN KLIK IKLAN INSTAN (Kembali ke Perilaku Skrip Awal)
    random.shuffle(video_links)
    
    for index, link in enumerate(video_links):
        print_log(f"\n[{index+1}/{len(video_links)}] Membuka Halaman: {link}")
        driver.get(link)
        
        try:
            # Tunggu tombol "Accept & Watch Video" selama maksimal 10 detik
            wait = WebDriverWait(driver, 10)
            accept_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Accept & Watch Video')] | //div[contains(@class, 'watched')]//button")
            ))
            
            main_window = driver.current_window_handle
            print_log("🔘 Tombol 'Accept & Watch Video' ditemukan! Melakukan klik...")
            accept_btn.click()
            time.sleep(3) # Beri waktu jendela tab baru terbuka

            # Cari jika ada jendela/tab baru yang terbuka
            all_windows = driver.window_handles
            if len(all_windows) > 1:
                # Pindah fokus ke tab iklan baru
                for window in all_windows:
                    if window != main_window:
                        driver.switch_to.window(window)
                        break
                
                # Tangkap URL dari website iklan tersebut
                ad_url = driver.current_url
                domain = urlparse(ad_url).netloc
                print_log(f"🌐 [WEB IKLAN TERBUKA]: {domain if domain else ad_url}")
                print_log("⏳ Menunggu di tab iklan selama 10 detik...")
                
                # Diamkan tab iklan selama 10 detik pas
                time.sleep(10)
                
                # Tutup tab iklan dan kembali ke tab utama
                driver.close()
                driver.switch_to.window(main_window)
                print_log("✅ Tab iklan ditutup. Langsung melompat ke video berikutnya!")
            else:
                print_log("⚠️ Klik berhasil dilakukan, namun tidak ada tab iklan eksternal terbuka.")
                
        except Exception as e:
            print_log("❌ Tombol iklan tidak terdeteksi / Gagal diklik pada halaman ini. Skip...")

        time.sleep(random.randint(1, 3))

    driver.quit()

if __name__ == "__main__":
    run_bot()
