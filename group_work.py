import pandas as pd
import statsmodels.api as sm

tesla = pd.read_csv("Individual_work_furkan/tesla_prices.csv")
interest = pd.read_csv("Individual_work_sujee/Cleaned_Treasury_Yield_Curve.csv")
ethereum = pd.read_csv("Individual_work_yigit/ethereum_prices.csv")

interest.rename(columns ={"date": "Date"}, inplace=True)

merged_data = pd.merge(tesla, ethereum, on="Date", how="left")
merged_data = pd.merge(merged_data, interest, on="Date", how="left")

print(merged_data.head())

merged_data.to_csv("merged_data.csv")

#%%
# first questions 
data = pd.read_csv('merged_data.csv')

# Calculating daily percentage changes for each specified yield rates term (short/medium/long term)
data['1_mo_change'] = data['1_mo'].pct_change(fill_method=None)
data['3_mo_change'] = data['3_mo'].pct_change(fill_method=None)
data['1_yr_change'] = data['1_yr'].pct_change(fill_method=None)
data['5_yr_change'] = data['5_yr'].pct_change(fill_method=None)
data['10_yr_change'] = data['10_yr'].pct_change(fill_method=None)
data['30_yr_change'] = data['30_yr'].pct_change(fill_method=None)

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

# Etherium: Correlation Analysis
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


# Etherium: Regression Analysis
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
