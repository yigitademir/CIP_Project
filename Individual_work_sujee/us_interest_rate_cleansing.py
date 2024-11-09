import pandas as pd

# Load the data
file_path = r'C:\Users\Sujeethan\switchdrive\SyncVM\MDS\CIP\Project\Individual_work_sujee\Merged_Treasury_Yield_Curve.csv'
df = pd.read_csv(file_path)

# Cleaning steps:

# 1. Handle Missing Values - Drop columns with more than 50% missing values and fill others with median value.
threshold = 0.5 * len(df)
df = df.dropna(axis=1, thresh=threshold)  # Drop columns
df.fillna(df.median(numeric_only=True), inplace=True)  # Fill remaining NaNs with median

# 2. Merge Duplicate Columns - Assume columns with similar names need merging
def merge_columns(df, col1, col2):
    df[col1] = df[col1].combine_first(df[col2])
    df.drop(columns=[col2], inplace=True)

if 'COUPON EQUIVALENT.1' in df.columns:
    merge_columns(df, 'COUPON EQUIVALENT', 'COUPON EQUIVALENT.1')
if 'COUPON EQUIVALENT.2' in df.columns:
    merge_columns(df, 'COUPON EQUIVALENT', 'COUPON EQUIVALENT.2')

# 3. Rename Columns for Consistency
df.columns = df.columns.str.replace('.', '', regex=False).str.replace(' ', '_').str.lower()

# 4. Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 5. Remove Rows with Invalid Dates
df = df[df['date'].notna()]

# 6. Handle Outliers - Example method: Clipping to percentiles (5th and 95th)
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = df[numeric_cols].clip(lower=df[numeric_cols].quantile(0.05), upper=df[numeric_cols].quantile(0.95), axis=1)

# 7. Drop Redundant Columns - Example: 'year' column derived from 'date'
if 'year' in df.columns:
    df.drop(columns=['year'], inplace=True)

# 8. Check and Drop Duplicates
df.drop_duplicates(inplace=True)

# Save the cleaned data
cleaned_file_path = r'C:\Users\Sujeethan\switchdrive\SyncVM\MDS\CIP\Project\Individual_work_sujee\Cleaned_Treasury_Yield_Curve.csv'
df.to_csv(cleaned_file_path, index=False)

print("Cleaning complete. Cleaned data saved to:", cleaned_file_path)
