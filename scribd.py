import os
import json
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_scraper(url, max_pages, output_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://www.scribd.com")
        
        # Cookie-larni yuklash
        if os.path.exists('cookies.json'):
            with open('cookies.json', 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print("Cookie-lar muvaffaqiyatli yuklandi.")
        
        driver.get(url)
        time.sleep(5)
        
        images = []
        
        for i in range(max_pages):
            # Sahifani topish (Scribd strukturasi bo'yicha)
            page_id = f"page_{i+1}"
            try:
                page_element = driver.find_element(By.ID, page_id)
                driver.execute_script("arguments[0].scrollIntoView();", page_element)
                time.sleep(2) # Yuklanishini kutish
                
                filename = f"temp_{i}.png"
                page_element.screenshot(filename)
                
                img = Image.open(filename).convert('RGB')
                images.append(img)
                os.remove(filename)
                print(f"Sahifa {i+1} tayyor.")
            except Exception as e:
                print(f"Sahifa {i+1} ni yuklab bo'lmadi: {e}")
                break
                
        if images:
            images[0].save(output_name, save_all=True, append_images=images[1:])
            print(f"PDF tayyor: {output_name}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = os.environ.get('SCRIBD_URL')
    pages = int(os.environ.get('PAGE_COUNT', 5))
    run_scraper(target_url, pages, "result.pdf")
