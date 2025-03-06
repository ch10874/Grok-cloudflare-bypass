from seleniumbase import Driver
import os
from dotenv import load_dotenv
import csv

load_dotenv()

LOGIN_URL = os.getenv("LOGIN_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PROMPT = "short term forecast. Separate into 3 sections of analysis (in that order): News Summary, Forecast Range & Key Factors Impacting the Range. Under each section have no more than 5 bullet points. Only include header and bullets (no extra text)."

with open('ticket_list.csv', mode='r') as file:
    reader = csv.reader(file)
    ticket_list = [row[0] for row in reader]

driver = Driver(uc=True)
driver.maximize_window()
driver.uc_open_with_reconnect(LOGIN_URL, 4)
driver.uc_gui_click_captcha()
driver.uc_open_with_reconnect(LOGIN_URL, 4)
driver.uc_gui_click_captcha()

driver.type('[name="email"]', EMAIL)
driver.type('[name="password"]', PASSWORD)
driver.click('button[type="submit"]')
driver.sleep(5)

driver.type('textarea[dir="auto"]', f"{ticket_list[0]} {PROMPT}\n")
driver.sleep(20)
elements = driver.find_elements('div[dir="auto"]')
result_text = elements[1].text

with open('result.txt', 'w', encoding='utf-8') as file:
    file.write(result_text)

driver.quit()

print("Script completed successfully.")