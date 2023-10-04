import os
import webbrowser
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

from scrape_fb import scrape_fb, login

names_file = "names.txt"
progress_file = "progress.txt"

if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        progress = int(f.read().strip())
else:
    progress = 0

with open(names_file, 'r') as f:
    names = f.readlines()

options = Options()
options.add_argument("--disable-notifications")

# Use the appropriate WebDriver executable path
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=options)

should_not_login = False

# Load the .env file
load_dotenv()

if "--bypass-login" in sys.argv:
    should_not_login = True

login(driver, should_not_login)

for i in range(progress, len(names)):
    name = names[i].strip()
    last_name, first_name = name.split(',')
    scrapable_name = f"{first_name.strip()} {last_name.strip()}"

    print(f"Searching for: {scrapable_name}")

    if "--scrape" in sys.argv:
        scrape_fb(driver, scrapable_name)
        continue

    if "--scrape" not in sys.argv:
        search_url = f"https://www.facebook.com/search/top/?q={first_name.strip()}%2{last_name.strip()}"
        webbrowser.open(search_url)
        continue

    with open(progress_file, 'w') as f:
        f.write(str(i + 1))

    if "--bypass-pause" not in sys.argv:
        input("Press Enter to continue to the next target...")

# Close the browser window
driver.quit()