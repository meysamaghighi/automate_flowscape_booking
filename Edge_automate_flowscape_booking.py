# %%
# %%
# Author: Innovative originated by Mrs. Meysam Aghighi; and Highly improved by Wei Li ;)
# Contact: meysam.aghighi@gmail.com/meysam.aghighi@ericsson.com
# Date: 2024-11-08
# Description: A script to automate desk booking in flowscape

import json
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta
import os
from sys import exit

def read_flowscape_desk_yaml(file_path):
    building = None
    floor = None
    desk = None
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('building:'):
                building = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('floor:'):
                floor = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('desk:'):
                desk = line.split(':', 1)[1].strip().strip('"')
    
    if desk is None:
        print("The wanted desk is not provided.")
        exit(1)  # Exit the Python process with a non-zero status
    
    return building, floor, desk

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
    try:
        # Trigger the Book Pop-up Box Window    
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'sc-fzoCCn') and contains(@class, 'sc-pZQux') and contains(@class, 'fRfxGB')]"))
        )

        # Extract the first seat info from the span within class "sc-pRtcU"
        _seat = element.find_element(By.XPATH, ".//div[contains(@class, 'sc-pRtcU')]//span").text
        #print(f"Seat Info: {_seat}")

        # Extract the floor info from the second span element and split the content
        floor_info = element.find_elements(By.XPATH, ".//span")[1].text
        
        _floor, _building = [item.strip() for item in floor_info.split(',', 1)]
        
        # Extract the number of seats from the third span element
        num_seats = element.find_elements(By.XPATH, ".//span")[2].text
        
        BOLD = "\033[1m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        GREY = "\033[90m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        
        ### there is a bug, the Blocked is not identified below!!!!
        
        # Book the desk
        # _avai_stat = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root') and contains(@class, 'sc-qbDCV') and contains(@class, 'hMsIwa') and contains(@class, 'MuiPaper-elevation10') and contains(@class, 'MuiPaper-rounded')]//span[contains(@class, 'sc-fzonjX') and contains(@class, 'sc-qQKeD')]"))
        # ).text
        _avai_stat = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root')]//span[contains(@class, 'sc-fzonjX')]"))
        ).text


        # Check the availability status and set the color accordingly
        if _avai_stat.startswith("Booked"):
            color = RED
        elif _avai_stat.startswith("Available"):
            color = GREEN
        elif _avai_stat.startswith("Blocked"):
            color = GREY
        elif _avai_stat.startswith("Busy"):
            color = YELLOW        
        else:
            color = RESET

        # Print the formatted output
        print(f"{BOLD}Seat {_seat}: {color}{_avai_stat}{RESET}: \n\tBuilding: {_building.strip()}; {_floor.strip()}; Number of Seats: {num_seats}")
        
        ## if it is available, continue booking steps
        time.sleep(2)
        if not _avai_stat.startswith("Available"):    
            #########################################################
            # Wait until the sub-element with class 'sc-psDhf' exists
            sub_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sc-psDhf"))
            )
            
            if sub_element:
                # If the sub-element exists, find the element with class 'sc-qYUWV'
                element_qYUWV = sub_element.find_element(By.CLASS_NAME, "sc-qYUWV")
                
                if element_qYUWV:
                    # Extract the booking info within the span element
                    spans = element_qYUWV.find_elements(By.TAG_NAME, "span")
                    span_texts = [span.text for span in spans]
                    print(f"\tExisting Bookings: {span_texts}")
            
    except TimeoutException:
        print(f"\t{BOLD}{GREY}No booking info associated")

    # Book the desk
    # _avai_stat = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root') and contains(@class, 'sc-qbDCV') and contains(@class, 'hMsIwa') and contains(@class, 'MuiPaper-elevation10') and contains(@class, 'MuiPaper-rounded')]//span[contains(@class, 'sc-fzonjX') and contains(@class, 'sc-qQKeD')]"))
    # ).text
    _avai_stat = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root')]//span[contains(@class, 'sc-fzonjX')]"))
    ).text
    
    #print(f"Availability: {_avai_stat}")
    if _avai_stat.startswith("Available"):
        try:
            # book_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book')]"))
            # )
            # if book_button:
            #     book_button.click()
            #     print("SUCCESSFULLY BOOKED A SEAT!!!")
                # Wait until the button element with text "Book" is present
            book_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Book')]"))
            )
            #print("Book button is present!")

            # Simulate a click on the button
            book_button.click()
            print(f"\t{BOLD}{GREEN}SUCCESSFULLY BOOKED A SEAT!!!{RESET}")
            
        except TimeoutException:
            print(f"Error: Book button was not found!!!")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

