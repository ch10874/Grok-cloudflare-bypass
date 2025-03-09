from seleniumbase import SB
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

with SB(uc=True) as sb:
    sb.uc_open_with_reconnect(LOGIN_URL, 4)
    sb.uc_gui_click_captcha()
    print("Solved the first captcha.")
    sb.uc_open_with_reconnect(LOGIN_URL, 4)
    sb.uc_gui_click_captcha()
    print("Solved the second captcha.")

    sb.type('[name="email"]', EMAIL)
    sb.type('[name="password"]', PASSWORD)
    sb.click('button[type="submit"]')
    sb.sleep(5)

    sb.type('textarea[dir="auto"]', f"{ticket_list[0]} {PROMPT}\n")
    print("Waiting 20s...")
    sb.sleep(20)
    elements = sb.find_elements('div[dir="auto"]')
    result_text = elements[1].text

    print("Saving result...")
    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(result_text)

    print("Script completed successfully.")
