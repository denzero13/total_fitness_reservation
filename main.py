from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os


URL = "https://totalfitness-ua.perfectgym.com/ClientPortal2/"


def main(email: str, password: str, training_with_coach: str):
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.get(URL)

    wait.until(EC.presence_of_element_located((By.NAME, "Login"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "confirm"))).click()

    time.sleep(5)
    today = datetime.today().strftime('%Y-%m-%d')
    driver.get(f"{URL}#/Classes/11/List?date={today}")

    time.sleep(5)
    items = driver.find_elements(By.CSS_SELECTOR, 'cp\\:classes-class-item')

    training, coach = training_with_coach.split(",")

    found = False
    for item in items:
        text = item.text.lower()

        if training in text and coach in text:
            try:
                book_now_button = WebDriverWait(item, 3).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        './/div[contains(@class, "cp-btn-classes-action") and .//span[text()="Book now"]]'
                    ))
                )
                book_now_button.click()
                print(f"✅ Успішно заброньовано {training} з {coach}")
                found = True
                time.sleep(5)
                break
            except Exception as e:
                print(f"🚫 Кнопка 'Взяти участь' неактивна або відсутня:", e)
                print(text)


    if not found:
        print("❌ Не знайдено відповідного тренування")

    driver.quit()

if __name__ == "__main__":
    main(os.environ.get('EMAIL'), os.environ.get('PASSWORD'), os.environ.get("TRAINING_WITH_COACH", ""))