# %%
### read the desired seat from a config file
file_path = 'flowscape-desk.yaml'
building, floor, desk = read_flowscape_desk_yaml(file_path)
print(f"Retrieving the wanted desk from file \"{file_path}\" :\n\tBuilding: {building}, Floor: {floor}, Desk: {desk}")

# %%
# %%
### Configuration Zone

from selenium.webdriver.edge.options import Options as EdgeOptions

edge_options = EdgeOptions()
## disable the USB warning messages
edge_options.add_argument("--disable-usb-keyboard-detect")
edge_options.add_argument("--disable-usb-discovery")

# Add any Edge-specific options here
#edge_options.add_argument("--kiosk")
edge_options.add_argument("--headless") 

#edge_options.add_argument("--profile-directory=Default")  # Use the default Edge profile
## use a dedicated new user data folder
edge_options.add_argument(f"--user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\Microsoft\\Edge\\Flowscape")
#edge_options.add_argument(f"--user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\Microsoft\\Edge\\User\\ Data")


# Initialize the Edge driver
driver = webdriver.Edge(options=edge_options)

# Get screen width and height
screen_width = driver.execute_script("return screen.width;")
screen_height = driver.execute_script("return screen.height;")

# Set the window size to half the screen width and full screen height
driver.set_window_size(screen_width // 2, screen_height)

# Set the window position to the right half of the screen
driver.set_window_position(screen_width // 2, 0)

# Go to webpage
print("Opening Flowscape Web site...")
flowscape_url="https://ericsson.flowscape.se/webapp/"
driver.get(flowscape_url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

try:
    # Wait and then Check if a redirection has occurred
    time.sleep(4) # a timer is needed for login redirect which may happen
    
    # Check if a redirection has occurred
    current_url = driver.current_url
    if current_url != flowscape_url:
        print(f"Redirected to: {current_url}")
        # Find and click the button on the redirected page
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='sc-jXbUNg jcveOs sc-kpDqfm dzkpkT']"))
        )
        if button:
            button.click()
            print("Auto login after redirected page!")
        else:
            print("Login Button not found on redirected page.")
    else:
        print("No Auto Login Needed")
except Exception as e:
    print(f"An error occurred: {e}")


# %%
## Function to select building and floor after the first-time login
def select_building_and_floor(driver, building, floor):
    try:    
        # Locate the "Select Building" element
        select_building_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//h4[text()='Select Building']"))
        )

        # Find the search box within the same container
        search_box = select_building_element.find_element(By.XPATH, "../div[@class='sc-fzoyTs jZUSDr']/input[@type='search']")

        # Fill in the building variable
        search_box.clear()
        time.sleep(2)
        search_box.send_keys(building)
        print(f"\tBuilding: {building}")
        
        # Select the Building provided in building variable
        buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='sc-fzqARJ gGnVyn']//button")))
        
        # Iterate through the building buttons to find the one with matching text
        for button in buttons:
            if button.text == building:
                button.click()
                break
                
        # Fill in the floor in the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-fzoNJl.loPePV'))
        )

        # Clear the search box
        search_box.clear()
        time.sleep(2)
        search_box.send_keys(floor)
        print(f"\tFloor: {floor}")
        
        # Select the provided floor in floor variable
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='sc-fzqARJ iQINDj']//button"))
        )

        # Iterate through the floor buttons to find the one with matching text
        for button in buttons:
            if button.text == floor:
                button.click()
                break
                                                
        Building_Floor_Selected = True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot for debugging
        driver.save_screenshot("screenshot_after_first_login_Error.png")
    
    return Building_Floor_Selected

