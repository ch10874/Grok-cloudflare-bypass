from seleniumbase import Driver
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
LOGIN_URL = os.getenv("LOGIN_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PROMPT = os.getenv("PROMPT")
TICKET_FILE = 'ticket_list.csv'
RESULT_FILE = 'result.txt'

def load_tickets(file_path):
    """Load ticket list from a CSV file."""
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

def login(driver):
    """Perform login action."""
    driver.uc_open_with_reconnect(LOGIN_URL, 4)
    driver.uc_gui_click_captcha()
    driver.uc_open_with_reconnect(LOGIN_URL, 4)
    driver.uc_gui_click_captcha()
    driver.type('[name="email"]', EMAIL)
    driver.type('[name="password"]', PASSWORD)
    driver.click('button[type="submit"]')
    driver.sleep(3)

def process_ticket(driver, ticket):
    """Process a single ticket."""
    driver.type('textarea[dir="auto"]', f"{ticket} {PROMPT}\n")
    driver.sleep(20)
    elements = driver.find_elements('div[dir="auto"]')
    return elements[1].text

def save_result(result, file_path):
    """Save the result to a text file."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(result + '\n')

def main():
    """Main function to execute the script."""
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)
    ticket_list = load_tickets(TICKET_FILE)
    driver = Driver(uc=True)
    driver.maximize_window()

    try:
        login(driver)
        for ticket in ticket_list:
            result_text = process_ticket(driver, ticket)
            save_result(result_text, RESULT_FILE)
        print("Script completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
