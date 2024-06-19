import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# Read the CSV file
df = pd.read_csv('CSD.csv')

# Initialize the undetected Chrome WebDriver
driver = uc.Chrome()

def login(email, password):
    try:
        # Open a new tab and switch to it
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get('https://accounts.google.com/signin/v2/identifier')

        # Enter email and proceed
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'identifierId'))
        )
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)

        # Wait for the transition to the password input
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )

        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, 'Passwd'))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Check for successful login
        WebDriverWait(driver, 20).until(
            EC.url_contains("mail.google.com")
        )
        print(f"Logged in successfully with {email}")

    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Failed to log in with {email}. Error: {e}")
        # Optional: Print page source or take a screenshot for debugging
        with open(f"page_source_{email}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot(f"screenshot_{email}.png")
    
    finally:
        # Close the tab
        driver.close()
        # Switch back to the first tab
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])

for index, row in df.iterrows():
    login(row['Email'], row['Password'])

driver.quit()
