import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Initialize the Web Driver
driver = webdriver.Chrome()  # Ensure that ChromeDriver is installed and in your PATH

try:
    # Open the specific FRED series page for Effective Federal Funds Rate
    url = 'https://fred.stlouisfed.org/series/RIFSPFFNB'
    driver.get(url)

    # Wait for the historical data table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'fred-table'))
    )

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the historical data table
    data_table = soup.find('table', class_='fred-table')

    # Extract data from the table
    rows = data_table.find_all('tr')
    data = []

    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        if len(columns) == 2:  # Ensure there are two columns (Date and Rate)
            date = columns[0].text.strip()
            rate = columns[1].text.strip()
            data.append({'Date': date, 'Rate': rate})

    # Convert the list of dictionaries to a DataFrame
    interest_rates_df = pd.DataFrame(data)

    # Filter the DataFrame for dates between 2021 and 2024
    interest_rates_df['Date'] = pd.to_datetime(interest_rates_df['Date'])
    filtered_rates_df = interest_rates_df[(interest_rates_df['Date'] >= '2021-01-01') &
                                          (interest_rates_df['Date'] <= '2024-12-31')]

    # Save the filtered DataFrame to a CSV file
    filtered_rates_df.to_csv('federal_funds_rate_2021_2024.csv', index=False)

finally:
    # Close the driver
    driver.quit()
