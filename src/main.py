
from undetected_chromedriver import ChromeOptions,Chrome
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def reserveTest(driver, BOOKED_SLOT_COUNT):
    ''' This function will book the slots on the slot booking page. 
    There can be maximum of 10 slots at one time . So we have defined BOOK_SLOT_COUNT and only run till its val is less then 11
    '''
    # Wait for the page to load and for the links to be updated
    try:

        wait = WebDriverWait(driver, 30)
        links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'reserve_')]")))
        print("Links Identified...........")
        while len(links) > 0 and BOOKED_SLOT_COUNT <= 10:
            links[0].click()
            print("Slot Booked..............................")
            BOOKED_SLOT_COUNT += 1
            # Wait for the links to be updated before finding them again
            wait.until(EC.staleness_of(links[0]))
            links = driver.find_elements(By.XPATH, "//*[contains(@id, 'reserve_')]")

        # Wait for the element to be clickable and perform the click action
        print("returning to Booking page............................................")
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'largetext'))).click()

        return BOOKED_SLOT_COUNT
    except Exception as e:
        print(str(e))



def bookSlot():
    try:
        username = "158892383281"
        password = "FdHhNt@D5h.5@S*"

        print("Starting the Chrome")
        try:
            chrome_options = ChromeOptions()

            # Add the debugging argument to the options object
            chrome_options.add_argument("--remote-debugging-port=9222")

            driver = Chrome(options=chrome_options)
        except Exception as e:
            print(str(e))
            time.sleep(30)
        print("Opening the site")
        driver.get('https://www.gov.uk/book-pupil-driving-test')

        # Wait for the "Start now" button to be clickable and perform the click action
        wait = WebDriverWait(driver, 10)

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'govuk-button--start'))).click()

        # Halting the program to let user clear captcha
        time.sleep(30)
        print("Logging In --------")
        # Find the username/email field and send the username itself to the input field
        driver.find_element("id", "user_id").send_keys(username)
        # Find the password input field and insert the password as well
        driver.find_element("id", "password").send_keys(password)
        # Click the login button
        driver.find_element("id", "continue").click()

        # Wait for the page to load before continuing
        time.sleep(15)
        print("Logged In --------")
        # Select the test field
        print("Selecting the test location as WEST and finding slots---------------------")
        select = Select(driver.find_element("id", "testcentregroups"))
        select.select_by_value('154230')
        # TEST VALUE:157670
        # WEST VALUE:154230

        # Select "No" in disability and get the available slots
        driver.find_element("id", "specialNeedsChoice-noneeds").click()
        driver.find_element("id", "submitSlotSearch").click()

        print("Checking slots")

        while True:
            print("################################################")
            print("New Search Cycle started")
            slotAvailable = True
            clickedNextAvailable = False
            BOOKED_SLOT_COUNT = 0
            while slotAvailable and BOOKED_SLOT_COUNT <= 10:
                try:
                    DONE=False
                    # Wait for the "Next available" link to be clickable and perform the click action
                    wait = WebDriverWait(driver, 10)
                    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'slotsavailable')))
                    print("Aavailable slots identified.........................")
                    # Wait for the element to be clickable
                    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'slotsavailable')))
                    element.click()
                    clickedNextAvailable = False
                    print("Reserving slots...........................")
                    BOOKED_SLOT_COUNT = reserveTest(driver, BOOKED_SLOT_COUNT)

                except:
                    try:
                        print("No slot found this week...............................")
                        if clickedNextAvailable == False:
                            print("Checking next available for slot........................")
                            # Wait for the "Search for next weekly slots" link to be clickable and perform the click action
                            wait.until(EC.element_to_be_clickable((By.ID, 'searchForWeeklySlotsNextAvailable'))).click()
                            clickedNextAvailable = True
                        else:
                            print("No slot available any time ................................")
                            slotAvailable = False
                            DONE=True
                    except:
                        # Wait for the "Change test centre or date" link to be clickable and perform the click action
                        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'largetext'))).click()
                        clickedNextAvailable = False

                if BOOKED_SLOT_COUNT==10:
                    DONE=True

            # Wait for a minute before trying to book another slot
                if DONE==True:

                    if BOOKED_SLOT_COUNT>0:
                        print("Slots found. Sleeping for 15 mins")
                        time.sleep(10*60)
                    else:
                        print("Slots Not found. Sleeping for 5 seconds")
                        time.sleep(5)
                    wait = WebDriverWait(driver, 5)
                    try:
                        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'homeIcon'))).click()
                    except:
                        try:
                            wait.until(EC.element_to_be_clickable((By.ID, 'searchForWeeklySlotsPreviousAvailable'))).click()
                        except:
                            continue
                    print("Cycle complete ")
                    print("**********************************************************************")
    except Exception as e:
        print(str(e))
        time.sleep(60)


if __name__=="__main__":
    bookSlot()