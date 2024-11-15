import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from debugpy.adapter.components import missing

# Load the data 
tesla = pd.read_csv("Individual_work_furkan/tesla_prices.csv")
yield_rate = pd.read_csv("Individual_work_sujee/Cleaned_Treasury_Yield.csv")
ethereum = pd.read_csv("Individual_work_yigit/ethereum_prices.csv")

# Rename columns for merging consistency
yield_rate.rename(columns={"date": "Date"}, inplace=True)

# Merge the data
merged_data = pd.merge(tesla.dropna(subset=['Date']), ethereum.dropna(subset=['Date']), on="Date", how="inner")
merged_data = pd.merge(merged_data, yield_rate.dropna(subset=['Date']), on="Date", how="inner")

# Save the cleaned merged data
cleaned_merged_path = "cleaned_merged_data.csv"
merged_data.to_csv(cleaned_merged_path, index=False)

# Print confirmation and display the first few rows of the merged data
print(f"Cleaned merged data saved to: {cleaned_merged_path}")
print(merged_data.head())


#1st Question Analysis
#How do changes in short-term, medium-term, and long-term U.S. Treasury yield rates influence the daily returns of Tesla stock and Ethereum prices?

print(30*'*','Research Question 1', 30*'*')

data = pd.read_csv('cleaned_merged_data.csv')

# Calculating daily percentage changes for each specified yield rates term (short/medium/long term)
data['1_mo_change'] = data['rate_1_mo'].pct_change(fill_method=None)
data['3_mo_change'] = data['rate_3_mo'].pct_change(fill_method=None)
data['1_yr_change'] = data['rate_1_yr'].pct_change(fill_method=None)
data['5_yr_change'] = data['rate_5_yr'].pct_change(fill_method=None)
data['10_yr_change'] = data['rate_10_yr'].pct_change(fill_method=None)
data['30_yr_change'] = data['rate_30_yr'].pct_change(fill_method=None)

# Tesla: Correlation Analysis
# Short-term: 1 month and 3 month yield rates changes
short_term_corr = data[['Tesla_1D%', '1_mo_change', '3_mo_change']].corr()

# Medium-term: 1 year and 5 year yield rates changes
medium_term_corr = data[['Tesla_1D%', '1_yr_change', '5_yr_change']].corr()

# Long-term: 10 year and 30 year yield rates changes
long_term_corr = data[['Tesla_1D%', '10_yr_change', '30_yr_change']].corr()

# Display the results
print("Short-term Tesla Correlation:\n", short_term_corr)
print("\nMedium-term Tesla Correlation:\n", medium_term_corr)
print("\nLong-term Tesla Correlation:\n", long_term_corr)

# Ethereum: Correlation Analysis
# Short-term (1 month and 3 month rate changes)
short_term_corr_eth = data[['ETH_1D%', '1_mo_change', '3_mo_change']].corr()

# Medium-term (1 year and 5 year rate changes)
medium_term_corr_eth = data[['ETH_1D%', '1_yr_change', '5_yr_change']].corr()

# Long-term (10 year and 30 year rate changes)
long_term_corr_eth = data[['ETH_1D%', '10_yr_change', '30_yr_change']].corr()

print("\nShort-term ETH Correlation:\n", short_term_corr_eth)
print("\nMedium-term ETH Correlation:\n", medium_term_corr_eth)
print("\nLong-term ETH Correlation:\n", long_term_corr_eth)


# Tesla: Regression Analysis
# Combine target variable and independent variables for cleaning
tesla_combine = pd.concat([data[['1_mo_change', '3_mo_change', '1_yr_change', '5_yr_change', 
                                 '10_yr_change', '30_yr_change']], data['Tesla_1D%']], axis=1)

# Clean all NaN and inf values
tesla_combine = tesla_combine.replace([np.inf, -np.inf], np.nan).dropna()

# Separate independent variables (X) and target variable (y)
y_tesla = tesla_combine['Tesla_1D%']
X_short_term_tesla = tesla_combine[['1_mo_change', '3_mo_change']]
X_medium_term_tesla = tesla_combine[['1_yr_change', '5_yr_change']]
X_long_term_tesla = tesla_combine[['10_yr_change', '30_yr_change']]

# Short-term regression for Tesla
X_short_term_tesla_clean = sm.add_constant(X_short_term_tesla)  # Add constant for intercept
short_term_tesla_model = sm.OLS(y_tesla, X_short_term_tesla).fit()

