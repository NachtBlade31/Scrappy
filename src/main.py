import undetected_chromedriver as uc
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def reserveTest(driver, BOOKED_SLOT_COUNT):
    ''' This function will book the slots on the slot booking page. 
    There can be maximum of 10 slots at one time . So we have defined BOOK_SLOT_COUNT and only run till its val is less then 11
    '''
    # Wait for the page to load and for the links to be updated
    wait = WebDriverWait(driver, 30)
    links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'reserve_')]")))

    while len(links) > 0 and BOOKED_SLOT_COUNT <= 10:
        links[0].click()
        BOOKED_SLOT_COUNT += 1
        # Wait for the links to be updated before finding them again
        wait.until(EC.staleness_of(links[0]))
        links = driver.find_elements(By.XPATH, "//*[contains(@id, 'reserve_')]")

    # Wait for the element to be clickable and perform the click action
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'largetext'))).click()

    return BOOKED_SLOT_COUNT



def bookSlot():
    username = "158892383281"
    password = "FdHhNt@D5h.5@S*"

    driver = uc.Chrome()
    driver.get('https://www.gov.uk/book-pupil-driving-test')

    # Wait for the "Start now" button to be clickable and perform the click action
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'govuk-button--start'))).click()

    # Halting the program to let user clear captcha
    time.sleep(60)

    # Find the username/email field and send the username itself to the input field
    driver.find_element("id", "user_id").send_keys(username)
    # Find the password input field and insert the password as well
    driver.find_element("id", "password").send_keys(password)
    # Click the login button
    driver.find_element("id", "continue").click()

    # Wait for the page to load before continuing
    time.sleep(30)

    while True:
        # Select the test field
        select = Select(driver.find_element("id", "testcentregroups"))
        select.select_by_value('157670')
        # TEST VALUE:157670
        # WEST VALUE:154230

        # Select "No" in disability and get the available slots
        driver.find_element("id", "specialNeedsChoice-noneeds").click()
        driver.find_element("id", "submitSlotSearch").click()

        slotAvailable = True
        clickedNextAvailable = False
        BOOKED_SLOT_COUNT = 0

        while slotAvailable and BOOKED_SLOT_COUNT <= 10:
            try:
                # Wait for the "Next available" link to be clickable and perform the click action
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'slotsavailable')))
                # Wait for the element to be clickable
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'slotsavailable')))
                element.click()
                clickedNextAvailable = False
                BOOKED_SLOT_COUNT = reserveTest(driver, BOOKED_SLOT_COUNT)

            except:
                try:
                    if clickedNextAvailable == False:
                        # Wait for the "Search for next weekly slots" link to be clickable and perform the click action
                        wait.until(EC.element_to_be_clickable((By.ID, 'searchForWeeklySlotsNextAvailable'))).click()
                        clickedNextAvailable = True
                    else:
                        slotAvailable = False
                except:
                    # Wait for the "Change test centre or date" link to be clickable and perform the click action
                    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'largetext'))).click()
                    clickedNextAvailable = False

        #if slotBooked==True:
            #send notification
            #print('send notification')

        # Wait for a minute before trying to book another slot
        time.sleep(60)


bookSlot()