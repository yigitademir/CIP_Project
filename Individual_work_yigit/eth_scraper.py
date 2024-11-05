from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the driver
path = "/chromedriver"
service = Service(path)
driver = webdriver.Chrome(service=service)

# ActionChain
actions = ActionChains(driver)

# Navigate to website
driver.get("https://coinmarketcap.com/")
time.sleep(2)

try:
    # Click on the Ethereum link
    ethereum_link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[2]/td[3]/div/a"))
    )
    print("Ethereum link found")
    ethereum_link.click()
    time.sleep(1)

    # Click on the "More information" button
    info_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-role='btn-content-item']"))
    )
    print("Info button found")
    info_button.click()
    time.sleep(1)

    # Handle the cookie popup
    try:
        accept_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        print("Cookie popup found")
        accept_cookies_button.click()
        time.sleep(1)

        # Locate the close button and click it
        close_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sc-4c05d6ef-0.dMwnWW.close-button"))
        )
        print("Close button found")
        close_button.click()
        time.sleep(1)
    except:
        print("Cookie or Pop-up error")

    # Wait for the block element to load
    block_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/section/div/div[8]"))
    )
    print("Block element found")

    # Use ActionChains to scroll to the block element
    actions.move_to_element(block_element).perform()
    print("Scrolled to block element")

    # Click the "See historical data" button
    hist_data_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/currencies/ethereum/historical-data/')]"))
    )
    print("Historical data button found")
    hist_data_button.click()
    time.sleep(2)

    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.BaseButton_base__34gwo.BaseButton_v-tertiary__AhlyE"))
    )

    hist_data_button.click()
    top_button = driver.find_element(By.CLASS_NAME, "sc-b36483b8-1 jXInTK")
    top_button.click()


    time.sleep(5)

except:
    print("Error")

finally:
    driver.quit()
    print("Driver closed")

