from seleniumbase import Driver
import os
from dotenv import load_dotenv
import csv

load_dotenv()

LOGIN_URL = os.getenv("LOGIN_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PROMPT = os.getenv("PROMPT")

with open('ticket_list.csv', mode='r') as file:
    reader = csv.reader(file)
    ticket_list = [row[0] for row in reader]

driver = Driver(uc=True)
driver.maximize_window()

try:
    driver.uc_open_with_reconnect(LOGIN_URL, 4)
    driver.uc_gui_click_captcha()
    driver.uc_open_with_reconnect(LOGIN_URL, 4)
    driver.uc_gui_click_captcha()

    driver.type('[name="email"]', EMAIL)
    driver.type('[name="password"]', PASSWORD)
    driver.click('button[type="submit"]')
    driver.sleep(3)

    driver.type('textarea[dir="auto"]', f"{ticket_list[0]} {PROMPT}\n")
    driver.sleep(20)
    elements = driver.find_elements('div[dir="auto"]')
    result_text = elements[1].text

    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(result_text)

    print("Script completed successfully.")

finally:
    driver.quit()
