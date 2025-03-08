from seleniumbase import Driver
from selenium.webdriver.common.by import By
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

def process_ticket(driver, ticket, index):
    """Process a single ticket."""
    driver.type('textarea[dir="auto"]', f"{ticket} {PROMPT}\n")
    driver.sleep(5)

    while True:
        # Check for rate limit message using XPath
        rate_limit_elements = driver.find_elements(By.XPATH, "//p[contains(text(), 'rate limits')]")
        if rate_limit_elements:
            print("Rate Limited")
            return None  # Exit the function if rate limited

        lis = driver.find_elements(By.TAG_NAME, 'li')
        if len(lis) == (index + 1) * 15:
            break
        driver.sleep(1)

    elements = driver.find_elements('div[dir="auto"]')
    h3s = elements[2 * index + 1].find_elements(By.TAG_NAME, 'h3')
    lines = elements[2 * index + 1].find_elements(By.TAG_NAME, 'li')
    
    result = f"{ticket}\n\n"
    for i in range(3):
        result += h3s[i].text + '\n'
        for j in range(5):
            result += lines[j + 5 * i].text + '\n'
    
    return result

def save_result(result, file_path):
    """Save the result to a text file."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(result + '\n')

def main():
    """Reset result file before starting."""
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)

    """Main function to execute the script."""
    ticket_list = load_tickets(TICKET_FILE)
    driver = Driver(uc=True)
    driver.maximize_window()

    try:
        login(driver)
        for index, ticket in enumerate(ticket_list):
            print(f"Processing ticket {index + 1}/{len(ticket_list)}: {ticket}")
            result_text = process_ticket(driver, ticket, index)
            if result_text is not None:  # Only save if not rate limited
                save_result(result_text, RESULT_FILE)
            else:
                break  # Exit if rate limited
        print("Script completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
