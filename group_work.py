import pandas as pd

tesla = pd.read_csv("Individual_work_furkan/tesla_prices.csv")
interest = pd.read_csv("Individual_work_sujee/Cleaned_Treasury_Yield_Curve.csv")
ethereum = pd.read_csv("Individual_work_yigit/ethereum_prices.csv")

interest.rename(columns ={"date": "Date"}, inplace=True)

merged_data = pd.merge(tesla, ethereum, on="Date", how="left")
merged_data = pd.merge(merged_data, interest, on="Date", how="left")

print(merged_data.head())

merged_data.to_csv("merged_data.csv")


