import pandas as pd

tesla_data = pd.read_csv('tesla_scraped_data.csv')

# Identify data types of each column
data_types = tesla_data.dtypes
print("Data Types:\n", data_types)

# Check for NA values
na_summary = tesla_data.isna().sum()
print("\nNA Value Summary:\n", na_summary)

# Remove rows with NA values and completely empty rows
tesla_data_cleaned = tesla_data.dropna(how='any').copy()

# Change the Date types to YYYY-MM-DD
tesla_data_cleaned['Date'] = pd.to_datetime(tesla_data_cleaned['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Sort by 'Date' in ascending order 
tesla_data_cleaned = tesla_data_cleaned.sort_values(by='Date', ascending=True).reset_index(drop=True)

# Rename columns for clarity
tesla_data_cleaned = tesla_data_cleaned.rename(columns={
    'Open': 'Tesla_Open',
    'High': 'Tesla_High',
    'Low': 'Tesla_Low',
    'Close    Close price adjusted for splits.': 'Tesla_Close',
    'Adj Close    Adjusted close price adjusted for splits and dividend and/or capital gain distributions.': 'Tesla_Adj_Close'
})

# Check if 'Tesla_Close' and 'Tesla_Adj_Close' columns are identical
are_columns_identical = tesla_data_cleaned['Tesla_Close'].equals(tesla_data_cleaned['Tesla_Adj_Close'])

# Typically keep 'Adj_Close' for accuracy, but removing here as it's identical to 'Close' 
# If columns are identical, remove the 'Tesla-Adj_Close' column
if are_columns_identical:
    tesla_data_cleaned = tesla_data_cleaned.drop(columns=['Tesla_Adj_Close'])
    
print("Are the 'Close' and 'Adj_Close' columns identical?:", are_columns_identical)

# Add a new column: the difference between 'High' and 'Low' columns
tesla_data_cleaned['Tesla_High'] = pd.to_numeric(tesla_data_cleaned['Tesla_High'], errors='coerce')
tesla_data_cleaned['Tesla_Low'] = pd.to_numeric(tesla_data_cleaned['Tesla_Low'], errors='coerce')
tesla_data_cleaned['Tesla_Intraday_Range'] = round(tesla_data_cleaned['Tesla_High'] - tesla_data_cleaned['Tesla_Low'], 2)

# Add a new column: change in 'Close' compared to the previous day
tesla_data_cleaned['Tesla_1D%'] = round(tesla_data_cleaned['Tesla_Close'].pct_change() * 100, 2)

tesla_data_cleaned['Tesla_1D%'] = tesla_data_cleaned['Tesla_1D%'].fillna(0)

# preview of the cleaned dataset
total_rows, total_columns = tesla_data_cleaned.shape
print(f"\nTotal Rows: {total_rows}, Total Columns: {total_columns}")
print("\nPreview of Cleaned Dataset:\n", tesla_data_cleaned.head())

tesla_data_cleaned.to_csv("tesla_prices.csv", index=False)
