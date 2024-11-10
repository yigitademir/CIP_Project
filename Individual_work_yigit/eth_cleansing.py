import pandas as pd
import pandas_market_calendars as mcal

def column_to_numeric(data, column):
    data[column] = data[column].astype(str).str.replace(r'[^\d.]', '', regex=True).str.strip()
    data[column] = pd.to_numeric(data[column], errors = 'coerce').astype('float')
    return data

#Read the data
df = pd.read_csv("eth_scraped_data.csv")
print(df.shape)
print(df.head())
print(df.columns)

# Drop unnecessary columns and change names
df = df.drop("Date End", axis=1)
df = df.drop("Market Cap", axis=1)
df.rename(columns = {"Date Start": "Date",
                     "Open": "ETH_Open",
                     "High": "ETH_High",
                     "Low": "ETH_Low",
                     "Close": "ETH_Close",
                     "Volume": "ETH_Volume(Billions)"}, inplace=True)
print(df.head())

#Check NA values
print(df.isnull().sum())

#Check and arrange datatypes
df.info()
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

for column in df.columns:
    if column != "Date":
        df = column_to_numeric(df, column)

#Label days for NYSE Market and add as a new "Market" column
nyse = mcal.get_calendar("NYSE")
start_date = df["Date"].min()
end_date = df["Date"].max()
schedule = nyse.schedule(start_date=start_date, end_date=end_date)

df["Market"] = df["Date"].apply(lambda x: "Open" if x in schedule.index else "Closed")

# Filter data and sort by Ascending dates
open_days_df  = df[df["Market"] == "Open"]
ethereum_prices = open_days_df.sort_values(by = "Date", ascending = True).reset_index(drop = True)

# Drop Market column
ethereum_prices.drop("Market", axis=1, inplace=True)

#Add daily difference column
ethereum_prices["ETH_Daily_Difference"] = round(ethereum_prices["ETH_High"] -  ethereum_prices["ETH_Low"], 2)

# Find change in percentage compared the day before
ethereum_prices["1D%"] = round(ethereum_prices["ETH_Close"].pct_change() * 100 , 2)
ethereum_prices["1D%"] = ethereum_prices["1D%"].fillna(0)

print(ethereum_prices.head())

# Write to csv
ethereum_prices.to_csv("ethereum_prices.csv", index=False)



