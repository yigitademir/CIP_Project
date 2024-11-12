import pandas as pd

# Load the data
file_path = r'C:\Users\Sujeethan\switchdrive\SyncVM\MDS\CIP\Project\Individual_work_sujee\Merged_Treasury_Yield_Curve.csv'
df = pd.read_csv(file_path)

# 1. Remove the columns '4 Mo' and 'Year' if they exist
columns_to_drop = ['4 Mo', 'Year']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Cleaning steps:

# 2. Handle Missing Values - Drop columns with more than 50% missing values and fill others with median value.
threshold = 0.5 * len(df)
df = df.dropna(axis=1, thresh=threshold)  # Drop columns
df.fillna(df.median(numeric_only=True), inplace=True)  # Fill remaining NaNs with median

# 3. Rename Columns for Consistency
df.columns = df.columns.str.replace('.', '', regex=False).str.replace(' ', '_').str.lower()

# 4. Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 5. Check and Drop Duplicates
df.drop_duplicates(inplace=True)

# 6. Change all numeric values to two decimal points except for 'date'
numeric_cols = df.select_dtypes(include='number').columns
for col in numeric_cols:
    if col in df.columns:  # Ensure the column still exists
        df[col] = df[col].round(2)

# 7. Rename columns without modifying 'date'
new_column_names = {col: f"rate_{col}" for col in df.columns if col != 'date'}
df.rename(columns=new_column_names, inplace=True)

# Save the cleaned data
cleaned_file_path = r'C:\Users\Sujeethan\switchdrive\SyncVM\MDS\CIP\Project\Individual_work_sujee\Cleaned_Treasury_Yield_Curve.csv'
df.to_csv(cleaned_file_path, index=False)

print("Cleaning complete. Cleaned data saved to:", cleaned_file_path)
