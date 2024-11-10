import pandas as pd

tesla_data = pd.read_csv('historical_data_scrapped.csv')

# Step 1: Identify data types of each column
data_types = tesla_data.dtypes
print("Data Types:\n", data_types)

# Step 2: Check for NA values
na_summary = tesla_data.isna().sum()
print("\nNA Value Summary:\n", na_summary)

# Step 3: Remove rows with NA values and completely empty rows
tesla_data_cleaned = tesla_data.dropna(how='any').copy()


tesla_data_cleaned['Date'] = pd.to_datetime(tesla_data_cleaned['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

tesla_data_cleaned = tesla_data_cleaned.sort_values(by='Date', ascending=True).reset_index(drop=True)

# Step 4: Rename columns for clarity
tesla_data_cleaned = tesla_data_cleaned.rename(columns={
    'Open': 'Tesla_Open',
    'High': 'Tesla_High',
    'Low': 'Tesla_Low',
    'Close    Close price adjusted for splits.': 'Tesla_Close',
    'Adj Close    Adjusted close price adjusted for splits and dividend and/or capital gain distributions.': 'Tesla_Adj_Close'
})

# Step 5: Check if 'Tesla_Close' and 'Tesla_Adj_Close' columns are identical
are_columns_identical = tesla_data_cleaned['Tesla_Close'].equals(tesla_data_cleaned['Tesla_Adj_Close'])

# If columns are identical, remove the 'Tesla-Adj_Close' column
if are_columns_identical:
    tesla_data_cleaned = tesla_data_cleaned.drop(columns=['Tesla_Adj_Close'])
    
print("Are the 'Close' and 'Adj_Close' columns identical?:", are_columns_identical)

# Step 6: Add a new column: the difference between 'High' and 'Low' columns
tesla_data_cleaned['Tesla_High'] = pd.to_numeric(tesla_data_cleaned['Tesla_High'], errors='coerce')
tesla_data_cleaned['Tesla_Low'] = pd.to_numeric(tesla_data_cleaned['Tesla_Low'], errors='coerce')
tesla_data_cleaned['Tesla_Intraday_Range'] = tesla_data_cleaned['Tesla_High'] - tesla_data_cleaned['Tesla_Low']

# Step 7: Add a new column: change in 'Close' compared to the previous day
tesla_data_cleaned['Tesla_1D%'] = tesla_data_cleaned['Tesla_Close'].pct_change() * 100

tesla_data_cleaned['Tesla_1D%'] = tesla_data_cleaned['Tesla_1D%'].fillna(0)

#Step 7: preview of the cleaned dataset
total_rows, total_columns = tesla_data_cleaned.shape
print(f"\nTotal Rows: {total_rows}, Total Columns: {total_columns}")
print("\nPreview of Cleaned Dataset:\n", tesla_data_cleaned.head())

tesla_data_cleaned.to_csv("tesla_prices.csv", index=False)