# Medium-term regression for Tesla
X_medium_term_tesla = sm.add_constant(X_medium_term_tesla)  # Add constant for intercept
medium_term_tesla_model = sm.OLS(y_tesla, X_medium_term_tesla).fit()

# Long-term regression for Tesla
X_long_term_tesla = sm.add_constant(X_long_term_tesla)  # Add constant for intercept
long_term_tesla_model = sm.OLS(y_tesla, X_long_term_tesla).fit()

# Ethereum: Regression Analysis
# Combine target variable and independent variables for cleaning
eth_combine = pd.concat([data[['1_mo_change', '3_mo_change', '1_yr_change', '5_yr_change', 
                               '10_yr_change', '30_yr_change']], data['ETH_1D%']], axis=1)

# Clean all NaN and inf values
eth_combine = eth_combine.replace([np.inf, -np.inf], np.nan).dropna()

# Separate independent variables (X) and target variable (y)
y_eth = eth_combine['ETH_1D%']
X_short_term_eth = eth_combine[['1_mo_change', '3_mo_change']]
X_medium_term_eth = eth_combine[['1_yr_change', '5_yr_change']]
X_long_term_eth = eth_combine[['10_yr_change', '30_yr_change']]

# Short-term regression for Ethereum
X_short_term_eth = sm.add_constant(X_short_term_eth )  # Add constant for intercept
short_term_eth_model = sm.OLS(y_eth, X_short_term_eth ).fit()

# Medium-term regression for Ethereum
X_medium_term_eth = sm.add_constant(X_medium_term_eth )  # Add constant for intercept
medium_term_eth_model = sm.OLS(y_eth, X_medium_term_eth ).fit()

# Long-term regression for Ethereum
X_long_term_eth_clean = sm.add_constant(X_long_term_eth )  # Add constant for intercept
long_term_eth_model = sm.OLS(y_eth, X_long_term_eth).fit()

# Print regression summaries for Tesla and Ethereum
print("\nTESLA Regression Results")
print("\nShort-term Tesla Regression Results:\n", short_term_tesla_model.summary())
print("\nMedium-term Tesla Regression Results:\n", medium_term_tesla_model.summary())
print("\nLong-term Tesla Regression Results:\n", long_term_tesla_model.summary())

print("\nETH Regression Results")
print("\nShort-term Ethereum Regression Results:\n", short_term_eth_model.summary())
print("\nMedium-term Ethereum Regression Results:\n", medium_term_eth_model.summary())
print("\nLong-term Ethereum Regression Results:\n", long_term_eth_model.summary())


#2nd Question Analysis
#Is there a predictive relationship between shifts in short-term yield_rate rates (1_mo, 3_mo) and intraday volatility of Tesla and Ethereum?

print(30*'*','Research Question 2', 30*'*')

# Calculate intraday volatility for Tesla and Ethereum
data['tesla_intraday_volatility'] = (data['Tesla_Intraday_Range'] / data['Tesla_Open']) * 100
data['eth_intraday_volatility'] = (data['ETH_Intraday_Range'] / data['ETH_Open']) * 100

# Clean NaN and inf values for volatility columns
data['tesla_intraday_volatility'] = data['tesla_intraday_volatility'].replace([np.inf, -np.inf], np.nan).dropna()
data['eth_intraday_volatility'] = data['eth_intraday_volatility'].replace([np.inf, -np.inf], np.nan).dropna()

# Exploratory Data Analysis: Scatter plots
# Tesla Scatter Plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(data['1_mo_change'], data['tesla_intraday_volatility'])
axes[0].set_xlabel('1-Month Yield Change (%)')
axes[0].set_ylabel('Tesla Intraday Volatility (%)')
axes[0].set_title('Tesla Intraday Volatility vs 1-Month Yield Change')

axes[1].scatter(data['3_mo_change'], data['tesla_intraday_volatility'])
axes[1].set_xlabel('3-Month Yield Change (%)')
axes[1].set_ylabel('Tesla Intraday Volatility (%)')
axes[1].set_title('Tesla Intraday Volatility vs 3-Month Yield Change')

plt.tight_layout()
plt.show()

# Ethereum Scatter Plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(data['1_mo_change'], data['eth_intraday_volatility'])
axes[0].set_xlabel('1-Month Yield Change (%)')
axes[0].set_ylabel('Ethereum Intraday Volatility (%)')
axes[0].set_title('Ethereum Intraday Volatility vs 1-Month Yield Change')

