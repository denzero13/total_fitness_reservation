from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

URL = "https://totalfitness-ua.perfectgym.com/ClientPortal2/"
EMAIL = "denmen133@gmail.com"     # 🔁 Введи свій емейл
PASSWORD = "qwertyden13"      # 🔁 Введи свій пароль


def main(email: str, password: str):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    driver.get(URL)

    wait.until(EC.presence_of_element_located((By.NAME, "Login"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "confirm"))).click()

    time.sleep(5)
    driver.get(f"{URL}#/Classes/11/List?date=2025-05-05")

    time.sleep(5)
    items = driver.find_elements(By.CSS_SELECTOR, 'cp\\:classes-class-item')

    found = False
    for item in items:
        text = item.text.lower()
        if "pilates" in text and "олена мікуліна" in text:
            try:
                book_now_button = WebDriverWait(item, 3).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        './/div[contains(@class, "cp-btn-classes-action") and .//span[text()="Взяти участь"]]'
                    ))
                )
                book_now_button.click()
                print("✅ Успішно заброньовано Pilates з Оленою Мікуліною")
                found = True
                time.sleep(5)
                break
            except Exception as e:
                print("🚫 Кнопка 'Взяти участь' неактивна або відсутня:", e)


    if not found:
        print("❌ Не знайдено відповідного тренування")

    driver.quit()

if __name__ == "__main__":
    main(os.environ.get('DENYS_EMAIL'), os.environ.get('DENYS_PASS'))