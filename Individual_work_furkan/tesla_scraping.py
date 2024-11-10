from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Load the webpage
driver.get("https://finance.yahoo.com/quote/TSLA/history/?guccounter=1")

# reject privacy
# Locate and click the scroll-down button
try:
    scroll_down_btn_xpath = '//*[@id="scroll-down-btn"]'
    scroll_down_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, scroll_down_btn_xpath))
        )
    driver.execute_script("arguments[0].scrollIntoView(true);", scroll_down_btn)
    time.sleep(1)  # Small delay to ensure scroll completes
    scroll_down_btn.click()
except:
    pass

# Wait until the "Reject" button is visible and click it
try:
    reject_btn_xpath = '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]'
    reject_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, reject_btn_xpath))
    )
    reject_btn.click()
except:
    print("empty")

# Handle the intermediate page if it appears
try:
    # Wait for the "If you are not redirected" link to appear
    redirect_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "here"))
    )
    # Click the link to proceed
    redirect_link.click()
    print("Clicked the redirect link.")
except Exception as e:
    print("Redirect link not found; continuing if already on the target page.", e)

# Wait until the date button is clickable and then click it
wait = WebDriverWait(driver, 10)
date_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-ylk*='date-select']")))
time.sleep(3)
date_button.click()
time.sleep(5)

# Input Desired Date Range
wait.until(EC.presence_of_element_located((By.NAME, "startDate")))
time.sleep(3)
start_date = driver.find_element(By.NAME, "startDate")
end_date = driver.find_element(By.NAME, "endDate")

# Define desired dates
start_date.clear()
start_date.send_keys("01/01/2021")  # Example start date
time.sleep(3)
end_date.clear()
end_date.send_keys("01/01/2024")  # Example end date
time.sleep(3)

# Click the 'Done' button to apply date range
done_button = driver.find_element(By.CSS_SELECTOR, "button.primary-btn[data-ylk*='fltr']")
done_button.click()

# Extract the Data from the Loaded Table
time.sleep(2)  # Allow some time for the table to update

# Use BeautifulSoup to parse the table
soup = BeautifulSoup(driver.page_source, 'html.parser')
table_container = soup.find("div", class_=re.compile(r"\btable-container\b"))
table = table_container.find("table") if table_container else None

# Extract headers and rows
headers, historical_data = [], []
if table:
    header_row = table.find('thead').find_all('th')
    headers = [header.text.strip() for header in header_row]
    
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        historical_data.append(cols)
        

# Convert to DataFrame
df = pd.DataFrame(historical_data, columns=headers)
print(df)

# Save the DataFrame to a CSV file
df.to_csv("tesla_scrapped_data.csv", index=False)

# Close the browser
driver.quit()