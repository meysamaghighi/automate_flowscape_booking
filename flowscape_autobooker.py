# %%
# Author: Meysam Aghighi
# Contact: meysam.aghighi@gmail.com/meysam.aghighi@ericsson.com
# Date: 2024-11-08
# Description: A script to automate desk booking in flowscape

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta

# Libraries needed for handling Chrome cookies
import os
import sqlite3
from Cryptodome.Cipher import AES
import win32crypt  # Available on Windows for decrypting Chrome cookies
import json
import base64


# %%
def load_cookies(driver):
    # Load cookies from the saved JSON file
    with open("flowscape_cookies.json", "r") as f:
        cookies = json.load(f)

    # Add each cookie to the session
    for cookie in cookies:    
    #     cookie.pop('sameSite', None)
        driver.add_cookie(cookie)
        
    driver.refresh()

# %%
def press_book(driver):
        # Book the desk
        try:
            book_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book')]"))
            )
            book_button.click()
            print("SUCCESSFULLY BOOKED A SEAT!!!")
        except TimeoutException:
            print(f"Error: Book button was not found!!!")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

# %%
### Configuration Zone
today = datetime.today()

need_to_select_building_and_floor = False
# building = "SEKI10 Kista"
# floor = "Floor 8"
desk = "326A"
dates = [(today + timedelta(days=i)).day for i in range(16)]
# dates = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# %%
# Close all open Chrome instances
os.system("taskkill /f /im chrome.exe")

# Allow some time for Chrome processes to terminate
time.sleep(2)

# Open Chrome
chrome_options = Options() # this is important for cookies to work

chrome_options.add_argument("--user-data-dir=C:\\Users\\eaghmey\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--profile-directory=Default")  # Use the default Chrome profile

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

# Go to webpage
driver.get("https://ericsson.flowscape.se/webapp/")

# Load manually saved cookies (alternative option to loading default profile)
# load_cookies(driver)

# Only if need to select building and floor
if (need_to_select_building_and_floor):
    # Select building
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[text()='{building}']"))
    )
    button.click()
    # Select floor
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[text()='{floor}']"))
    )
    button.click()


print("Checking to see if we are on the right page...")
# (to-do) add code to click on "login" button


print(f"searching the desk {desk}...")
# Search the desk
search_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
)
search_field.send_keys(desk)
time.sleep(1)
print("click on the first search...")
# Open the first search (desk)
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'sc-qZtCU cJnHnZ')]"))
)
button.click()

print(f"looking at seat {desk}")
print(f"getting the div_element containing selected seat...")

# Get the element containing selected seat
div_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-pRtcU.iqDVFC span"))
    # EC.find_element_by_css_selector('div.sc-pRtcU.iqDVFC span')
)

selected_desk = div_element.text
print(f"selected desk = {selected_desk}")

# Check if the desk number matches the expected value
if selected_desk == desk:    
    # Book desk in all dates
    for date in dates:
        # Move to the next month if needed
        if (date == 1):
            print("going next month...")
            ## to-do: fix this part, current version doesn't work...
            button = driver.find_element(By.XPATH, f"//button[contains(@class, 'MuiPickersCalendarHeader-iconButton')]")
            driver.execute_script("arguments[0].click();", button)
            if button.is_displayed() and button.is_enabled():
                button.click()
            # next_month_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'MuiPickersCalendarHeader-iconButton')]"))
            # )
            # next_month_button.click()
        # Select date
        try:
            ## this part was so annoying to fix...
            element = WebDriverWait(driver, 10).until(
               EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'MuiButtonBase-root MuiIconButton-root MuiPickersDay-day') and not(contains(@class, 'MuiPickersDay-dayDisabled'))]//p[text()='{date}']"))
            )           
            element.click()
            print(f"date selected: {date}")
            # Book the desk
            press_book(driver)
        except Exception as e:
            print(f"Error selecting date: {date}")
            print(e)
        time.sleep(1)
else:
    print(f"Desk number found: {selected_desk}. No action performed. Check the code.")


