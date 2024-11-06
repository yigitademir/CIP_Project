from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

# Set up the driver
path = "/Users/yigitalidemir/Desktop/HSLU/Lectures/CIP/CIP_Project/Individual_work_yigit/chromedriver"
service = Service(path)
driver = webdriver.Chrome(service=service)

# ActionChain
actions = ActionChains(driver)

# Navigate to website
driver.get("https://coincodex.com/")
time.sleep(2)


try:
    '''
    #Scroll down to the ethereum
    btc = driver.find_element(By.XPATH, "//a[@href = '/crypto/bitcoin/']")
    scroll_origin = ScrollOrigin.from_element(btc)
    actions.scroll_from_origin(scroll_origin,0, 1000)
    print("Scrolled down")
    '''
    #Close the ad banner
    try:
        close_banner = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close"))
        )
        close_banner.click()
        print("Banner closed")
    except:
        print("No banner")

    # Click on the Ethereum link
    ethereum_link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href = '/crypto/ethereum/']"))
    )
    print("Ethereum link found")
    ethereum_link.click()
    time.sleep(2)

    #Click on the historical data
    hist_data_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href = '/crypto/ethereum/historical-data/']"))
    )
    print("Historical data button found")
    hist_data_button.click()
    time.sleep(2)

    #Arrange time period
    time_period_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary"
    time_period_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, time_period_button_css))
    )
    print("Time period button found")
    time_period_button.click()

    start_date_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary.dateToggle > div.date-picker > app-date-range-picker > div > div > div > div.calendars > input[type=date]:nth-child(1)"
    end_date_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary.dateToggle > div.date-picker > app-date-range-picker > div > div > div > div.calendars > input[type=date]:nth-child(2)"
    select_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary.dateToggle > div.date-picker > app-date-range-picker > div > div > div > div.dates-select > div.select > button"
    start_date_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, start_date_button_css))
    )

    end_date_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, end_date_button_css))
    )

    select_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, select_button_css))
    )

    print("Start and End date button found")
    start_date_button.send_keys("01012021")
    time.sleep(1)
    end_date_button.send_keys("01012024")
    time.sleep(1)
    select_button.click()
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="formatted-table full-size-table").text
    print(table)


except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    print("Driver closed")