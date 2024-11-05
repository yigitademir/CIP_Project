import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create a WebDriver instance
driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

# Define the URL for FRED
url = "https://fred.stlouisfed.org/"
driver.get(url)

# Wait for the page to load and search for interest rates
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "q"))
)
search_box.send_keys("interest rates")
search_box.submit()

# Wait for results to load
time.sleep(5)

# Scrape the page
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the relevant data table
# You may need to inspect the HTML structure to locate the data correctly
# This example assumes interest rates data is in a table with specific classes

tables = soup.find_all("table")

# Example of how to extract data (modify this based on actual HTML structure)
interest_rates = []
for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if cols:  # Check if the row has data
            interest_rates.append(cols)

# Convert the list to a DataFrame for easier manipulation
df = pd.DataFrame(interest_rates, columns=["Date", "Interest Rate"])
print(df)

# Clean up
driver.quit()
