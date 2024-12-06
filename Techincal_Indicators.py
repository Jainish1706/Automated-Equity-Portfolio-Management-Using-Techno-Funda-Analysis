url = 'https://anaconda.org/conda-forge/libta-lib/0.4.0/download/linux-64/libta-lib-0.4.0-h166bdaf_1.tar.bz2'
!curl -L $url | tar xj -C /usr/lib/x86_64-linux-gnu/ lib --strip-components=1
url = 'https://anaconda.org/conda-forge/ta-lib/0.4.19/download/linux-64/ta-lib-0.4.19-py310hde88566_4.tar.bz2'
!curl -L $url | tar xj -C /usr/local/lib/python3.10/dist-packages/ lib/python3.10/site-packages/talib --strip-components=3

import talib
import yfinance as yf
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from mplfinance.original_flavor import candlestick_ohlc
import talib
import shutil
import numpy as np
from scipy.optimize import root



def xnpv(rate, cashflows, dates):
    """
    Calculate the net present value of a series of cashflows at irregular intervals.

    Parameters:
    - rate: The discount rate.
    - cashflows: List of cashflows (positive and negative).
    - dates: List of corresponding dates for each cashflow.

    Returns:
    - XNPV value.
    """
    try:
        return np.nansum([cf / (1 + rate)**((date - dates[0]).days / 365.0) for cf, date in zip(cashflows, dates)])
    except (ZeroDivisionError, RuntimeWarning):
        return np.nan  # Return NaN for any issues

# Set the directory where your CSV files are stored
input_directory = '/content/drive/MyDrive/Stocks_system'

# Set the directory where you want to store the output files
output_directory = '/content/drive/MyDrive/Final_list'

# Initialize lists for XIRR calculation across all stocks
all_cash_flows = []
all_cash_flow_dates = []
all_xirrs = []
all_stock_names = []

