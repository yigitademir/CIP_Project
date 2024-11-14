import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# URL of the Treasury Yield Curve Rates page
url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202411'
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Accept cookies if the prompt appears
try:
    accept_cookies_button = driver.find_element(By.XPATH, '//button[text()="Accept All Cookies"]')
    accept_cookies_button.click()
    time.sleep(2)
except:
    pass  # If the button is not found, proceed

# Function to scrape data for a given year
def scrape_data_for_year(year_value):
    # Select the year from the dropdown using the provided option value
    select_element = Select(driver.find_element(By.ID, 'edit-field-tdr-date-value'))
    select_element.select_by_value(str(year_value))
    time.sleep(1)  # Short pause for dropdown selection

    # Click the "Apply" button
    apply_button = driver.find_element(By.ID, 'edit-submit-dfu-tool-page')
    apply_button.click()
    time.sleep(5)  # Wait for the page to update with new data

    # Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'views-table'})

    if not table:
        print(f"No table found for year value {year_value}")
        return None

    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = [col.text.strip() for col in row.find_all('td')]
        rows.append(cols)

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)
    df['Year'] = year_value  # Add year column for context
    return df

# Scrape data for the years 2024, 2023, 2022 and 2021
year_values = ['2024', '2023', '2022', '2021']
merged_data = pd.DataFrame()

for year_value in year_values:
    print(f"Scraping data for year value {year_value}...")
    df = scrape_data_for_year(year_value)
    if df is not None:
        merged_data = pd.concat([merged_data, df], ignore_index=True)
        print(f"Data for year value {year_value} scraped and merged.")

# Close the WebDriver
driver.quit()

# Sort the merged data by date column
merged_data['Date'] = pd.to_datetime(merged_data['Date'])  # Ensure 'Date' column is datetime type
merged_data = merged_data.sort_values(by='Date')


# Save the merged DataFrame to a new CSV file
merged_data.to_csv('Merged_Treasury_Yield_Curve.csv', index=False)
print("All data merged, sorted by date, and saved to Merged_Treasury_Yield_Curve.csv")
