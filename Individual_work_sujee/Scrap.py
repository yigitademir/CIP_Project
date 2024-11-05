from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set up Selenium options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (optional)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver (replace with the path to your ChromeDriver)
driver = webdriver.Chrome(options=options)

# Define the URL for the 10-Year Bond Yield historical data on Investing.com
url = 'https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data'

try:
    # Open the URL
    driver.get(url)

    # Accept cookies if prompted
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]"))
        )
        cookie_button.click()
    except Exception as e:
        print("No cookie prompt found:", e)

    # Wait for the date picker to load and set custom dates
    time.sleep(2)  # Adjust this wait time if necessary
    date_picker = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".datePickerIconWrap"))
    )
    date_picker.click()

    # Set the start date to 01-01-2021
    start_date_input = driver.find_element(By.CSS_SELECTOR, "#startDate")
    start_date_input.clear()
    start_date_input.send_keys("01/01/2021")

    # Set the end date to today's date
    end_date_input = driver.find_element(By.CSS_SELECTOR, "#endDate")
    end_date_input.clear()
    end_date_input.send_keys(time.strftime("%m/%d/%Y"))

    # Apply the date range
    apply_button = driver.find_element(By.CSS_SELECTOR, ".applyBtn")
    apply_button.click()

    # Wait for the data to load
    time.sleep(5)  # Adjust based on your internet speed and page loading time

    # Extract page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table containing historical data
    table = soup.find("table", {"class": "historicalTbl"})

    # Parse the data into a structured format
    data = []
    for row in table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        if len(cols) > 1:
            date = cols[0].text.strip()
            price = cols[1].text.strip()
            open_ = cols[2].text.strip()
            high = cols[3].text.strip()
            low = cols[4].text.strip()
            change = cols[5].text.strip()
            data.append([date, price, open_, high, low, change])

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["Date", "Price", "Open", "High", "Low", "Change"])

    # Display the scraped data
    print(df)

    # Optional: Save to CSV
    df.to_csv("us_10_year_bond_yield.csv", index=False)
    print("Data saved to us_10_year_bond_yield.csv")

finally:
    # Close the WebDriver
    driver.quit()