# Loop through each CSV file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)

        # Load CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        # Calculate the 20-day and 50-day EMA
        df['ema20'] = talib.EMA(df['Close'], timeperiod=20)
        df['ema50'] = talib.EMA(df['Close'], timeperiod=50)

        # Calculate ADX
        df['adx'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)

        # Calculate ADX slope
        df['adx_slope'] = talib.LINEARREG_SLOPE(df['adx'], timeperiod=5)  # You can adjust the timeperiod as needed

        # Generate signals
        df['signal'] = 0  # 0 represents no signal

        # Buy signal: 20 EMA crosses above 50 EMA, and ADX slope is approaching zero (positive or negative side)
        df.loc[(df['ema20'] > df['ema50']) & ((df['adx_slope'] > 0) | (df['adx_slope'] < 0)) & (df['adx_slope'].abs() < 0.1), 'signal'] = 1

        # Sell signal: 20 EMA crosses below 50 EMA, and ADX slope is approaching zero (positive or negative side)
        df.loc[(df['ema20'] < df['ema50']) & ((df['adx_slope'] > 0) | (df['adx_slope'] < 0)) & (df['adx_slope'].abs() < 0.1), 'signal'] = -1

        # Initialize trade variables
        current_trade = None
        trades = []

        # Initialize lists for XIRR calculation
        cash_flows = []
        cash_flow_dates = []

        # Flag to indicate the first trade is a Buy trade
        first_trade_is_buy = True


        # Loop through the DataFrame to execute trades
        for i in range(1, len(df)):
            if df['signal'][i] == 1 and current_trade is None:
                # Open buy trade if the crossover happens and ADX slope is approaching zero
                current_trade = {'type': 'Buy', 'date': df['Date'][i], 'price': df['Close'][i]}
                # Record cash flow and date for XIRR calculation (considering buy price as negative cash flow)
                cash_flows.append(-current_trade['price'])
                cash_flow_dates.append(pd.to_datetime(current_trade['date']))
            elif df['signal'][i] == -1 and current_trade is None and not first_trade_is_buy:
                # Open sell (short) trade if the crossover happens and ADX slope is approaching zero
                current_trade = {'type': 'Sell', 'date': df['Date'][i], 'price': df['Close'][i]}
                # Record cash flow and date for XIRR calculation (considering sell price as positive cash flow)
                cash_flows.append(current_trade['price'])
                cash_flow_dates.append(pd.to_datetime(current_trade['date']))
            elif current_trade is not None:
                # Check for conditions to close the trade
                if current_trade['type'] == 'Buy' and df['Close'][i] < df['ema50'][i]:
                    # Close buy trade if price closes below 50 EMA
                    current_trade['close_date'] = df['Date'][i]
                    current_trade['close_price'] = df['Close'][i]
                    trades.append(current_trade)

                    # Record cash flow and date for XIRR calculation (considering close price as positive cash flow)
                    cash_flows.append(current_trade['close_price'])
                    cash_flow_dates.append(pd.to_datetime(current_trade['close_date']))

                    current_trade = None
                    first_trade_is_buy = False
                elif current_trade['type'] == 'Sell' and df['Close'][i] > df['ema50'][i]:
                    # Close sell trade if price closes above 50 EMA
                    current_trade['close_date'] = df['Date'][i]
                    current_trade['close_price'] = df['Close'][i]
                    trades.append(current_trade)

                    # Record cash flow and date for XIRR calculation (considering close price as negative cash flow)
                    cash_flows.append(-current_trade['close_price'])
                    cash_flow_dates.append(pd.to_datetime(current_trade['close_date']))

                    current_trade = None

        # Close any remaining open trades at the end of the data
        if current_trade is not None:
            current_trade['close_date'] = df['Date'].iloc[-1]
            current_trade['close_price'] = df['Close'].iloc[-1]
            trades.append(current_trade)

            # Record cash flow and date for the last trade
            if current_trade['type'] == 'Buy':
                cash_flows.append(current_trade['close_price'])
                cash_flow_dates.append(pd.to_datetime(current_trade['close_date']))
            elif current_trade['type'] == 'Sell':
                cash_flows.append(-current_trade['close_price'])
                cash_flow_dates.append(pd.to_datetime(current_trade['close_date']))

        # Display trades
        trade_df = pd.DataFrame(trades)
        print(trade_df)


        # Save trades to Excel file
        trade_df = pd.DataFrame(trades)
        trade_output_path = os.path.join(output_directory, f'{filename.split(".")[0]}_trades.xlsx')
        trade_df.to_excel(trade_output_path, index=False)

        # Print cash flows and corresponding dates
        print(f"Trades saved to: {trade_output_path}")


        # Calculate XIRR using scipy.optimize.root with 'hybr' method
        result = root(xnpv, x0=0.05, args=(cash_flows, cash_flow_dates), method='hybr')

        if result.success:
            xirr = result.x[0]  # Extract the result from the optimization result
            all_cash_flows.append(cash_flows)
            all_cash_flow_dates.append(cash_flow_dates)
            all_xirrs.append(xirr)
            all_stock_names.append(filename.split(".")[0])

            # Print individual XIRR result
            print(f'XIRR for {filename}: {xirr * 100:.2f}%')
        else:
            print(f'Failed to calculate XIRR for {filename}. Check cash flows for invalid values.')

        # Reset cash_flows and cash_flow_dates for the next iteration
        cash_flows = []
        cash_flow_dates = []

# Save aggregated XIRRs to a single file
if all_xirrs:
    all_xirrs_df = pd.DataFrame({'Stock': all_stock_names, 'XIRR': all_xirrs})
    aggregated_xirr_output_path = os.path.join(output_directory, 'aggregated_xirrs.xlsx')
    all_xirrs_df.to_excel(aggregated_xirr_output_path, index=False)
    print(f'Aggregated XIRRs saved to: {aggregated_xirr_output_path}')
else:
    print('No trades to calculate aggregated XIRRs.')

# Print work done
print("Work done!")