from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the driver
driver = webdriver.Chrome()

# ActionChain
actions = ActionChains(driver)

# Part 1 Navigate to website
driver.get("https://coincodex.com/")
time.sleep(2)

try:
    #Close the ad banner
    try:
        close_banner = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close"))
        )
        close_banner.click()
        print("Banner closed.")
    except:
        print("No banner.")

    # Click on the Ethereum link
    ethereum_link = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href = '/crypto/ethereum/']"))
    )
    print("Ethereum link found.")
    actions.move_to_element(ethereum_link).perform()
    time.sleep(2)
    ethereum_link.click()

    #Click on the historical data
    hist_data_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href = '/crypto/ethereum/historical-data/']"))
    )
    print("Historical data button found.")
    hist_data_button.click()

    # Find and click time period button
    time_period_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary"
    time_period_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, time_period_button_css))
    )
    print("Time period button found.")
    time_period_button.click()

    # Find field for start and en date
    start_date_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary.dateToggle > div.date-picker > app-date-range-picker > div > div > div > div.calendars > input[type=date]:nth-child(1)"
    end_date_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary.dateToggle > div.date-picker > app-date-range-picker > div > div > div > div.calendars > input[type=date]:nth-child(2)"
    select_button_css = "body > app-root > app-root > div > div > div > div > app-coin-history-data > section.seo-section.section-container > div > div.options-bar.d-flex.justify-content-between.align-items-center > div.date-select.button.button-secondary.dateToggle > div.date-picker > app-date-range-picker > div > div > div > div.dates-select > div.select > button"

    start_date_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, start_date_button_css))
    )

    end_date_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, end_date_button_css))
    )

    select_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, select_button_css))
    )
    print("Start and End date button found.")

    # Send date input
    start_date = "01012021"
    end_date = "01012024"

    start_date_button.send_keys(start_date)
    time.sleep(1)
    end_date_button.send_keys(end_date)
    time.sleep(1)
    select_button.click()
    print("Given time-period selected.")
    time.sleep(2)

    # Part 2 BeautifulSoup Scrape
    data = []
    print("Scrape starting...")

    # Iterate through all pages.
    for i in range(37):
        # Check if the first popup appears
        try:
            first_popup_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID, "onesignal-slidedown-cancel-button"))
            )
            time.sleep(1)
            first_popup_button.click()
            print("First popup closed.")
            time.sleep(1)

            # Check if the second popup appears
            try:
                second_popup_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.ID, "onesignal-slidedown-cancel-button"))
                )
                second_popup_button.click()
                print("Second popup closed.")

            except:
                print("No second popup detected.")

        except:
            print("No popup detected.")

        # Parse/Update the page source
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="formatted-table full-size-table")

        #Get the headers from first row
        if i == 0:
            headers = [header.text for header in table.find_all("th")]

        # Proceed with scraping the table data
        rows = table.find_all("tr")
        for row in rows[1:]:
            cells = row.find_all("td")
            data.append([cell.text.strip() for cell in cells])
        print("Page", i+1, "completed.")

        # Move to the page indicator and click to go to the next page except last page
        if i != 36:
            page_indicator = driver.find_element(By.XPATH, "//a[@aria-label = 'Next']")
            actions.move_to_element(page_indicator).perform()
            page_indicator.click()
            time.sleep(1)

    #Create dataframe
    df = pd.DataFrame(data, columns=headers)
    print(df)
    df.to_csv("eth_scraped_data.csv", index=False)
    print("Data scraped.")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    print("Driver closed.")