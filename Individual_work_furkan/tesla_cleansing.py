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

# Step 4: Rename columns for clarity
tesla_data_cleaned = tesla_data_cleaned.rename(columns={
    'Close    Close price adjusted for splits.': 'Close',
    'Adj Close    Adjusted close price adjusted for splits and dividend and/or capital gain distributions.': 'Adj_Close'
})

# Step 5: Check if 'Close' and 'Adj_Close' columns are identical
are_columns_identical = tesla_data_cleaned['Close'].equals(tesla_data_cleaned['Adj_Close'])

# If columns are identical, remove the 'Adj_Close' column
if are_columns_identical:
    tesla_data_cleaned = tesla_data_cleaned.drop(columns=['Adj_Close'])
    
print("Are the 'Close' and 'Adj_Close' columns identical?:", are_columns_identical)

# Step 6: Add a new column: the difference between 'High' and 'Low' columns
tesla_data_cleaned['High'] = pd.to_numeric(tesla_data_cleaned['High'], errors='coerce')
tesla_data_cleaned['Low'] = pd.to_numeric(tesla_data_cleaned['Low'], errors='coerce')
tesla_data_cleaned['High_Low_Diff'] = tesla_data_cleaned['High'] - tesla_data_cleaned['Low']

# Step 7: Add a new column: change in 'Close' compared to the previous day
tesla_data_cleaned['Close_Change'] = tesla_data_cleaned['Close'].pct_change() * 100

#Step 7: preview of the cleaned dataset
total_rows, total_columns = tesla_data_cleaned.shape
print(f"\nTotal Rows: {total_rows}, Total Columns: {total_columns}")
print("\nPreview of Cleaned Dataset:\n", tesla_data_cleaned.head())

df = pd.DataFrame(tesla_data_cleaned)
print(df)
df.to_csv("historical_data_cleaned.csv", index=False)