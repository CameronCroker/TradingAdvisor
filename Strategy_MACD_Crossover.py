# description: This program uses the moving Average Convergence/Divergence (MACD crossover
# to determine when to buy and sell stock.

# description: this program attempts to optimize a users portfolio using Efficient Frontier

#import the libraries
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data as web
plt.style.use('fivethirtyeight')

#Load the data
AAPL = pd.read_csv('AAPL.csv')

#Set the  index
AAPL = AAPL.set_index(pd.DatetimeIndex(AAPL['Date'].values))

#Calculate the MACD and signal line indicators
#Calculate the short term exponential moving average (EMA)
ShortEMA = AAPL.Close.ewm(span=12, adjust=False).mean()
#Calculate the long term exponential moving average
LongEMA = AAPL.Close.ewm(span=26, adjust=False).mean()

#Calculate the MACD line
MACD = ShortEMA - LongEMA

#Span 9 period exponentially smooth average of the macd line
signal = MACD.ewm(span=9 ,adjust=False).mean()

#Create new columns for the data
AAPL['MACD'] = MACD
AAPL['Signal Line'] = signal

#Create a function to signal when to buy an asset
def buy_sell(signal):
    Buy = []
    Sell = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return Buy, Sell

#Create Buy and Sell Column
a = buy_sell(AAPL)
AAPL['Buy_signal_Price'] = a[0]
AAPL['Sell_signal_Price'] = a[1]

#Visually show the stock buy and sell signals
plt.figure(figsize=(12.2, 4.5))
plt.plot(AAPL['Close'], label='Close Price', alpha=0.35)
plt.plot(AAPL['Signal Line'], label='Signal', alpha=0.35)
plt.title('MACD vs Signal line')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Price USD ($)')
plt.scatter(AAPL.index, AAPL['Buy_signal_Price'], color='green', label='Buy', marker='^', alpha=1)
plt.scatter(AAPL.index, AAPL['Sell_signal_Price'], color='red', label='Sell', marker='v', alpha=1)
plt.legend(loc='upper left')

print(AAPL)

plt.show()