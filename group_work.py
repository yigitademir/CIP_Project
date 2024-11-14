import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from debugpy.adapter.components import missing

tesla = pd.read_csv("Individual_work_furkan/tesla_prices.csv")
interest = pd.read_csv("Individual_work_sujee/Cleaned_Treasury_Yield_Curve.csv")
ethereum = pd.read_csv("Individual_work_yigit/ethereum_prices.csv")

interest.rename(columns ={"date": "Date"}, inplace=True)

merged_data = pd.merge(tesla, ethereum, on="Date", how="left")
merged_data = pd.merge(merged_data, interest, on="Date", how="left")

print(merged_data.head())

merged_data.to_csv("merged_data.csv")
data = merged_data

#%%
# first questions 
data = pd.read_csv('merged_data.csv')

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
# The target variable as Tesla_1D% for all regressions
y = data['Tesla_1D%']

# Short-term regression analysis
X_short_term = data[['1_mo_change', '3_mo_change']]
X_short_term = sm.add_constant(X_short_term)
short_term_model = sm.OLS(y, X_short_term, missing='drop').fit()

# Medium-term regression analysis
X_medium_term = data[['1_yr_change', '5_yr_change']]
X_medium_term = sm.add_constant(X_medium_term)
medium_term_model = sm.OLS(y, X_medium_term, missing='drop').fit()

# Long-term regression analysis
X_long_term = data[['10_yr_change', '30_yr_change']]
X_long_term = sm.add_constant(X_long_term)
long_term_model = sm.OLS(y, X_long_term, missing='drop').fit()

# Regression summaries for Tesla
print ("\nTESLA Regression Results")
print("\nShort-term Tesla Regression Results:\n", short_term_model.summary())
print("\nMedium-term Tesla Regression Results:\n", medium_term_model.summary())
print("\nLong-term Tesla Regression Results:\n", long_term_model.summary())


# Ethereum: Regression Analysis
# Target variable as ETH_1D% for all regressions
y_eth = data['ETH_1D%']

# Short-term regression analysis for ETH
X_short_term_eth = data[['1_mo_change', '3_mo_change']]
X_short_term_eth = sm.add_constant(X_short_term_eth)
short_term_model_eth = sm.OLS(y_eth, X_short_term_eth, missing='drop').fit()

# Medium-term regression analysis for ETH
X_medium_term_eth = data[['1_yr_change', '5_yr_change']]
X_medium_term_eth = sm.add_constant(X_medium_term_eth)
medium_term_model_eth = sm.OLS(y_eth, X_medium_term_eth, missing='drop').fit()

# Long-term regression analysis for ETH
X_long_term_eth = data[['10_yr_change', '30_yr_change']]
X_long_term_eth = sm.add_constant(X_long_term_eth)
long_term_model_eth = sm.OLS(y_eth, X_long_term_eth, missing='drop').fit()

# Regression summaries for ETH
print ("\nETH Regression Results")
print("\nShort-term ETH Regression Results:\n", short_term_model.summary())
print("\nMedium-term ETH Regression Results:\n", medium_term_model.summary())
print("\nLong-term ETH Regression Results:\n", long_term_model.summary())

# %%

#2nd Question Analysis
#Is there a predictive relationship between shifts in short-term interest rates (1_mo, 3_mo) and intraday volatility of Tesla and Ethereum?

print(30*'*','Research Question 2', 30*'*')

# Calculate intraday volatility for Tesla and Ethereum
data['tesla_intraday_volatility'] = (data['Tesla_1D%'] / data['Tesla_Open']) * 100
data['eth_intraday_volatility'] = (data['ETH_1D%'] / data['ETH_Open']) * 100

# Exploratory Data Analysis
# Scatter plot for Tesla
# Create side-by-side scatter plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Scatter plot for 1-month yield change
axes[0].scatter(data['1_mo_change'], data['tesla_intraday_volatility'])
axes[0].set_xlabel('1-Month Yield Change (%)')
axes[0].set_ylabel('Tesla Intraday Volatility (%)')
axes[0].set_title('Tesla Intraday Volatility vs 1-Month Yield Change')

