import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def hVol (data):
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    volatility = log_returns.std() * np.sqrt(252)
    return volatility

# Define the ticker symbol and time window for the golden cross
ticker = "^GSPC"

startD = "2016-01-01"

# Get historical market data for the ticker symbol
stock_data = yf.download(ticker, start=startD)

vol = 1+hVol(stock_data)
golden_cross_short_window = 50
golden_cross_long_window = 200
shortW = round(50*1)
longW = round(166*vol)

# Calculate the moving averages for the golden cross
stock_data['SMA_short'] = stock_data['Close'].rolling(window=golden_cross_short_window).mean()
stock_data['SMA_long'] = stock_data['Close'].rolling(window=golden_cross_long_window).mean()


# Generate signals for the golden cross 1
stock_data['Signal'] = 0.0
stock_data['Signal'] = np.where(stock_data['SMA_short'] > stock_data['SMA_long'], 1.0, 0.0)


# Calculate the daily returns for the stock
stock_data['Returns'] = stock_data['Close'].pct_change()

# Calculate the cumulative returns for the golden cross strategy 1
stock_data['Strategy Returns'] = stock_data['Signal'].shift(1) * stock_data['Returns']


# Calculate the cumulative returns for the passive strategy
stock_data['Passive Returns'] = stock_data['Returns']
stock_data['Passive Cumulative Returns'] = (1 + stock_data['Passive Returns']).cumprod()

# Calculate the cumulative returns for the S&P500 index
sp500_data = yf.download('^GSPC', start=startD)
sp500_data['Returns'] = sp500_data['Close'].pct_change()
sp500_data['Cumulative Returns'] = (1 + sp500_data['Returns']).cumprod()

# Priority change to recent data for overperforming stockv- On test, not part of main project
#mktD = stock_data['Passive Cumulative Returns'][-1]- sp500_data['Cumulative Returns'][-1]
#print(mktD)
#shortW = round(50*1/mktD/2)
#longW = round(166*vol/mktD/2)

# Calculate the moving averages for the dynamic golden cross 
stock_data['SMA_short2'] = stock_data['Close'].rolling(window=shortW).mean()
stock_data['SMA_long2'] = stock_data['Close'].rolling(window=longW).mean()

# Generate signals for the golden cross 2
stock_data['Signal2'] = 0.0
stock_data['Signal2'] = np.where(stock_data['SMA_short2'] > stock_data['SMA_long2'], 1.0, 0.0)

# Calculate the cumulative returns for the golden cross strategy 2
stock_data['Strategy Returns2'] = stock_data['Signal2'].shift(1) * stock_data['Returns']

# Calculate the cumulative returns for the stock, golden cross, and passive strategies
stock_data['Cumulative Returns'] = (1 + stock_data['Strategy Returns']).cumprod()
stock_data['Passive Cumulative Returns'] = (1 + stock_data['Passive Returns']).cumprod()
stock_data['Cumulative Returns2'] = (1 + stock_data['Strategy Returns2']).cumprod()

# Plot the cumulative returns for the stock, golden cross, passive, and S&P500 strategies
plt.plot(stock_data.index, stock_data['Cumulative Returns'], label='Golden Cross')
plt.plot(stock_data.index, stock_data['Cumulative Returns2'], label='Dynamic Golden Cross')
plt.plot(stock_data.index, stock_data['Passive Cumulative Returns'], label='Passive')
plt.plot(sp500_data.index, sp500_data['Cumulative Returns'], label='S&P500')
plt.legend(loc='upper left')
plt.show()

# Print the final cumulative returns for the stock, golden cross, passive, and S&P500 strategies
print('Final Cumulative Returns -', ticker)
print('Golden Cross:', stock_data['Cumulative Returns'][-1])
print('Golden Cross2:', stock_data['Cumulative Returns2'][-1])
print('Passive:', stock_data['Passive Cumulative Returns'][-1])
print('S&P500:', sp500_data['Cumulative Returns'][-1])
print('Volatility:', hVol(stock_data))
