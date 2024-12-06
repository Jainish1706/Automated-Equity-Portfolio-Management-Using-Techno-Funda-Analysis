import pandas as pd
import numpy as np
import yfinance as yf
import cvxpy as cp
import matplotlib.pyplot as plt


stock_symbols = ["AXISBANK","BANKBARODA","BPCL","BOSCHLTD","CHOLAFIN","DIVISLAB","GRASIM",
           "JSWSTEEL","ONGC","PFC","PNB","SRF","SIEMENS","SBIN","TATACONSUM","TATAPOWER","TATASTEEL","ZYDUSLIFE"]


temp = []
for symbol in stock_symbols:
  temp.append(symbol+".NS")

stock_symbols = temp
# Define the time frame for historical data
start_date = '2010-01-01'
end_date = '2022-12-31'

stock_data = yf.download(stock_symbols, start=start_date, end=end_date)['Adj Close']

# Calculate daily returns
returns = stock_data.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()
cov_matrix.dropna(inplace=True)
print(cov_matrix)

num_assets = len(stock_symbols)
num_portfolios = 10000

# Set a random seed for reproducibility
np.random.seed(42)

results = []

for _ in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    portfolio_return = np.sum(mean_returns * weights) * 252  # Annualized return
    portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)  # Annualized volatility
    sharpe_ratio = (portfolio_return - 0.0647)/portfolio_std_dev
    results.append([weights, portfolio_return, portfolio_std_dev, sharpe_ratio])

# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=['Portfolio_Weights', 'Portfolio_Return', 'Portfolio_StdDev', 'Sharpe_Ratio'])

max_sharpe_ratio_portfolio = results_df.loc[results_df['Sharpe_Ratio'].idxmax()]

# Find the portfolio with the minimum standard deviation (risk)
min_risk_portfolio = results_df.loc[results_df['Portfolio_StdDev'].idxmin()]

print("Maximum Sharpe Ratio Portfolio:")
print(max_sharpe_ratio_portfolio)
print("\nMinimum Risk Portfolio:")
print(min_risk_portfolio)

print(max_sharpe_ratio_portfolio['Portfolio_Weights'])
print(min_risk_portfolio['Portfolio_Weights'])


plt.figure(figsize=(10, 6))
plt.scatter(results_df['Portfolio_StdDev'], results_df['Portfolio_Return'], c=results_df['Sharpe_Ratio'], cmap='viridis')
plt.title('Efficient Frontier')
plt.xlabel('Portfolio Risk (Standard Deviation)')
plt.ylabel('Portfolio Return')
plt.colorbar(label='Sharpe Ratio')
plt.scatter(max_sharpe_ratio_portfolio['Portfolio_StdDev'], max_sharpe_ratio_portfolio['Portfolio_Return'], c='red', marker='*', s=100, label='Max Sharpe Ratio')
plt.scatter(min_risk_portfolio['Portfolio_StdDev'], min_risk_portfolio['Portfolio_Return'], c='green', marker='*', s=100, label='Min Risk')
plt.legend()

plt.show()