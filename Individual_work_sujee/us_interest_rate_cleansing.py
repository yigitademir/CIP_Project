import pandas as pd

# Load the data
df = pd.read_csv('Merged_Treasury_Yield.csv')

# Additional Column
df['10 Yr'] = pd.to_numeric(df['10 Yr'], errors='coerce')  # Convert to numeric, handle errors
df['2 Yr'] = pd.to_numeric(df['2 Yr'], errors='coerce')  # Convert to numeric, handle errors

# Add a new column for the Yield Curve Spread (10Y - 2Y)
df['Yield Curve Spread'] = df['10 Yr'] - df['2 Yr']

# Cleaning steps:

# 1. Remove the columns '4 Mo' and 'Year' if they exist
columns_to_drop = ['4 Mo', 'Year']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# 2. Handle Missing Values - Drop columns with more than 50% missing values and fill others with median value
threshold = 0.5 * len(df)
df = df.dropna(axis=1, thresh=int(threshold))  # Drop columns
df.fillna(df.median(numeric_only=True), inplace=True)  # Fill remaining NaNs with median

# 3. Rename Columns for Consistency
df.columns = df.columns.str.replace('.', '', regex=False).str.replace(' ', '_').str.lower()

# 4. Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 5. Check and Drop Duplicates
df.drop_duplicates(inplace=True)

# 6. Change all numeric values to two decimal points except for 'date'
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = df[numeric_cols].round(2)

# 7. Rename columns without modifying 'date'
new_column_names = {col: f"rate_{col}" for col in df.columns if col != 'date'}
df.rename(columns=new_column_names, inplace=True)

# Save the cleaned DataFrame to a new CSV file
df.to_csv('Cleaned_Treasury_Yield.csv', index=False)

print("Cleaning complete. Cleaned data saved to: 'Cleaned_Treasury_Yield.csv'")