# %%
# Check whether needs to provide building and floor info after the login (only applicable for the first time)
Building_Floor_Selected = False

try:
    # Wait for the element to be present in the DOM and visible
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h4[text()='Select Building']"))
    )
    print("Proving building and floor info after the new login... ")
    
    Building_Floor_Selected = select_building_and_floor(driver, building, floor)
except:
    print("Previously provided building and floor info found...")

# %%
from selenium.webdriver.common.action_chains import ActionChains

print(f"Locate the desired desk: {desk}@(Building {building} - {floor})...")

if not Building_Floor_Selected:
    try:
        # Find all elements with the class 'sc-fzoyAV fQsatj'
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-fzoyAV.fQsatj'))
        )

        # Ensure there are at least two elements
        if len(elements) >= 2:
            # Simulate a click on the second element
            second_element = elements[3]
            action = ActionChains(driver)
            action.move_to_element(second_element).click().perform()
        else:
            print("Cannot Pop-up the Select Build Box, Less than two elements found with the class 'sc-fzoyAV fQsatj'")    

        # Put the building in the search box element
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-fzoNJl.sc-fzoXWK.hnKkAN'))
        )

        # Clear the search box
        search_box.clear()

        # Input the variable into the search box
        search_box.send_keys(building)
        # Optionally, submit the search form if needed

        # Select the Building provided in building variable
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='sc-fzqARJ gGnVyn']//button"))
        )

        # Iterate through the building buttons to find the one with matching text
        for button in buttons:
            if button.text == building:
                button.click()
                break

        # Fill in the follow in the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-fzoNJl.loPePV'))
        )

        # Clear the search box
        search_box.clear()

        # Input the variable into the search box
        search_box.send_keys(floor)

        # Select the provided floor in floor variable
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='sc-fzqARJ iQINDj']//button"))
        )

        # Iterate through the floor buttons to find the one with matching text
        for button in buttons:
            if button.text == floor:
                button.click()
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot for debugging
        driver.save_screenshot("screenshot_reselect_building_floor_Error.png")   

# %%
# ## test different type of desk status
# #desk='168A'
# desk='122A'
# print(desk)
# #floor

# %%
# Look for the wanted desk and get a list which may contain wrong building and floor due to the flowscape bug!!!
time.sleep(2)
#search_box = driver.find_element(By.CLASS_NAME, 'sc-oTNDV.fBEiJb')
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'sc-oTNDV.fBEiJb'))
)

# Clear the search box
search_box.clear()
time.sleep(2)

# Input the variable into the search box
search_box.send_keys(desk)
time.sleep(5)

# Find the control modal
control_modal = driver.find_element(By.CLASS_NAME, "sc-pYA-dN.espQSf.control-modal")

# Initialize a list to remember elements
remembered_elements = []

# Iterate over the elements
elements = control_modal.find_elements(By.CLASS_NAME, "sc-qZtCU")
for element in elements:
    if "eOMlGi" in element.get_attribute("class"):
        building_text = element.find_element(By.CLASS_NAME, "sc-pkUbs.crfFDZ").text
        if building_text == building:
            continue
        else:
            break
    elif "cJnHnZ" in element.get_attribute("class"):
        _seat = element.find_element(By.CLASS_NAME, "sc-pHIBf.jLICbL").text
        avai_status = element.find_element(By.CLASS_NAME, "sc-pQEbo.iKmNOq").text
        remembered_elements.append((element, avai_status, _seat))
        #sub_element.click()
        #element.click()
        #time.sleep(20)

print(str(len(remembered_elements)) + " desks returned to further match with the wanted desk...")

# %%
## to tolerate the flowscape web bug, go through all the listed seats and identify the seat in the correct building and floor
desk_found=False
print("Matching retured list against the right floor and building ... ")

