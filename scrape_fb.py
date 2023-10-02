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
from supee import get_string_after_div
import time
import os

# Function to find elements, handle stale exception, and retry


def find_link_elements(driver):
    return driver.find_elements(By.XPATH, '//a[starts-with(@href, "https://www.facebook.com/")]')


def contains(input_string):
    words = input_string.split(' ')
    formatted_string = ' and '.join(
        [f'contains(text(), "{word}")' for word in words])
    return formatted_string


def wait_page_load(driver):
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    # Wait until a specific element is present
    wait.until(EC.presence_of_element_located((By.ID, 'facebook')))
    print("Page loaded...")


def filter_html_elements(elements):
    # Filter duplicates
    seen_names = set()
    filtered_elements = []

    for element in elements:
        inner_html = element.get_attribute('innerHTML')
        name = get_string_after_div(inner_html)
        if name and len(name.split()) >= 2 and name not in seen_names:
            print(f"Adding element with name: {name}")  # Debug log
            seen_names.add(name)
            filtered_elements.append(element)

    print(f"Filtered elements: {len(filtered_elements)}")  # Debug log
    return filtered_elements


def scrape_fb(name):

    # Load the .env file
    load_dotenv()

    # Access the variables
    email = os.getenv('FB_EMAIL')
    password = os.getenv('FB_PASSWORD')

    # Facebook login page URL
    login_url = "https://www.facebook.com"

    # Replace spaces with %20 for URL encoding
    dynamic_query_encoded = name.replace(' ', '%20')
    print(f"Encoded query: {dynamic_query_encoded}")

    # Facebook search page URL
    search_url = f"https://www.facebook.com/search/top/?q={dynamic_query_encoded}"

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

        # Fill in the email and password fields and submit the form
        wait_page_load(driver)
        print("logging in...")
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'pass')
        login_button = driver.find_element(By.NAME, 'login')
        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()

        # Navigate to the Facebook search page
        wait_page_load(driver)
        print(f"Navigating to: {search_url}")
        driver.get(search_url)

        # Wait for the page to load
        wait_page_load(driver)

        # Find elements with retry
        elements = find_link_elements(driver)

        # elements checkpoint
        filtered_elements = filter_html_elements(elements)
        
        # Open each profile and take a screenshot
        for i in range(len(filtered_elements)):
            if i == 5:
                break

            print(f"Processing profile {i}...")  # Debug log

            if filtered_elements:
                # Get the href value of the element
                href = filtered_elements[i].get_attribute('href')
                print(f"Loading: {href}")

                # Open the profile in a new tab
                driver.execute_script(f"window.open('{href}', '_blank');")

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                # Wait for the page to load
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.ID, 'facebook')))
                print("Page loaded...")

                print("Taking screenshot...")
                # Create a unique filename based on the current timestamp
                filename = f'profile_{int(time.time())}_{i}.png'
                filepath = os.path.join('screenshots', filename)

                # Take a screenshot and save it in the 'screenshots' directory
                driver.save_screenshot(filepath)

                print(f"Saved screenshot as {filename}.")  # Debug log

                # Close the tab and switch back to the main window
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                print("No elements present")  # Debug log

    finally:
        # Close the browser window
        driver.quit()
