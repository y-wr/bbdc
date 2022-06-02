import time
from playsound import playsound
from pyautogui import moveTo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


# Login details:
USERNAME = "..."
PASSWORD = "..."

# Format = ["dd/mm/yyyy","dd/mm/yyyy", (...)]
DESIRED_DATES = ["02/11/2022"]

# Format = ["1", "2", "3", "4", "5"]
# For all session, leave empty.
DESIRED_SESS = []

# Time between refresh interval (seconds).
INTERVAL = 10

# No need to change.
WAIT = 5


# Load page.
def load_page():

    driver = webdriver.Safari()
    driver.maximize_window()
    driver.implicitly_wait(20)
    driver.get("https://info.bbdc.sg/members-login/")
    print("Page Loaded.")

    return driver


# Login into page.
def login(driver, username=USERNAME, password=PASSWORD):

    # Key in username.
    driver.find_element(By.ID, "txtNRIC").click()
    driver.find_element(By.ID, "txtNRIC").send_keys(username)
    print(USERNAME + " --> SUCCESS")
    time.sleep(WAIT)

    # Key in password.
    driver.find_element(By.ID, "txtPassword").click()
    driver.find_element(By.ID, "txtPassword").send_keys(password)
    print(PASSWORD + " --> SUCCESS")
    time.sleep(WAIT)

    # Click log in button.
    driver.find_element(By.ID, "loginbtn").click()
    print("Logged In.")


# Switch to frame and click on prac.
def booking_page(driver):

    driver.switch_to.frame(1)
    print("Switched to LeftFrame.")
    driver.find_element(By.LINK_TEXT, "Booking without Fixed Instructor").click()
    print("Selected Booking Page.")


def select_slots(driver):

    # Accept reminder.
    driver.switch_to.default_content()
    driver.switch_to.frame(2)
    driver.find_element(By.CSS_SELECTOR, "input[value='I Agree']").click()
    print("Reminder Accepted.")
    time.sleep(WAIT)

    # Select month parameters.
    for month in driver.find_elements(By.CSS_SELECTOR, "input[type=checkbox][id='checkMonth']"):
        month.click()
    print("Month Selected.")

    # Select session parameters.
    if len(DESIRED_SESS) == 0:
        driver.find_element(
            By.CSS_SELECTOR, "input[type=checkbox][name='allSes']"
        ).click()
    else:
        for day in DESIRED_SESS:
            driver.find_element(
                By.CSS_SELECTOR, f"input[type=checkbox][value='{day}']"
            ).click()
    print("Session Selected.")

    # Select day parameters.
    driver.find_element(By.CSS_SELECTOR, "input[type=checkbox][name='allDay']").click()
    print("Day Selected.")

    driver.find_element(By.NAME, "btnSearch").click()
    print("Search Clicked.")
    time.sleep(WAIT)


def check_dates(driver):

    # Dismiss alert.
    try:
        driver.switch_to.alert.dismiss()
        print("Alert Dismissed.")
    except:
        pass

    # Find the table that contains the dates.
    table = driver.find_element(
        By.CSS_SELECTOR, "table[bgcolor='#666666'][cellspacing='1'][cellpadding='2']"
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Iterate through the rows to extract each date.
    slots = []
    for row in rows[2:]:
        data = row.find_elements(By.TAG_NAME, "td")
        date = data[0].text[:10]
        slots.append(date)

    return slots


def refresh(driver):

    # Select back button.
    driver.find_element(By.CSS_SELECTOR, "input[value='<< Back']").click()
    moveTo(500, 500)

    # Click search button.
    while True:
        try:
            driver.find_element(By.NAME, "btnSearch").click()
            return
        except:
            try:
                if driver.find_element(By.CSS_SELECTOR, "font[size='5']").text == "REMINDER NOTICE":
                    select_slots(driver)
                    return
            except:
                continue
        
            continue


def alert(slots):

    # Add matched slots to list.
    available = []
    for slot in slots:
        if slot in DESIRED_DATES:
            available.append(slot)
            print(f"{slot} AVAILABLE")

    # Play alert if slots found.
    if len(available) != 0:
        playsound("alert.wav")
    else:
        print("No Slot Found.")

    return


def main():

    driver = load_page()
    login(driver)
    time.sleep(2 * WAIT)  # To clear unsecure form warning.
    booking_page(driver)
    time.sleep(WAIT)
    select_slots(driver)
    time.sleep(WAIT)

    count = 0
    while True:
        print(f"\n\nRefresh Count: {count}")
        slots = check_dates(driver)
        alert(slots)
        time.sleep(INTERVAL)
        refresh(driver)
        count += 1
        time.sleep(WAIT * 2)


if __name__ == "__main__":
    main()