for e in remembered_elements:
    ## Double click on each listed desk is needed to iterate one by one !!!
    e[0].click() 
    e[0].click()

    # _avai_stat = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root') and contains(@class, 'sc-qbDCV') and contains(@class, 'hMsIwa') and contains(@class, 'MuiPaper-elevation10') and contains(@class, 'MuiPaper-rounded')]//span[contains(@class, 'sc-fzonjX') and contains(@class, 'sc-qQKeD')]"))
    # ).text

    _avai_stat = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root')]//span[contains(@class, 'sc-fzonjX')]"))
    ).text

    # Trigger the Book Pop-up Box Window    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'sc-fzoCCn') and contains(@class, 'sc-pZQux') and contains(@class, 'fRfxGB')]"))
    )

    # Extract the first seat info from the span within class "sc-pRtcU"
    _seat = element.find_element(By.XPATH, ".//div[contains(@class, 'sc-pRtcU')]//span").text

    # Extract the floor info from the second span element and split the content
    floor_info = element.find_elements(By.XPATH, ".//span")[1].text
    _floor, _building = [item.strip() for item in floor_info.split(',', 1)]
    
    # Extract the number of seats from the third span element
    num_seats = element.find_elements(By.XPATH, ".//span")[2].text
    
    ##@todo: there is yellow busy case not handled separately!
    
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    GREY = "\033[90m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    # Check the availability status and set the color accordingly
    if _avai_stat.startswith("Booked"):
        color = RED
    elif _avai_stat.startswith("Available"):
        color = GREEN
    elif _avai_stat.startswith("Blocked"):
        color = GREY
    elif _avai_stat.startswith("Busy"):
        color = YELLOW           
    else:
        color = RESET
        
    if (floor==_floor and building==_building and desk==_seat):
        desk_found=True
        _matchStr=f"{BOLD} {RED} The wanted desk identified: "
        # Print the formatted output
        print(_matchStr+f"{BOLD} \n\t{RESET}{BOLD} Building: {_building.strip()} - {_floor.strip()}; Seat {_seat}: {color}{_avai_stat}{RESET}: Number of Seats: {num_seats}")
        break

    # Print the formatted output
    print(f"\t\tBuilding: {_building.strip()} - {_floor.strip()}; {BOLD}Seat {_seat}: {color}{_avai_stat}{RESET}: Number of Seats: {num_seats}")    
    
    time.sleep(2)

if not desk_found:
    print(f"Wanted Seat {desk} cannot be found on Floor {floor} in Building {building} !!!")
    exit(-1)     

    

# %%
## this function works!!!
def click_next_month_button(driver):
    try:
        # Wait for the button to be clickable
        button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButtonBase-root.MuiIconButton-root.MuiPickersCalendarHeader-iconButton[tabindex="0"]'))
        )
        
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        
        # Click the button
        button.click()
        
        print("Button clicked successfully")
    except Exception as e:
        print("Error clicking button")
        print(e)

# Usage
#click_next_month_button(driver)

# %%
today = datetime.today()
dates = [(today + timedelta(days=i)).day for i in range(17)]
print('Booking started in range below!')
print(dates)

# Book desk in all dates
for date in dates:
    try:
        ## add month check based on tabindex element
        element = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'MuiButtonBase-root MuiIconButton-root MuiPickersDay-day') and not(contains(@class, 'MuiPickersDay-dayDisabled'))]//p[text()='{date}']"))
        )
        
        
        # Get the parent button element
        button = element.find_element(By.XPATH, './ancestor::button')
        
        #print(button.get_attribute('tabindex'))
        nextMonth = button.get_attribute('tabindex')
        
        if nextMonth=='-1':
            # Find the button element
            #monthButton = driver.find_element(By.CSS_SELECTOR, '.MuiButtonBase-root.MuiIconButton-root.MuiPickersCalendarHeader-iconButton')
            #monthButton.click()
            print("you need manully click next month")
            click_next_month_button(driver)
            element = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'MuiButtonBase-root MuiIconButton-root MuiPickersDay-day') and not(contains(@class, 'MuiPickersDay-dayDisabled'))]//p[text()='{date}']"))
                )
        
        element.click()
        time.sleep(2)
        print(f"date selected: {date}")
        time.sleep(2)
        
        # Book the desk
        press_book(driver)
    except Exception as e:
        print(f"Error selecting date: {date}")
        print(e)
    time.sleep(1)

# %%
print(f"\n{BOLD}{GREEN}DESK BOOKING FINISHED COMPLETELY!!!{RESET}\n\n")
driver.quit()