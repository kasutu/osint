from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

# Function to find elements, handle stale exception, and retry
def find_elements_with_retry(driver, xpath):
    try:
        return driver.find_elements(By.XPATH, xpath)
    except StaleElementReferenceException:
        # If StaleElementReferenceException occurs, wait and retry
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        return driver.find_elements(By.XPATH, xpath)
    except Exception as e:
        print(f"Exception occurred: {e}. Falling back to find <a> element with href 'https://www.facebook.com/'")
        return driver.find_elements(By.XPATH, '//a[starts-with(@href, "https://www.facebook.com/")]')

def contains(input_string):
      words = input_string.split(' ')
      formatted_string = ' and '.join([f'contains(text(), "{word}")' for word in words])
      return formatted_string

def scrape_fb(name):
    dynamic_query = name.replace(' ', '%20')

    # Load the .env file
    load_dotenv()

    # Access the variables
    email = os.getenv('FB_EMAIL')
    password = os.getenv('FB_PASSWORD')

    # Facebook login page URL
    login_url = "https://www.facebook.com"

    # Facebook search page URL
    search_url = "https://www.facebook.com/search/top/?q=" + dynamic_query

    # Set up Chrome options
    options = Options()
    options.add_argument("--disable-notifications")

    # Use the appropriate WebDriver executable path
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # Create a directory for the screenshots
    os.makedirs('screenshots', exist_ok=True)

    try:
        # Navigate to the Facebook login page
        driver.get(login_url)

        # Wait for the page to load (adjust the time based on your network speed)
        driver.implicitly_wait(10)

        # Fill in the email and password fields and submit the form
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'pass')
        login_button = driver.find_element(By.NAME, 'login')

        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()

        # Navigate to the Facebook search page
        driver.get(search_url)

        # Wait for the page to load
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Navigate to the Facebook search page
                driver.get(search_url)

                # Wait for the page to load
                wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
                wait.until(EC.presence_of_element_located((By.ID, 'facebook')))  # Wait until a specific element is present

                print("Page loaded...")
                break  # If the page loads successfully, break the loop
            except TimeoutException:
                print(f"Page load timed out. Retrying ({attempt+1}/{max_attempts})...")

        # Replace spaces with %20 for URL encoding
        dynamic_query_encoded = dynamic_query.replace('%20', ' ')

        # Find elements with retry
        print(f'searching for {dynamic_query_encoded}')
        elements = find_elements_with_retry(driver, f'//a[{contains(dynamic_query_encoded)}]')
          
        # Open each profile and take a screenshot
        for i in range(len(elements)):
            print(f"Processing profile {i}...")  # Debug log
          
            if elements:
              # Get the href value of the element
              href = elements[i].get_attribute('href')
              print(href)

              # Open the profile in a new tab
              driver.execute_script(f"window.open('{href}');")
              driver.switch_to.window(driver.window_handles[-1])

              # Wait for the page to load
              wait = WebDriverWait(driver, 15)  # Wait up to 10 seconds
              wait.until(EC.presence_of_element_located((By.ID, 'facebook')))  # Wait until a specific element is present
    
              # Take a screenshot and save it in the 'screenshots' directory
              driver.save_screenshot(f'screenshots/profile{i}.png')

              print(f"Saved screenshot for profile {i+1}.")  # Debug log

              # Close the tab and switch back to the main window
              driver.close()
              driver.switch_to.window(driver.window_handles[0])
            else:
                print("No elements present")  # Debug log

    finally:
        # Close the browser window
        driver.quit()