axes[1].scatter(data['3_mo_change'], data['eth_intraday_volatility'])
axes[1].set_xlabel('3-Month Yield Change (%)')
axes[1].set_ylabel('Ethereum Intraday Volatility (%)')
axes[1].set_title('Ethereum Intraday Volatility vs 3-Month Yield Change')

plt.tight_layout()
plt.show()

# Correlation Matrix
correlation_matrix = data[['tesla_intraday_volatility', 'eth_intraday_volatility', '1_mo_change', '3_mo_change']].corr()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print("Correlation Matrix:\n", correlation_matrix)

# Regression Analysis
# Clean NaN and inf values in independent variables
X_cleaned = data[['1_mo_change', '3_mo_change']].replace([np.inf, -np.inf], np.nan).dropna()

# Tesla intraday volatility as the dependent variable
y_tesla_vol_cleaned = data['tesla_intraday_volatility'].replace([np.inf, -np.inf], np.nan).dropna()

# Align indices for Tesla
common_index_tesla = X_cleaned.index.intersection(y_tesla_vol_cleaned.index)
X_tesla_aligned = sm.add_constant(X_cleaned.loc[common_index_tesla])
y_tesla_aligned = y_tesla_vol_cleaned.loc[common_index_tesla]

# Tesla regression model
model_tesla_vol = sm.OLS(y_tesla_aligned, X_tesla_aligned).fit()
print("Tesla Intraday Volatility Regression Results:\n", model_tesla_vol.summary())

# Ethereum intraday volatility as the dependent variable
y_eth_vol_cleaned = data['eth_intraday_volatility'].replace([np.inf, -np.inf], np.nan).dropna()

# Align indices for Ethereum
common_index_eth = X_cleaned.index.intersection(y_eth_vol_cleaned.index)
X_eth_aligned = sm.add_constant(X_cleaned.loc[common_index_eth])
y_eth_aligned = y_eth_vol_cleaned.loc[common_index_eth]

# Ethereum regression model
model_eth_vol = sm.OLS(y_eth_aligned, X_eth_aligned).fit()
print("Ethereum Intraday Volatility Regression Results:\n", model_eth_vol.summary())


#3rd Question Analysis
# What is the correlation between medium- to long-term yield_rate rates (e.g., rate_5_yr, 10rate__yr) and the volume of trades for Tesla and Ethereum over time?

print(30*'*','Research Question 3', 30*'*')

# Cleaning Tesla and Ethereum Volume columns
data['Volume'] = data['Volume'].replace({',': ''}, regex=True).astype(float)  # Convert Tesla's Volume to numeric
data['ETH_Volume(Billions)'] = data['ETH_Volume(Billions)'].replace({',': ''}, regex=True).astype(float)  # Convert Ethereum's Volume to numeric

# Research Question 3: Correlation and Regression Analysis
print(30 * '*', 'Research Question 3', 30 * '*')

# Correlation Analysis for Tesla's Trading Volume with Medium- to Long-Term yield_rate Rates
volume_corr_tesla = data[['Volume', 'rate_5_yr', 'rate_10_yr']].corr()
print("\nTesla Volume Correlation with Medium- and Long-Term yield_rate Rates:\n", volume_corr_tesla)

# Correlation Analysis for Ethereum's Trading Volume with Medium- to Long-Term yield_rate Rates
volume_corr_eth = data[['ETH_Volume(Billions)', 'rate_5_yr', 'rate_10_yr']].corr()
print("\nEthereum Volume Correlation with Medium- and Long-Term yield_rate Rates:\n", volume_corr_eth)

# Regression Analysis for Tesla's Volume with Medium- to Long-Term yield_rate Rates
X_tesla_vol = data[['rate_5_yr', 'rate_10_yr']]
y_tesla_vol = data['Volume']
X_tesla_vol = sm.add_constant(X_tesla_vol)  # Adding a constant term
tesla_vol_model = sm.OLS(y_tesla_vol, X_tesla_vol, missing='drop').fit()
print("\nTesla Volume Regression Results:\n", tesla_vol_model.summary())

# Regression Analysis for Ethereum's Volume with Medium- to Long-Term yield_rate Rates
X_eth_vol = data[['rate_5_yr', 'rate_10_yr']]
y_eth_vol = data['ETH_Volume(Billions)']
X_eth_vol = sm.add_constant(X_eth_vol)  # Adding a constant term
eth_vol_model = sm.OLS(y_eth_vol, X_eth_vol, missing='drop').fit()
print("\nEthereum Volume Regression Results:\n", eth_vol_model.summary())