# Scatter plot for 3-month yield change
axes[1].scatter(data['3_mo_change'], data['tesla_intraday_volatility'])
axes[1].set_xlabel('3-Month Yield Change (%)')
axes[1].set_ylabel('Tesla Intraday Volatility (%)')
axes[1].set_title('Tesla Intraday Volatility vs 3-Month Yield Change')

plt.tight_layout()
plt.show()

# Create side-by-side scatter plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Scatter plot for 1-month yield change
axes[0].scatter(data['1_mo_change'], data['eth_intraday_volatility'])
axes[0].set_xlabel('1-Month Yield Change (%)')
axes[0].set_ylabel('Ethereum Intraday Volatility (%)')
axes[0].set_title('Ethereum Intraday Volatility vs 1-Month Yield Change')

# Scatter plot for 3-month yield change
axes[1].scatter(data['3_mo_change'], data['eth_intraday_volatility'])
axes[1].set_xlabel('3-Month Yield Change (%)')
axes[1].set_ylabel('Ethereum Intraday Volatility (%)')
axes[1].set_title('Ethereum Intraday Volatility vs 3-Month Yield Change')

plt.tight_layout()
plt.show()


# Correlation between short-term yield changes and intraday volatility
correlation_matrix = data[['tesla_intraday_volatility', 'eth_intraday_volatility', '1_mo_change', '3_mo_change']].corr()

# Display full correlation matrix
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print("Correlation Matrix:\n", correlation_matrix)


# Define independent variables (1-month and 3-month yield changes) and add a constant
X = data[['1_mo_change', '3_mo_change']]
X = sm.add_constant(X)

# Tesla intraday volatility as the dependent variable
y_tesla_vol = data['tesla_intraday_volatility'].dropna()
model_tesla_vol = sm.OLS(y_tesla_vol, X.loc[y_tesla_vol.index], missing= 'drop').fit()
print("Tesla Intraday Volatility Regression Results:\n", model_tesla_vol.summary())

# Ethereum intraday volatility as the dependent variable
y_eth_vol = data['eth_intraday_volatility'].dropna()
model_eth_vol = sm.OLS(y_eth_vol, X.loc[y_eth_vol.index], missing= 'drop').fit()
print("Ethereum Intraday Volatility Regression Results:\n", model_eth_vol.summary())


# %%

#3rd Question Analysis
# What is the correlation between medium- to long-term interest rates (e.g., 5_yr, 10_yr) and the volume of trades for Tesla and Ethereum over time?

print(30*'*','Research Question 3', 30*'*')

# Correlation Analysis for Tesla's Trading Volume with Medium- to Long-Term Interest Rates
volume_corr_tesla = data[['Volume', '5_yr', '10_yr']].corr()
print("\nTesla Volume Correlation with Medium- and Long-Term Interest Rates:\n", volume_corr_tesla)

# Correlation Analysis for Ethereum's Trading Volume with Medium- to Long-Term Interest Rates
volume_corr_eth = data[['ETH_Volume', '5_yr', '10_yr']].corr()
print("\nEthereum Volume Correlation with Medium- and Long-Term Interest Rates:\n", volume_corr_eth)

# Regression Analysis for Tesla's Volume with Medium- to Long-Term Interest Rates
X_tesla_vol = data[['5_yr', '10_yr']]
y_tesla_vol = data['Volume']
X_tesla_vol = sm.add_constant(X_tesla_vol)  # Adding a constant term
tesla_vol_model = sm.OLS(y_tesla_vol, X_tesla_vol, missing='drop').fit()
print("\nTesla Volume Regression Results:\n", tesla_vol_model.summary())

# Regression Analysis for Ethereum's Volume with Medium- to Long-Term Interest Rates
X_eth_vol = data[['5_yr', '10_yr']]
y_eth_vol = data['ETH_Volume']
X_eth_vol = sm.add_constant(X_eth_vol)  # Adding a constant term
eth_vol_model = sm.OLS(y_eth_vol, X_eth_vol, missing='drop').fit()
print("\nEthereum Volume Regression Results:\n", eth_vol_model.summary())
