import pandas as pd
from tradingview_ta import TA_Handler, Interval
import yfinance as yf

# Load the Excel file with openpyxl engine
symbols = pd.read_csv('nifty100.csv')
symbols = symbols['Symbol']
targetPrices = []

for ticker in symbols:
    try:
        #Perform Fundamental Analysis
        file = 'Data/'+ticker+'.xlsx'
        data = pd.read_excel(file, sheet_name='Data Sheet')
        print(data.loc[28])
        begining = data.loc[28][7]
        ending = data.loc[28][9]
        cagr = (ending/begining)**(1/3)-1
        projectIncome = (cagr+1)*ending
        numberShares = data.loc[68][9]
        price = data.loc[88][9]
        actualPrice = data.loc[88][10]
        projectedEps = projectIncome/numberShares
        eps = ending/numberShares
        pe = price/eps
        targetPrice = projectedEps*pe
        xReturns = ((targetPrice/price)-1)*100

        #To get Last Traded Price
        output = TA_Handler(
            symbol=ticker,
            screener="India",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY
        )
        data = yf.download(ticker+".NS", '2022-03-31', '2024-03-31')
        drawdown = ((data['High'].min()/price)-1)*100
        runUp = ((data['High'].max()/price)-1)*100

        ltp = output.get_analysis().indicators['close']
        temp = { 'Stock': ticker, 'CMP(22)' : price, 'Target': round(targetPrice,0), 'xReturn' : round(xReturns, 2),
                 'LTP': round(ltp, 2), 'High': round(data['High'].max(), 2),
                 'CMP(23)' : actualPrice,
                 'Target Hit' : data['High'].max() >= targetPrice,
                 'Drawdown' : drawdown,
                 'Run-up' : runUp,
                 'Range': round(runUp-drawdown, 2)
               }
        targetPrices.append(temp)
        print(ticker+" completed")
    except Exception as e:
        print("Error occured: "+ticker+f': {e}')

df = pd.DataFrame(targetPrices)
df = df.loc[df['xReturns'] > 19]
symbolList = pd.DataFrame(columns=['Symbol'])
symbolList['Symbol'] = df['Stock']
symbolList.to_csv('Screened Stocks.csv')
print(df)
portfolio_data = []

weights = [0.06731798, 0.00540599, 0.00466443, 0.02178775, 0.06498564, 0.13678365
 ,0.01311841, 0.08734345, 0.06980525, 0.00844776, 0.00479463, 0.031153
 ,0.09616128, 0.13515062, 0.0780914 , 0.00642792, 0.03622815 ,0.13233269]

for i in range(len(weights)):
    stock_data = df.iloc[i]  # Select the i-th row from the filtered DataFrame
    quantity = round((100000 * weights[i]) / stock_data['CMP(22)'], 0)  # Replace 'Column_Name' with the actual column name
    buy_value = quantity * stock_data['CMP(22)']
    return_value = quantity * (stock_data['LTP'] - stock_data['CMP(22)'])

    portfolio_data.append({
        'Stock': stock_data['Stock'],  # Replace 'Stock' with the actual column name
        'Quantity': round(quantity, 0),
        'Buy-Value': round(buy_value, 2),
        'Return': round(return_value, 2)
    })

# Create the portfolio DataFrame from the list of dictionaries
portfolio = pd.DataFrame(portfolio_data)

print(portfolio)