from playwright.sync_api import sync_playwright
import img2pdf
import time
import os
import json

URL = os.getenv("BOOK_URL")
TOTAL = int(os.getenv("TOTAL_PAGES", "10"))

os.makedirs("pages", exist_ok=True)

images = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        viewport={"width": 1400, "height": 2000}
    )

    # Cookie yuklash
    with open("cookies.json", "r", encoding="utf-8") as f:
        cookies = json.load(f)

    # Cookie fix
    for cookie in cookies:

        if "sameSite" in cookie:

            if cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                cookie["sameSite"] = "None"

    context.add_cookies(cookies)

    page = context.new_page()

    page.goto(URL, timeout=120000)

    print("Waiting page load...")
    time.sleep(10)

    for i in range(TOTAL):

        filename = f"pages/page_{i+1}.png"

        page.screenshot(
            path=filename,
            full_page=False
        )

        print(f"saved: {filename}")

        images.append(filename)

        page.evaluate("""
            window.scrollBy({
                top: 1600,
                behavior: 'smooth'
            })
        """)

        time.sleep(2)

    browser.close()

with open("book.pdf", "wb") as f:
    f.write(img2pdf.convert(images))

print("PDF tayyor")
